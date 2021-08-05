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

## The Store Module

`driver.store.Store` is handling all the state keeping between shutdowns.
This keeps the colors and necessary data from the animations persisted onto the Microcontroller.
It does that by reading every 240 ticks the json file and comparing it with the current state.
If the state changed it dumps it back to disk. This is working as redisdump.

## The LEDDriver

`driver.led.LedDriver` is handling the LEDs. It manages the setting of LEDs which animation is currently in control and
also what animations are registered and available to the driver.

## Animations

### snake

This is an animation which runs a connected length of leds through the led strip.
It stores the `steps` between each tick the `length` of the snake and the `color`.

### breath

This is an animation which pulses between different colors.
It stores up to 6 `colors` and transitions between them.

### off

This shows always `RGB(0,0,0)`. The off state.

### normal

This is a normal color selector which sets the color of all LEDs at once and is persisted between reboots.

### manual

This mode is automatically activated when the `/leds/` and the `/leds/{unit}` endpoint is used.
It does nothing directly with the LEDs except displaying the current state of each NeoPixel.


## API

### :: [GET,POST]/leds/?

Gets and sets all LEDs.

```bash
export ENDPOINT=127.0.2.1
curl -X GET "$ENDPOINT/leds"
{"error": "scraping data of all leds is not supported"}
```

```bash
export ENDPOINT=127.0.2.1
curl -d '{ "red": 0, "green": 255, "blue": 0}' -X POST "$ENDPOINT/leds"
{"green": 255, "blue": 0, "red": 0}
```

### :: [GET,POST] /leds/{unit}/?

Gets and sets LED by unit.

```bash
export ENDPOINT=127.0.2.1
curl -X GET "$ENDPOINT/leds/0"
{"green": 255, "blue": 0, "red": 0}
```

```bash
export ENDPOINT=127.0.2.1
curl -d '{ "red": 0, "green": 255, "blue": 0}' -X POST "$ENDPOINT/leds/0"
{"green": 255, "blue": 0, "red": 0}
```

### :: [GET] /lens/?

```bash
export ENDPOINT=127.0.2.1
curl -X GET "$ENDPOINT/lens"
{"first": 0, "last": 143}
```
### :: [GET,POST] /animation/?

```bash
export ENDPOINT=127.0.2.1
curl -X GET "$ENDPOINT/animation"
{"animation": "manual"}
```

```bash
export ENDPOINT=127.0.2.1
curl -d '{"animation": "snake"}' -X POST "$ENDPOINT/animation"
{"animation": "snake"}
```

### :: [GET,PUT] /animation/{Animation.SUPPORTED}/?

```bash
export ENDPOINT=127.0.2.1
curl -X GET "$ENDPOINT/animation/snake"
{"color": {"green": 0, "blue": 128, "red": 135}, "steps": 1, "length": 53}
```

```bash
export ENDPOINT=127.0.2.1
curl -d {"steps": 2} -X PUT "$ENDPOINT/animation/snake"
{"color": {"green": 0, "blue": 128, "red": 135}, "steps": 2, "length": 53}
```
