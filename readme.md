# A DIY WS2812 project

## Description

This is a DIY project for smart leds, built for Raspberry PI zero W.

Goals:

- 🚧 Efficient CPU usage, using daemon threads with locks and condition variables
- 🚧 Minimal bandwidth usage to drive the leds via UDP
- 🚧 Clean and readable code, using the best possible idioms of python3🐍
- 🚧 No bugs 🐛
- ✅ To have fun 😁😁

## Libraries

Although the whole project is supposed to be a DIY project, an initial use of an external library to get the project started is a good idea.

For this I used the awesome library [ws2812x-python](https://github.com/rpi-ws281x/rpi-ws281x-python).

To install the library execute the following command:

```shell
sudo pip install rpi_ws281x
```

## Networking

The communication "protocol" is quite simple. It consists of two parts, the code and the data.

|  Code  |   Data    |
|:------:|:---------:|
|  Byte  | ByteArray |

For example lets say, I want to send a command that sets all the leds to the RED color. The command that I should send is the following

```python
[0x01, 0xFF, 0x00, 0x00]
```

Translating the above command:

The first byte '0x01' is the code of the command, it translates to "I want to set all the leds to a specific color". The rest 3 bytes are needed to set the RGB color. First we send the RED byte, then the GREEN, then the BLUE

There are 4 possible codes (for now):

|Code |    Data   |                      Description                    |              Example               |
|:---:|:--------: |:---------------------------------------------------:|:----------------------------------:|
| 0x0 |     -     | Ends the program                                    | ```[0x0]```                        |
| 0x1 |   R,G,B   | Sets the ledstrip to a single RGB color             | ```[0x1, 0x00, 0xFF, 0x00]```      |
| 0x2 |  i,R,G,B  | Sets a specific led in the ledstrip to an RGB color | ```[0x2, 0x3, 0xFF, 0x00, 0xFF]``` |
| 0x3 | ByteArray | Selects an animation to be played                   | ```[0x3, *b'rainbow']```           |

## Animations

To create a new animation you can insert your new animation as a python3 function. Add a new function in the [animations file](./src/libs/animations/animations.py) as shown below.

```python
@animation
def rainbow(strip):
    LEN  = len(strip)*50
    LEDS = [ Color.HSV(v*360/LEN, 1, 1) for v in range(LEN) ]
    while True:
        LEDS = [ LEDS[-1], *LEDS[:-1] ]
        strip[:] = LEDS[0:len(strip)+1]
        strip.show()
        sleep(0.01)
```

## Service Installation

To ensure that the script will run on startup, the Systemd Services. The installation script is robust and subject of change, as soon as my knowledge on the topic get better.

To install the service execute the following

```bash
sudo make service
```

The service default name is ```smart-leds-server``` but it can be changed by changing the ```NAME``` variable in the following files:

- [service.sh](./service.sh)
- [daemon-controller.sh](./daemon-controller.sh)

This change should occure before service installation!

## Console

The service starts a screen session with the name of the prementions variables. This screen is a part of the superuser screens since the command starts with sudo.

To connect to the default screen execute the following:

```bash
sudo screen -rd smart-leds-server
```

Please consider having only one screen named as smart-leds-server, so you dont have conflicting screen names!

If the ```NAME``` variable was changed, then the screen name will change accordingly!
