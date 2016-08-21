#TODO: expose ports
#TODO: published ports
#TODO: restart policy
#TODO: ulimits

import logging
from docker_rerun.models import ValueOpt, BoolOpt, MapOpt

log = logging.getLogger('docker-rerun')
logging.basicConfig(level=logging.INFO)

class OptionParser(object):
    def __init__(self, config):
        self.config = config

    def get_all_opts(self):
        def iter_opts():
            for o_name, o_key, o_type in config_opts:
                opt = o_type(o_name, self.get(o_key))
                if not opt.is_null():
                    log.info('found configured option: %s' % str(opt))
                    yield str(opt)
        return list(iter_opts())

    def get(self, key):
        """
        Retrieve a top-level or nested key, e.g:
        >>> get('Id')
        >>> get('HostConfig.Binds')
        """
        log.debug('get for key: %s' % key)
        key_parts = key.split('.')
        config = self.config
        while key_parts:
            config = config[key_parts.pop(0)]
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
    ('--link', 'HostConfig.Links', ValueOpt),
    ('--log-driver', 'HostConfig.LogConfig.Type', ValueOpt),
    ('--log-opt', 'HostConfig.LogConfig.Config', MapOpt),
    ('--memory', 'HostConfig.Memory', ValueOpt),
    ('--memory-reservation', 'HostConfig.MemoryReservation', ValueOpt),
    ('--memory-swap', 'HostConfig.MemorySwap', ValueOpt),
    ('--memory-swappiness', 'HostConfig.MemorySwappiness', ValueOpt),
    ('--oom-kill-disable', 'HostConfig.OomKillDisable', BoolOpt),
    ('--oom-score-adj', 'HostConfig.OomScoreAdj', ValueOpt),
    ('--publish-all', 'HostConfig.PublishAllPorts', BoolOpt),
#    ('--publish', 'HostConfig.???', ValueOpt),
    ('--pid', 'HostConfig.PidMode', ValueOpt),
    ('--pids-limit', 'HostConfig.PidsLimit', ValueOpt),
    ('--privileged', 'HostConfig.Privileged', BoolOpt),
    ('--read-only', 'HostConfig.ReadonlyRootfs', BoolOpt),
    ('--rm', 'HostConfig.AutoRemove', BoolOpt),
    ('--volume', 'HostConfig.Binds', ValueOpt),
    ('--security-opt', 'HostConfig.SecurityOpt', ValueOpt),
    ('--shm-size', 'HostConfig.ShmSize', ValueOpt),
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
