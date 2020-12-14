#! /usr/bin/env python3

# SECTION Imports
from libs                import *
from queue               import Queue
from rpi_ws281x          import PixelStrip
from socket              import socket
from time                import sleep
# !SECTION

# SECTION Constants
class LedSettings:
    """A class to hold all the information for the ledstrip"""
    COUNT      = 8       # Number of LED pixels.
    PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
    FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
    DMA        = 10      # DMA channel to use for generating signal (try 10)
    BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
    INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
    CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

class Networking:
    """A class to hold all the information for the networking"""
    from socket import AF_INET as INET, SOCK_DGRAM as UDP
    
    ADDRESS = ("rpizw", 5005)
    
    class Codes:
        """A class to hold all the possible codes for the network commands"""
        EXIT      = 0
        SINGLE    = 1
        SPECIFIC  = 2
        ANIMATION = 3
        
class Threading:
    """A class to hold all the information for threading"""
    class Keys:
        """A class to hold all the possible keys for the daemons"""
        ANIMATOR = "animator"
        PRODUCER = "producer"

# !SECTION

# SECTION Init
strip = PixelStrip( LedSettings.COUNT       ,
                    LedSettings.PIN         ,
                    LedSettings.FREQ_HZ     ,
                    LedSettings.DMA         ,
                    LedSettings.INVERT      ,
                    LedSettings.BRIGHTNESS  ,
                    LedSettings.CHANNEL     )
strip.begin()

requests        = Queue()
animation_queue = Queue(1)
# !SECTION

# SECTION Workers
@daemon(key=Threading.Keys.ANIMATOR)
def animator():
    """Pops an item from the animation queue, or waits for the next item to come, passing the strip to the function as the first and only argument"""
    while True:
        try:
            print("ANIMATOR: Waiting next animation...")
            animation = animation_queue.get()
            print(f"ANIMATOR: Playing animation {animation.__name__}")
            animation(strip)
        except InterruptedError:
            print("ANIMATOR: Interrupted")

@daemon(key=Threading.Keys.PRODUCER)
def producer():
    """Recieves and pushes, into the request queue, the next command from the network"""
    with socket(Networking.INET, Networking.UDP) as sock:
        sock.bind(Networking.ADDRESS)
        while True:
            print("NETWORK: Wait for packet...")
            data, addr = sock.recvfrom(1024)
            print(f"NETWORK: Recieved from {addr} data={data}")
            requests.put_nowait( (data[0], data[1:]) )
# !SECTION

# SECTION Main
try:
    while True:
        print("CONSUMER: Wait for command...")
        code, data = requests.get()
        print(f"CONSUMER: Popped code={code} with data={data}")
        
        # Interrupt animator
        raise_at(Threading.Keys.ANIMATOR, InterruptedError)
        
        # Translate codes
        if code == Networking.Codes.EXIT:
            print("CONSUMER: Exitting...")
            break
        elif code == Networking.Codes.SINGLE:
            strip[:] = [ Color.RGB( *data ) ] * len(strip)
            strip.show()
        elif code == Networking.Codes.SPECIFIC:
            strip[ data[0] ] = Color.RGB( *data[1:] )
            strip.show()
        elif code == Networking.Codes.ANIMATION:
            animation_queue.put_nowait(get_animation(data.decode()))
        else:
            print(f"CONSUMER: Could not translate code={code}")
except KeyboardInterrupt:
    pass
except Exception as ex:
    print(f"CONSUMER: Could not translate code={code}\n\tError: {ex}")
# !SECTION


# SECTION Clean up
strip[:] = [ Color.RGB(0,0,0) ] * len(strip)
strip.show()
# !SECTION
