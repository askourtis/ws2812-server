from .. import export

_animations = {}

@export
def animation(target):
    """Registers an animation"""
    key = target.__name__
    
    if key in _animations:
        raise KeyError(f"Key: {key} is already registered.")
    
    _animations[key] = target
    print(f"Added new animation: {key}")
    
    return target


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
