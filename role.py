from inspect import getmembers, isfunction

def consume(*roles):
    def deco(cls):
        for role in roles:
            _add_methods(role, cls)
        return cls
    return deco

def _add_methods(role, cls):
    for attr, val in getmembers(role, isfunction): 
        setattr(cls, attr, val)
