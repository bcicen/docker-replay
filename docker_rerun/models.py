#class OptionParser(dict):
#    def __init__(self, *args):
#        dict.__init__(self, args)
#
#    def __getitem__(self, key):
#        val = dict.__getitem__(self, key)
#        print("GET")
#        return val
#
#    def __setitem__(self, key, val):
#        print("SET")
#        dict.__setitem__(self, key, val)

class DockerOpt(object):
    def is_null(self):
        if self.value:
            return False
        return True

class BoolOpt(DockerOpt):
    def __init__(self, opt, val):
        self.opt = opt
        self.value = val

    def __str__(self):
        return self.opt

class ValueOpt(DockerOpt):
    """ Option with one or more user-defined values """
    def __init__(self, opt, val):
        self.opt = opt
        self.value = val

    def __str__(self):
        if isinstance(self.value, str): 
            return '%s%s' % (self.opt, self.value)
        elif isinstance(self.value, list):
            return ' '.join([ '%s%s' % (self.opt, v) for v in self.value ])
        else:
            raise TypeError('unsupported value type for option "%s": %s' % \
                    (self.opt, self.value))

class MultiValueOpt(DockerOpt):
    def __init__(self):
        pass

def parse_opt(opt, value):
    if not value:
        return None

    if isinstance(value, bool):
        parse_bool_opt(opt, value)
    elif isinstance(value, list):
        parse_multivalue_opt(opt, value)
    elif isinstance(value, string):
        parse_value_opt(opt, value)

def parse_value_opt(f):
    def wrap(obj, *args, **kwargs):
        opt, val = f(obj)
        if not val:
            return None
        if isinstance(val, str): 
            return '%s%s' % (opt, val)
        elif isinstance(val, list):
            return ' '.join([ '%s%s' % (opt, v) for v in val ])
        else:
            raise TypeError('unsupported option value type: %s' % val)
    return wrap

def parse_bool_opt(opt, value):
    def wrap(obj, *args, **kwargs):
        opt, val = f(obj)
        if not val:
            return None
        return opt
    return wrap

