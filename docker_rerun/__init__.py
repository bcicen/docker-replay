import sys
from argparse import ArgumentParser
from docker import Client, errors

from docker_rerun import version
from docker_rerun.opts import OptionParser

class RunCommand(object):
    def __init__(self, container_id, pretty_print=True):
        self.pretty_print = pretty_print
        client = Client()
        try:
            inspect = client.inspect_container(container_id)
            self.parser = OptionParser(inspect)
        except errors.NotFound:
            print('no such container: %s' % container_id)
            sys.exit(1)

    @property
    def cmd(self):
        key = 'Config.Cmd' 
        if self.parser.get(key):
            return (' ').join(self.parser.get(key))

    @property
    def entrypoint(self):
        key = 'Config.Entrypoint' 
        if self.parser.get(key):
            return '--entrypoint="%s"' % ' '.join(self.parser.get(key))

    @property
    def name(self):
        return '--name=%s' % self.parser.get('Name').strip('/')

    def __str__(self):
        opts = self.parser.get_all_opts()
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
