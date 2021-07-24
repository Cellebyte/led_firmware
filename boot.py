# This file is executed on every boot (including wake-boot from deepsleep)
# uos.dupterm(None, 1) # disable REPL on UART(0)

import esp
import uasyncio

from apiserver.api import APIHandler
from driver.led import LEDDriver
from secure import password, wlan
from webserver.http import HTTPServer

esp.osdebug(None)

led_driver = LEDDriver(144, 1)
api_handler = APIHandler(leds=led_driver)
http_server = HTTPServer(wlan, password, 80, handler=api_handler)
led_driver.reset()
http_server.init()


async def main(http_server: HTTPServer, led_driver: LEDDriver):
    loop = uasyncio.get_event_loop()
    server = http_server.start()
    loop.create_task(server)
    loop.create_task(led_driver.start())
    server = await server
    await server.wait_closed()
    # await uasyncio.sleep_ms(10_000)


while True:
    try:
        uasyncio.run(main(http_server, led_driver))
    except KeyboardInterrupt:
        loop = uasyncio.get_event_loop()
        print("closing")
        loop.stop()
        uasyncio.close()
