# led-firmware

## General

This project is built with micropython for either the ESP8266 NodeMCU or in the future
the Arduino Nano RP2040H.

## how to start

The initial main file is the `boot.py`.
From their it is separated by api objects and handling
the http server and the led driver as well as the store module.

```tree
.
├── README.md
├── apiserver
│   ├── __init__.py
│   ├── api.py
│   ├── constants.py
│   ├── objects
│   │   ├── __init__.py
│   │   ├── animation.py
│   │   ├── hsl.py
│   │   ├── response.py
│   │   └── rgb.py
│   └── util.py
├── boot.py
├── driver
│   ├── __init__.py
│   ├── animations
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── breath.py
│   │   ├── manual.py
│   │   ├── normal.py
│   │   ├── off.py
│   │   └── snake.py
│   ├── constants.py
│   ├── led.py
│   ├── store.py
│   └── util.py
├── pymakr.conf
├── secure.py
└── webserver
    ├── __init__.py
    └── http.py
```
