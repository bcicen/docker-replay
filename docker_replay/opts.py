#TODO: ulimits

import logging
from docker_replay.models import *

log = logging.getLogger('docker-replay')

class OptionParser(object):

    args = []
    opts = []

    def __init__(self, config):
        self.config = config

        self.read_opts()
        self.read_args()

        log.info('parsed %d options' % len(self.opts))
        log.info('parsed %d args' % len(self.args))

    def read_opts(self):
        # read in all basic options
        for o_name, o_key, o_type in config_opts:
            o_val = self.get(o_key, o_type.default)
            self.opts += list(build_opt(o_type, o_name, o_val))

        # read options requiring unique parsing
        self.opts.append(DockerOpt('--name', self.get('Name').strip('/')))

        # published ports
        val = self.get('HostConfig.PortBindings')
        self.opts += list(self.read_published(val))

        # exposed ports
        val = self.get('Config.ExposedPorts')
        self.opts += list(self.read_exposed(val))

        # network mode
        val = self.get('HostConfig.NetworkMode')
        self.opts.append(self.read_netmode(val))

        # container links
        val = self.get('HostConfig.Links')
        self.opts += list(self.read_links(val))

        # restart policy
        val = self.get('HostConfig.RestartPolicy')
        self.opts.append(self.read_restart(val))

        # entrypoint
        val = self.get('Config.Entrypoint')
        self.opts.append(self.read_entrypoint(val))

    def read_args(self):
        # image
        self.args.append(DockerArg('Image', self.get('Config.Image')))

        # cmd
        val = self.get('Config.Cmd')
        self.args.append(self.read_cmd(val))

    @staticmethod
    def read_published(bindings):
        def read_hostports(hplist):
            for hp in hplist:
                if hp['HostIp']:
                    yield '%s:%s' % (hp['HostIp'], hp['HostPort'])
                else:
                    yield hp['HostPort']

        if not bindings:
            return

        for cport,binds in bindings.items():
            cport, proto = cport.split('/')
            for hostport in read_hostports(binds):
                val = '%s:%s/%s' % (hostport,cport,proto)
                yield DockerOpt('--publish', val)

    @staticmethod
    def read_exposed(exposed):
        if not exposed:
            return
        for port in exposed:
            yield DockerOpt('--expose', port)

    @staticmethod
    def read_links(links):
        if not links:
            return
        for link in links:
            src, linkname = link.split(':')
            val = '%s:%s' % (src.strip('/'), linkname.split('/')[-1])
            yield DockerOpt('--link', val)

    @staticmethod
    def read_netmode(mode):
        if mode == "default":
            mode = None
        return DockerOpt('--net', mode)

    @staticmethod
    def read_restart(policy):
        if policy['Name'] == 'on-failure':
            val = 'on-failure:%s' % policy['MaximumRetryCount']
        elif policy['Name'] == 'always':
            val = 'on-failure:%s' % policy['MaximumRetryCount']
        else:
            val = None
        return DockerOpt('--restart', val)

    @staticmethod
    def read_entrypoint(ep):
        if ep:
            ep = '"%s"' % ' '.join(ep)
        return DockerOpt('--entrypoint', ep)

    @staticmethod
    def read_cmd(cmd):
        if cmd:
            cmd = ' '.join(cmd)
        return DockerArg('Cmd', cmd)

    def get(self, key, default=None):
        """
        Retrieve a top-level or nested key, e.g:
        >>> get('Id')
        >>> get('HostConfig.Binds')
        """
        log.debug('get for key: %s' % key)
        key_parts = key.split('.')
        config = self.config
        while key_parts:
            try:
                config = config[key_parts.pop(0)]
            except KeyError:
                log.info('returning null for non-existent key: %s' % key)
                return default
        return config

