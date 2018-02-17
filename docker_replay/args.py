from docker_replay.models import DockerArg

class ArgParser(object):
    def __init__(self, o_name, o_key):
        self.name = o_name
        self.key = o_key

    def build(self, val):
        yield DockerArg(self.name, val)

class CmdParser(ArgParser):
    def build(self, val):
        if val:
            val = ' '.join(val)
        yield DockerArg(self.name, val)

config_args = [
  ArgParser('image', 'Config.Image'),
  CmdParser('cmd', 'Config.Cmd'),
]
