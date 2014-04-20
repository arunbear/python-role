from inspect import getmembers, isfunction

def consume(*roles):
    def deco(cls):
        provided_by = {}
        for role in roles:
            _add_methods(role, cls, provided_by)
        return cls
    return deco

def _add_methods(role, cls, provided_by):
    for attr, val in getmembers(role, isfunction): 
        if not hasattr(cls, attr):
            setattr(cls, attr, val)
            provided_by[attr] = role
        elif attr in provided_by:
            raise _conflict_error(attr, role, provided_by)

def _conflict_error(attr, role, provided_by):
    msg = 'Method %s.%s conflicts with %s.%s' % (
        role.__name__,
        attr,
        provided_by[attr].__name__,
        attr,
    )
    return NameError(msg)
