
def value_opt(f):
    """
    value_opt decorator wraps a function returning an option name
    and a single or multiple values
    """
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

def bool_opt(f):
    """
    bool_opt decorator wraps a function returning an option name and a
    value that can be evaluated to empty/non-empty
    """
    def wrap(obj, *args, **kwargs):
        opt, val = f(obj)
        if not val:
            return None
        return opt
    return wrap

