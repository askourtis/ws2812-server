from ..                import export, Color
from ._animation_utils import animation
from time              import sleep

@animation
def rainbow(strip):
    LEN  = len(strip)*50
    LEDS = [ Color.HSV(v*360/LEN, 1, 1) for v in range(LEN) ]
    while True:
        LEDS = [ LEDS[-1], *LEDS[:-1] ]
        strip[:] = LEDS[0:len(strip)+1]
        strip.show()
        sleep(0.01)

# TODO Add more animations