
class DockerOpt(object):
    def __init__(self, opt, val):
        self.opt = opt
        self.value = val

    def is_null(self):
        if self.value:
            return False
        return True

class BoolOpt(DockerOpt):
    def __init__(self, *args):
        DockerOpt.__init__(self, *args)

    def __str__(self):
        return self.opt

#TODO: add ByteValueOpt type to convert bytes to human-readable string
class ValueOpt(DockerOpt):
    """ Option with one or more user-defined values """
    def __init__(self, *args):
        DockerOpt.__init__(self, *args)

    def __str__(self):
        if isinstance(self.value, str):
            return '%s %s' % (self.opt, self.value)
        elif isinstance(self.value, int):
            return '%s %s' % (self.opt, self.value)
        elif isinstance(self.value, float):
            return '%s %s' % (self.opt, self.value)
        elif isinstance(self.value, list):
            return ' '.join([ '%s %s' % (self.opt, v) for v in self.value ])
        else:
            raise TypeError('unsupported value type for option "%s": %s' % \
                    (self.opt, self.value))

class MapOpt(DockerOpt):
    """ Option with one or more user-defined mappings """
    def __init__(self, *args):
        DockerOpt.__init__(self, *args)

    def __str__(self):
        if not isinstance(self.value, dict):
            raise TypeError('unsupported value type for option "%s": %s' % \
                    (self.opt, self.value))
        kvlist = [ '%s=%s' % (k,v) for k,v in self.value.items() ]
        return ' '.join([ '%s %s' % (self.opt, i) for i in kvlist ])
