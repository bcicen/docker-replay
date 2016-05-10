import sys
from argparse import ArgumentParser
from docker import Client, errors

from docker_rerun import version

def value_opt(f):
    def wrap(obj):
        opt, val = f()
        if not val:
            return None
        if isinstance(val, str): 
            return '%s%s' % (opt, val)
        elif isinstance(val, list):
            return ' '.join([ '%s%s' % (opt, v) for v in val ])
        else:
            raise TypeError('unknown option value type: %s' % val)

    return wrap(obj)

def bool_opt(f):
    def wrap(obj):
        opt, val = f()
        if not val:
            return None
        return opt

    return wrap(obj)

class RunCommand(object):
    def __init__(self, container_id):
        client = Client()
        try:
            self.container = client.inspect_container(container_id)
            self.config = self.container['Config']
            self.host_config = self.container['HostConfig']
        except errors.NotFound:
            print('no such container: %s' % container_id)
            sys.exit(1)

    @property
    def cmd(self):
        return (' ').join(self.config['Cmd'])

    @property
    def add_host_opt(self):
        if not self.host_config['ExtraHosts']:
            return None
        return ' '.join([ '--add-host=%s' % h for h in \
                self.host_config['ExtraHosts'] ])

    @property
    def blkio_weight_opt(self):
        if self.host_config['BlkioWeight']:
            return '--blkio-weight="%s"' % self.host_config['BlkioWeight']

    @property
    def blkio_weight_device_opt(self):
        if self.host_config['BlkioWeightDevice']:
            return '--blkio-weight-device="%s"' % self.host_config['BlkioWeightDevice']

    @property
    def cpu_shares_opts(self):
        if self.config['CpuShares']:
            return '--cpu-shares' % self.config['CpuShares']

    @property
    def entrypoint_opt(self):
        if self.config['Entrypoint']:
            return '--entrypoint="%s"' % ' '.join(self.config['Entrypoint'])

    @property
    @bool_opt
    def interactive_opt(self):
        return '--interactive', self.config['OpenStdin']

    @property
    def memory_opt(self):
        if self.host_config['Memory']:
            return '--memory="%s"' % self.host_config['Memory']

    @property
    def name_opt(self):
        return '--name="%s"' % self.container['Name'].strip('/')

    @property
    def tty_opt(self):
        if self.config['Tty']:
            return '--tty'

    @property
    def user_opt(self):
        if self.config['User']:
            return '--user="%s"' % self.config['User']

    @property
    def volume_opt(self):
        return ' '.join([ '--volume=%s' % v for v in \
                self.host_config['Binds'] ])

    def build_opts(self):
        opts = [ o for o in self._all_opts() if o ]
        return ' '.join(opts)

    def _all_opts(self):
        return [ self.__getattribute__(a) for a in \
                 dir(self) if a.endswith('_opt') ]

    def __str__(self):
        return 'docker run %s' % self.build_opts()

def main():
    parser = ArgumentParser(description='docker-rerun v%s' % version)
    parser.add_argument('container', help='container to generate command from')

    args = parser.parse_args()

    print(RunCommand(args.container))

if __name__ == '__main__':
    main()
