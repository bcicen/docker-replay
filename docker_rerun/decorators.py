
def value_opt(f):
    def wrap(obj, *args, **kwargs):
        opt, val = f(obj)
        if not val:
            return None
        if isinstance(val, str): 
            return '%s%s' % (opt, val)
        elif isinstance(val, list):
            return ' '.join([ '%s%s' % (opt, v) for v in val ])
        else:
            raise TypeError('unknown option value type: %s' % val)
    return wrap

def bool_opt(f):
    def wrap(obj, *args, **kwargs):
        opt, val = f(obj)
        if not val:
            return None
        return opt
    return wrap

