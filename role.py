from inspect import isfunction

def consume(*roles):
    def deco(cls):
        for role in roles:
            _add_methods(role, cls)
        return cls
    return deco

def _add_methods(role, cls):
    for attr in dir(role): 
        val = getattr(role, attr)
        if isfunction(val):
            setattr(cls, attr, val)
