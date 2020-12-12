from . import export

@export
class Color:
    """A class to group all color related functions"""
    @staticmethod
    def RGB(R, G, B):
        """Coverts an RGB triplet to a single integer

        Args:
            R (byte): A byte representing the brightness of the Red color
            G (byte): A byte representing the brightness of the Green color
            B (byte): A byte representing the brightness of the Blue color

        Returns:
            [int]: A single color integer
        """
        return  ((R << 16) & 0xFF0000) | ((G << 8) & 0x00FF00) | ((B << 0) & 0x0000FF) 

    @staticmethod
    def HSV(H, S, V):
        """Coverts an HSV triplet to a single integer

        Args:
            H (float): A float [0,360) representing the hue
            S (float): A float [0,1] representing the saturation
            V (float): A float [0,1] representing the value

        Returns:
            [int]: A single color integer
        """
        C = V * S
        X = C * (1 - abs( (H/60) % 2 - 1 ))
        m = V - C

        H = H % 360

        if 0 <= H < 60:
            R, G, B = C, X, 0
        elif 60 <= H < 120:
            R, G, B = X, C, 0
        elif 120 <= H < 180:
            R, G, B = 0, C, X
        elif 180 <= H < 240:
            R, G, B = 0, X, C
        elif 240 <= H < 300:
            R, G, B = X, 0, C
        elif 300 <= H < 360:
            R, G, B = C, 0, X

        return Color.RGB( int((R+m)*255), int((G+m)*255), int((B+m)*255) )
