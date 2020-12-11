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
