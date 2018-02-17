import logging
from docker_replay.args import config_args
from docker_replay.opts import config_opts
from docker_replay.models import DockerOpt, DockerArg

log = logging.getLogger('docker-replay')

class ConfigParser(object):

    args = []
    opts = []

    def __init__(self, config):
        self.config = config

        # build all options
        for op in config_opts:
            o_val = self.get(op.key, op.otype.default)
            self.opts += list(op.build(o_val))

        for ap in config_args:
            o_val = self.get(ap.key)
            self.args += list(ap.build(o_val))

        log.info('parsed %d options' % len(self.opts))
        log.info('parsed %d args' % len(self.args))

    def get(self, key, default=None):
        """
        Retrieve a top-level or nested key, e.g:
        >>> get('Id')
        >>> get('HostConfig.Binds')
        """
        key_parts = key.split('.')
        config = self.config
        while key_parts:
            try:
                config = config[key_parts.pop(0)]
            except KeyError:
                log.warn('returning default for missing key: %s' % key)
                return default
        log.debug('get key: %s (%s)' % (key, config))
        return config
