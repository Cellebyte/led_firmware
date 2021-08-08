# This file is executed on every boot (including wake-boot from deepsleep)
# uos.dupterm(None, 1) # disable REPL on UART(0)

import gc

import esp
import machine
import uasyncio

from animations.manual import Manual
from animations.normal import Normal
from animations.off import Off
from animations.snake import Snake
from apiserver.api import APIHandler
from driver.color_store import ColorStore
from driver.led import LEDDriver
from driver.store import Store
from secure import password, wlan
from webserver.http import HTTPServer

esp.osdebug(None)

store = Store()
color_store = ColorStore(store=store, slots=6)
led_driver = LEDDriver(144, 1, store=store)
snake = Snake(store, color_store, led_driver)
normal = Normal(store, color_store, led_driver)
off = Off(store, led_driver)
manual = Manual(store, led_driver)
led_driver.register_animation(snake)
led_driver.register_animation(off)
led_driver.register_animation(normal)
led_driver.register_animation(manual)
api_handler = APIHandler(leds=led_driver)
http_server = HTTPServer(wlan, password, 80, handler=api_handler)
led_driver.reset()
led_driver.write()
http_server.init()
machine.freq(160000000)


async def main(http_server: HTTPServer, led_driver: LEDDriver):
    loop = uasyncio.get_event_loop()
    server = http_server.start()
    loop.create_task(server)
    loop.create_task(led_driver.start())
    loop.create_task(store.start())
    server = await server
    await server.wait_closed()
    await uasyncio.sleep_ms(10_000)


while True:
    try:
        uasyncio.run(main(http_server, led_driver))
        gc.collect()
    except KeyboardInterrupt:
        print("closing")
    finally:
        loop = uasyncio.get_event_loop()
        loop.stop()
        loop.close()
        break
