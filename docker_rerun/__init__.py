import sys
from argparse import ArgumentParser
from docker import Client, errors

from docker_rerun import version
from docker_rerun.decorators import bool_opt, value_opt

class RunCommand(object):
    bool_opts = []
    value_opts = []
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
    @value_opt
    def add_host_opt(self):
        return '--add-host=', self.host_config['ExtraHosts']

    @property
    @value_opt
    def blkio_weight_opt(self):
        return '--blkio-weight=', self.host_config['BlkioWeight']

    @property
    @value_opt
    def blkio_weight_device_opt(self):
        return '--blkio-weight-device=', self.host_config['BlkioWeightDevice']

    @property
    @value_opt
    def cpu_shares_opts(self):
        return '--cpu-shares=', self.config['CpuShares']

    @property
    def entrypoint_opt(self):
        if self.config['Entrypoint']:
            return '--entrypoint="%s"' % ' '.join(self.config['Entrypoint'])

    @property
    @bool_opt
    def interactive_opt(self):
        return '--interactive', self.config['OpenStdin']

    @property
    @value_opt
    def memory_opt(self):
        return '--memory=', self.host_config['Memory']

    @property
    @value_opt
    def name_opt(self):
        return '--name=', self.container['Name'].strip('/')

    @property
    @bool_opt
    def tty_opt(self):
        return '--tty', self.config['Tty']

    @property
    @value_opt
    def user_opt(self):
        return '--user=', self.config['User']

    @property
    @value_opt
    def volume_opt(self):
        return '--volume=', self.host_config['Binds']

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
