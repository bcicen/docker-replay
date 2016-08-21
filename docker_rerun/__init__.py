import sys
import logging
from argparse import ArgumentParser
from docker import Client, errors

from docker_rerun import version
from docker_rerun.opts import OptionParser

log = logging.getLogger('docker-rerun')
logging.basicConfig(level=logging.INFO)

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

    def __str__(self):
        opts = [ str(o) for o in self.parser.opts if not o.is_null() ]
        opts += [ str(a) for a in self.parser.args if not a.is_null() ]

        if self.pretty_print:
            return 'docker run %s' % ' \\\n           '.join(opts)
        return 'docker run %s' % ' '.join(opts)

def main():
    parser = ArgumentParser(description='docker-rerun v%s' % version)
    parser.add_argument('container', help='container to generate command from')

    args = parser.parse_args()

    print(RunCommand(args.container))
