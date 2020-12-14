from rpi_ws281x         import PixelStrip
from ._extension_tools  import add_attr

__all__ = []

@add_attr(PixelStrip, "__len__")
def strip_len(self):
    return self._led_data.size

@add_attr(PixelStrip, "__setitem__")
def strip_set_item(self, idx, value):
    self._led_data[idx] = value
    
@add_attr(PixelStrip, "__getitem__")
def strip_get_item(self, idx):
    return self._led_data[idx]
