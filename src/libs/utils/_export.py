import sys

__all__ = [ 'export' ]

def export(target):
    """Exposes the selected callable to the namespace

    Args:
        target (Callable): The callable

    Returns:
        Callable: The target
    """
    mod = sys.modules[target.__module__]
    if hasattr(mod, '__all__'):
        mod.__all__.append(target.__name__)
    else:
        mod.__all__ = [ target.__name__ ]
    return target