config_opts = [
    ('--env', 'Config.Env', ValueOpt),
    ('--hostname', 'Config.Hostname', ValueOpt),
    ('--interactive', 'Config.OpenStdin', BoolOpt),
    ('--label', 'Config.Labels', MapOpt),
    ('--tty', 'Config.Tty', BoolOpt),
    ('--user', 'Config.User', ValueOpt),
    ('--workdir', 'Config.WorkingDir', ValueOpt),
    ('--add-host', 'HostConfig.ExtraHosts', ValueOpt),
    ('--blkio-weight', 'HostConfig.BlkioWeight', ValueOpt),
    ('--blkio-weight-device', 'HostConfig.BlkioWeightDevice', ValueOpt),
    ('--cap-add', 'HostConfig.CapAdd', ValueOpt),
    ('--cap-drop', 'HostConfig.CapDrop', ValueOpt),
    ('--cgroup-parent', 'HostConfig.CgroupParent', ValueOpt),
    ('--cidfile', 'HostConfig.ContainerIDFile', ValueOpt),
    ('--cpu-period', 'HostConfig.CpuPeriod', ValueOpt),
    ('--cpu-shares', 'HostConfig.CpuShares', ValueOpt),
    ('--cpu-quota', 'HostConfig.CpuQuota', ValueOpt),
    ('--cpuset-cpus', 'HostConfig.CpusetCpus', ValueOpt),
    ('--cpuset-mems', 'HostConfig.CpusetMems', ValueOpt),
    ('--device', 'HostConfig.Devices', ValueOpt),
    ('--device-read-bps', 'HostConfig.BlkioDeviceReadBps', ValueOpt),
    ('--device-read-iops', 'HostConfig.BlkioDeviceReadIOps', ValueOpt),
    ('--device-write-bps', 'HostConfig.BlkioDeviceWriteBps', ValueOpt),
    ('--device-write-iops', 'HostConfig.BlkioDeviceWriteIOps', ValueOpt),
    ('--dns', 'HostConfig.Dns', ValueOpt),
    ('--dns-opt', 'HostConfig.DnsOptions', ValueOpt),
    ('--dns-search', 'HostConfig.DnsSearch', ValueOpt),
    ('--group-add', 'HostConfig.GroupAdd', ValueOpt),
    ('--ipc', 'HostConfig.IpcMode', ValueOpt),
    ('--isolation', 'HostConfig.Isolation', ValueOpt),
    ('--kernel-memory', 'HostConfig.KernelMemory', ValueOpt),
    ('--log-driver', 'HostConfig.LogConfig.Type', ValueOpt),
    ('--log-opt', 'HostConfig.LogConfig.Config', MapOpt),
    ('--memory', 'HostConfig.Memory', ByteValueOpt),
    ('--memory-reservation', 'HostConfig.MemoryReservation', ByteValueOpt),
    ('--memory-swap', 'HostConfig.MemorySwap', ByteValueOpt),
    ('--memory-swappiness', 'HostConfig.MemorySwappiness', ValueOpt),
    ('--oom-kill-disable', 'HostConfig.OomKillDisable', BoolOpt),
    ('--oom-score-adj', 'HostConfig.OomScoreAdj', ValueOpt),
    ('--publish-all', 'HostConfig.PublishAllPorts', BoolOpt),
    ('--pid', 'HostConfig.PidMode', ValueOpt),
    ('--pids-limit', 'HostConfig.PidsLimit', ValueOpt),
    ('--privileged', 'HostConfig.Privileged', BoolOpt),
    ('--read-only', 'HostConfig.ReadonlyRootfs', BoolOpt),
    ('--rm', 'HostConfig.AutoRemove', BoolOpt),
    ('--volume', 'HostConfig.Binds', ValueOpt),
    ('--security-opt', 'HostConfig.SecurityOpt', ValueOpt),
    ('--shm-size', 'HostConfig.ShmSize', ByteValueOpt),
    ('--userns', 'HostConfig.UsernsMode', ValueOpt),
    ('--uts', 'HostConfig.UTSMode', ValueOpt),
    ('--volume-driver', 'HostConfig.VolumeDriver', ValueOpt),
    ('--volumes-from', 'HostConfig.VolumesFrom', ValueOpt),
    ('--ip', 'NetworkSettings.IPAddress', ValueOpt),
#    ('--ip6', 'LinkLocalIPv6Address', ValueOpt),
#    ('--netdefault', '???', ValueOpt),
#    ('--net-alias', '???', ValueOpt),
    ('--mac-address', 'NetworkSettings.MacAddress', ValueOpt)
  ]
