import sys
from argparse import ArgumentParser
from docker import Client, errors

from docker_rerun import version
from docker_rerun.models import BoolOpt, ValueOpt

config_opts = [
    ('--cpu-shares=', 'CpuShares', ValueOpt),
    ('--interactive', 'OpenStdin', BoolOpt),
    ('--tty', 'Tty', BoolOpt),
    ('--user=', 'User', ValueOpt)
  ]

host_config_opts = [
    ('--add-host=', 'ExtraHosts', ValueOpt),
    ('--blkio-weight=', 'BlkioWeight', ValueOpt),
    ('--blkio-weight-device=', 'BlkioWeightDevice', ValueOpt),
    ('--memory=', 'Memory', ValueOpt),
    ('--volume=', 'Binds', ValueOpt)
  ]

class RunCommand(object):
    def __init__(self, container_id, pretty_print=True):
        self.pretty_print = pretty_print
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
        if self.config['Cmd']:
            return (' ').join(self.config['Cmd'])

    @property
    def entrypoint(self):
        if self.config['Entrypoint']:
            return '--entrypoint="%s"' % ' '.join(self.config['Entrypoint'])

    @property
    def name(self):
        return '--name=%s' % self.container['Name'].strip('/')

    def _get_value(self, source, key):
        return source.get(key)

    def assemble_opts(self):
        all_opts = []

        # add all config opts
        for opt_name, key, opt_type in config_opts:
            all_opts.append(opt_type(opt_name, self.config.get(key)))

        # add all host_config opts
        for opt_name, key, opt_type in host_config_opts:
            all_opts.append(opt_type(opt_name, self.host_config.get(key)))

        return [ str(o) for o in all_opts if not o.is_null() ]

    def __str__(self):
        opts = self.assemble_opts()
        opts.append(self.name)

        if self.entrypoint:
            opts.append(self.entrypoint)

        if self.cmd:
            opts.append(self.cmd)

        if self.pretty_print:
            return 'docker run %s' % ' \\\n           '.join(opts)
        return 'docker run %s' % ' '.join(opts)

def main():
    parser = ArgumentParser(description='docker-rerun v%s' % version)
    parser.add_argument('container', help='container to generate command from')

    args = parser.parse_args()

    print(RunCommand(args.container))
