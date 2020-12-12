from ..utils import export

_animations = {}

@export
def animation(key):
    """Registers an animation

    Args:
        key (AnyStr): A key to store the animation

    Raises:
        KeyError: If the key is none or already in use

    Returns:
        [Callable]: A decorator to register the target
    """
    if key is None:
        raise KeyError("None is not a valid key.")
    
    if key in _animations:
        raise KeyError(f"Key: {key} is already in use.")
    
    def decorator(target):
        _animations[key] = target
        print(f"Added new animation: {key}")
        return target
    return decorator

@export
def get_animation(key):
    """Returns the animation object given a key

    Args:
        key (AnyStr): The key of the animation

    Raises:
        KeyError: If the key is none or not in use

    Returns:
        [Callable]: The selected animation
    """
    if key is None:
        raise KeyError("None is not a valid key.")
    
    if key not in _animations:
        raise KeyError(f"Key: ${key} is not in use.")
    
    return _animations[key]
