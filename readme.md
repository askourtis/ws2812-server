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

|Code|Data|Description|Example|
|:--:|:--:|:---------:|:-----:|
|0x0|-|Ends the program|```[0x0]```|
|0x1|R,G,B|Sets the ledstrip to a single RGB color|```[0x1, 0x00, 0xFF, 0x00]```
|0x2|i,R,G,B|Sets a specific led in the ledstrip to an RGB color|```[0x2, 0x3, 0xFF, 0x00, 0xFF]```
|0x3|ByteArray|Selects an animation to be played|```[0x3, *b'rainbow']```
