from . import export

@export
class Color:
    """A class to group all color related functions"""
    @staticmethod
    def RGB(R, G, B):
        return  ((R << 16) & 0xFF0000) | ((G << 8) & 0x00FF00) | ((B << 0) & 0x0000FF) 
