# This file is executed on every boot (including wake-boot from deepsleep)
# uos.dupterm(None, 1) # disable REPL on UART(0)

REDUCED_FEATURESET = True
import os

if getattr(os.uname(), "sysname") == "esp32":
    REDUCED_FEATURESET = False
try:
    import esp

    esp.osdebug(None)
except ImportError:
    REDUCED_FEATURESET = False
    pass

# import machine
import micropython
import uasyncio
from driver.led import LEDDriver
from driver.store import Store
from secure import password, wlan
from webserver.http import HTTPServer
from apiserver.handlers.led_handler import LEDHandler
from apiserver.handlers.len_handler import LenHandler
from apiserver.handlers.animation_handler import AnimationHandler
from apiserver.handlers.gc_handler import GCHandler
from apiserver.api import API
from animations.manual import Manual
from animations.off import Off


# machine.freq(160000000)

if __name__ == "__main__":
    micropython.alloc_emergency_exception_buf(100)

    store = Store()
    led_driver = LEDDriver(144, 1, store=store)
    led_driver.register_animation(Off(store, led_driver))
    led_driver.register_animation(Manual(store, led_driver))
    api = API()
    api.register_handler(LEDHandler(led_driver))
    api.register_handler(LenHandler(led_driver))
    api.register_handler(AnimationHandler(led_driver))
    api.register_handler(GCHandler())

    if not REDUCED_FEATURESET:
        from animations.normal import Normal
        from animations.snake import Snake
        from animations.breath import Breath
        from driver.color_store import ColorStore
        from apiserver.handlers.color_handler import ColorHandler

        color_store = ColorStore(store=store, slots=10)
        led_driver.register_animation(Snake(store, color_store, led_driver))
        led_driver.register_animation(Normal(store, color_store, led_driver))
        led_driver.register_animation(Breath(store, color_store, led_driver))
        api.register_handler(ColorHandler(color_store))

    with HTTPServer(wlan, password, 80, handler=api) as http_server:
        led_driver.reset()
        led_driver.write()

        async def main(http_server: HTTPServer, led_driver: LEDDriver):
            loop = uasyncio.get_event_loop()
            server = http_server.start()
            loop.create_task(server)
            loop.create_task(led_driver.start())
            loop.create_task(store.start())
            server = await server
            await server.wait_closed()
            await uasyncio.sleep_ms(10_000)

        try:
            uasyncio.run(main(http_server, led_driver))
        except KeyboardInterrupt:
            print("closing")
        finally:
            loop = uasyncio.get_event_loop()
            loop.stop()
            loop.close()
