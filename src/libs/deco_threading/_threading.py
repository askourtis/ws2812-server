#@format
from .. import export
import threading
import ctypes

_daemons = {}

@export
def daemon(key=None):
    """A decorator factory that starts a deamon thread with the given function for a target

    Args:
        key (Optional[AnyStr], optional): A key to assign to the thread for later use

    Raises:
        KeyError: If the key already exists as a daemon
        
    Returns:
        Callable: The actual decorator
    """
    if key is not None and key in _daemons:
        raise KeyError(f"The key: ${key} is already in the thread pool.")
    
    def decorator(target):
        thread = threading.Thread(target=target, daemon=True)
        if key is not None:
            _daemons[key] = thread
        thread.start()

    return decorator

@export
def raise_at(key, exception):
    """Raises an exception on the selected thread

    Args:
        key (Optional[AnyStr]): The selected key of the thread. If None, then the exeption is forwared to all threads
        exception: The exception to raise

    Raises:
        KeyError: If the selected key is not valid
        ValueError: If any of the treads are already joined
        SystemError: If the raise fails
    """
    if key is None:
        threads = _daemons.values()
    elif key in _daemons:
        threads = [ _daemons[key] ]
    else:
        raise KeyError(f"The key: ${key} is not in the thread pool.")

    for thread_obj in threads:
        found = False
        target_tid = 0
        for tid, tobj in threading._active.items():
            if tobj is thread_obj:
                found = True
                target_tid = tid
                break

        if not found:
            raise ValueError("Invalid thread object")

        ret = ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(target_tid),  ctypes.py_object(exception))
        if ret == 0:
            raise ValueError("Invalid thread ID")
        elif ret > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(target_tid, 0)
            raise SystemError("PyThreadState_SetAsyncExc failed")
