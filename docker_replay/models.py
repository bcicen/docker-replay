
class DockerParam(object):
    """ Base class for options or arguments """

    default = None

    def __init__(self, name, val):
        self.name = name
        self.value = val

    def is_null(self):
        if self.value:
            return False
        return True

class DockerArg(DockerParam):
    """ Represents a positional argument to `docker run` """

    def __str__(self):
        return self.value

class DockerOpt(DockerParam):
    """ Represents an option to `docker run` """

    def __str__(self):
        return '%s %s' % (self.name, self.value)

"""
Generic option types
"""

class BoolOpt(DockerOpt):
    def __init__(self, *args):
        super(DockerOpt, self).__init__(*args)
        # DockerOpt.__init__(self, *args)

    def __str__(self):
        return self.name

class ByteValueOpt(DockerOpt):
    """ Option with one or more user-defined values """

    @staticmethod
    def format_bytes(x):
        KB = 1024
        MB = KB*1024
        GB = MB*1024

        def _round(x):
            return int(round(x))

        x = float(x)
        if x < 1024:
            return '%sb' % _round(x)
        elif 1024 <= x < MB:
            return '%sk' % _round(x/KB)
        elif KB <= x < GB:
            return '%sm' % _round(x/MB)
        elif GB <= x:
            return '%sg' % _round(x/GB)

    def __str__(self):
        try:
            return '%s %s' % (self.name, self.format_bytes(self.value))
        except ValueError:
            raise TypeError('unsupported value type for option "%s": %s' % \
                    (self.name, self.value))

class ValueOpt(DockerOpt):
    """ Option with one or more user-defined values """

    def __str__(self):
        try:
            return '%s %s' % (self.name, self.value)
        except ValueError:
            raise TypeError('unsupported value type for option "%s": %s' % \
                    (self.name, self.value))

class MapOpt(ValueOpt):
    """ Option with one or more user-defined mappings """

    default = {}
