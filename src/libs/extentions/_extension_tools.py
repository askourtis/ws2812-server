from ..utils import export

@export
def add_attr(at, name):
    def decorator(target):
        setattr(at, name, target)
    return decorator
