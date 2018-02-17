#TODO: ulimits

from docker_replay.models import *

class OptParser(object):
    def __init__(self, o_name, o_key, o_type):
        self.name = o_name
        self.key = o_key
        self.otype = o_type

    # parse given value and yield zero or more DockerOpts
    def build(self, val):
        # yield a new opt for multi-value options(--volume, --env, etc.)
        if self.otype == ValueOpt and isinstance(val, list):
            for v in val:
                yield self.build_one(v)
        elif self.otype == MapOpt and isinstance(val, dict):
            for k,v in val.items():
                val = '%s=%s' % (k,v)
                yield self.build_one(val)
        else:
            yield self.build_one(val)

    def build_one(self, val):
        return self.otype(self.name, val)

class NameParser(OptParser):
    def build(self, val):
        yield self.build_one(val.strip('/'))

class PublishedParser(OptParser):
    def build(self, val):
        if not val:
            return

        def read_hostports(hplist):
            for hp in hplist:
                if hp['HostIp']:
                    yield '%s:%s' % (hp['HostIp'], hp['HostPort'])
                else:
                    yield hp['HostPort']

        for cport, binds in val.items():
            cport, proto = cport.split('/')
            for hostport in read_hostports(binds):
                v = '%s:%s/%s' % (hostport,cport,proto)
                yield self.build_one(v)

class ExposedParser(OptParser):
    def build(self, val):
        if not val:
            return
        for port in val.keys():
            yield self.build_one(port)

class LinkParser(OptParser):
    def build(self, val):
        if not val:
            return
        for link in val:
            src, linkname = link.split(':')
            v = '%s:%s' % (src.strip('/'), linkname.split('/')[-1])
            yield self.build_one(v)

class NetModeParser(OptParser):
    def build(self, val):
        if val == "default":
            return
        yield self.build_one(val)

class RestartParser(OptParser):
    def build(self, val):
        if val['Name'] == 'no':
            return
        v = '%s:%s' % (val['Name'], val['MaximumRetryCount'])
        yield self.build_one(v)

class EntrypointParser(OptParser):
    def build(self, val):
        if val:
            v = '"%s"' % ' '.join(val)
            yield self.build_one(v)

