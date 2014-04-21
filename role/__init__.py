from inspect import getmembers, isfunction, ismethod

def consume(*roles):
    def deco(cls):
        provided_by = {}
        for role in roles:
            _add_methods(role, cls, provided_by)
        for role in roles:
            _chk_requirements(role, cls)
        return cls
    return deco

def _add_methods(role, cls, provided_by):
    for attr, val in getmembers(role, isfunction): 
        if not hasattr(cls, attr):
            setattr(cls, attr, val)
            provided_by[attr] = role
        elif attr in provided_by:
            raise _conflict_error(attr, role, provided_by)

def _chk_requirements(role, cls):
    for meth in getattr(role, 'requires', ()):
        if not ismethod(getattr(cls, meth, None)):
            raise _requirement_error(cls, meth, role)

def _conflict_error(attr, role, provided_by):
    msg = 'Method %s.%s conflicts with %s.%s' % (
        role.__name__,
        attr,
        provided_by[attr].__name__,
        attr,
    )
    return NameError(msg)

def _requirement_error(cls, meth, role):
    msg = '%s does not have a %s method, which is required by %s' % (
        cls.__name__,
        meth,
        role.__name__,
    )
    return TypeError(msg)
