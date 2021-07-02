# This file is executed on every boot (including wake-boot from deepsleep)
# uos.dupterm(None, 1) # disable REPL on UART(0)
import gc

import esp
import micropython

from apiserver.api import APIHandler
from driver.led import LEDDriver
from webserver.http import HTTPServer
from secure import wlan, password
esp.osdebug(None)


def gc_info():
    print("--------------------------------------------------")
    print("Memory allocated: {} bytes".format(gc.mem_alloc()))
    print("Memory free:      {} bytes".format(gc.mem_free()))
    print("--------------------------------------------------")
    print(micropython.mem_info())
    print("--------------------------------------------------")


led_driver = LEDDriver(144, 1)
api_handler = APIHandler(led=led_driver)
http_server = HTTPServer(wlan, password, 80, handler=api_handler)
led_driver.reset()
http_server.init()
count = 0
while True:
    count += 1
    if count >= 60:
        count = 0
    http_server.loop(count)
    gc_info()
    gc.collect()
    gc_info()