config_opts = [
    OptParser('--env', 'Config.Env', ValueOpt),
    OptParser('--hostname', 'Config.Hostname', ValueOpt),
    OptParser('--interactive', 'Config.OpenStdin', BoolOpt),
    OptParser('--label', 'Config.Labels', MapOpt),
    OptParser('--tty', 'Config.Tty', BoolOpt),
    OptParser('--user', 'Config.User', ValueOpt),
    OptParser('--workdir', 'Config.WorkingDir', ValueOpt),
    OptParser('--add-host', 'HostConfig.ExtraHosts', ValueOpt),
    OptParser('--blkio-weight', 'HostConfig.BlkioWeight', ValueOpt),
    OptParser('--blkio-weight-device', 'HostConfig.BlkioWeightDevice', ValueOpt),
    OptParser('--cap-add', 'HostConfig.CapAdd', ValueOpt),
    OptParser('--cap-drop', 'HostConfig.CapDrop', ValueOpt),
    OptParser('--cgroup-parent', 'HostConfig.CgroupParent', ValueOpt),
    OptParser('--cidfile', 'HostConfig.ContainerIDFile', ValueOpt),
    OptParser('--cpu-period', 'HostConfig.CpuPeriod', ValueOpt),
    OptParser('--cpu-shares', 'HostConfig.CpuShares', ValueOpt),
    OptParser('--cpu-quota', 'HostConfig.CpuQuota', ValueOpt),
    OptParser('--cpuset-cpus', 'HostConfig.CpusetCpus', ValueOpt),
    OptParser('--cpuset-mems', 'HostConfig.CpusetMems', ValueOpt),
    OptParser('--device', 'HostConfig.Devices', ValueOpt),
    OptParser('--device-read-bps', 'HostConfig.BlkioDeviceReadBps', ValueOpt),
    OptParser('--device-read-iops', 'HostConfig.BlkioDeviceReadIOps', ValueOpt),
    OptParser('--device-write-bps', 'HostConfig.BlkioDeviceWriteBps', ValueOpt),
    OptParser('--device-write-iops', 'HostConfig.BlkioDeviceWriteIOps', ValueOpt),
    OptParser('--dns', 'HostConfig.Dns', ValueOpt),
    OptParser('--dns-opt', 'HostConfig.DnsOptions', ValueOpt),
    OptParser('--dns-search', 'HostConfig.DnsSearch', ValueOpt),
    OptParser('--group-add', 'HostConfig.GroupAdd', ValueOpt),
    OptParser('--ipc', 'HostConfig.IpcMode', ValueOpt),
    OptParser('--isolation', 'HostConfig.Isolation', ValueOpt),
    OptParser('--kernel-memory', 'HostConfig.KernelMemory', ValueOpt),
    OptParser('--log-driver', 'HostConfig.LogConfig.Type', ValueOpt),
    OptParser('--log-opt', 'HostConfig.LogConfig.Config', MapOpt),
    OptParser('--memory', 'HostConfig.Memory', ByteValueOpt),
    OptParser('--memory-reservation', 'HostConfig.MemoryReservation', ByteValueOpt),
    OptParser('--memory-swap', 'HostConfig.MemorySwap', ByteValueOpt),
    OptParser('--memory-swappiness', 'HostConfig.MemorySwappiness', ValueOpt),
    OptParser('--oom-kill-disable', 'HostConfig.OomKillDisable', BoolOpt),
    OptParser('--oom-score-adj', 'HostConfig.OomScoreAdj', ValueOpt),
    OptParser('--publish-all', 'HostConfig.PublishAllPorts', BoolOpt),
    OptParser('--pid', 'HostConfig.PidMode', ValueOpt),
    OptParser('--pids-limit', 'HostConfig.PidsLimit', ValueOpt),
    OptParser('--privileged', 'HostConfig.Privileged', BoolOpt),
    OptParser('--read-only', 'HostConfig.ReadonlyRootfs', BoolOpt),
    OptParser('--rm', 'HostConfig.AutoRemove', BoolOpt),
    OptParser('--volume', 'HostConfig.Binds', ValueOpt),
    OptParser('--security-opt', 'HostConfig.SecurityOpt', ValueOpt),
    OptParser('--shm-size', 'HostConfig.ShmSize', ByteValueOpt),
    OptParser('--userns', 'HostConfig.UsernsMode', ValueOpt),
    OptParser('--uts', 'HostConfig.UTSMode', ValueOpt),
    OptParser('--volume-driver', 'HostConfig.VolumeDriver', ValueOpt),
    OptParser('--volumes-from', 'HostConfig.VolumesFrom', ValueOpt),
    OptParser('--ip', 'NetworkSettings.IPAddress', ValueOpt),
#    OptParser('--ip6', 'LinkLocalIPv6Address', ValueOpt),
#    OptParser('--netdefault', '???', ValueOpt),
#    OptParser('--net-alias', '???', ValueOpt),
    OptParser('--mac-address', 'NetworkSettings.MacAddress', ValueOpt),

    # non-generic opt parsers
    EntrypointParser('--entrypoint', 'Config.Entrypoint', DockerOpt),
    ExposedParser('--expose', 'Config.ExposedPorts', DockerOpt),
    LinkParser('--link', 'HostConfig.Links', DockerOpt),
    NameParser('--name', 'Name', DockerOpt),
    NetModeParser('--net', 'HostConfig.NetworkMode', DockerOpt),
    PublishedParser('--publish', 'HostConfig.PortBindings', DockerOpt),
    RestartParser('--restart', 'HostConfig.RestartPolicy', DockerOpt),
  ]
