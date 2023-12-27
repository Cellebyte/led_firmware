# from driver.util import gc_info
import gc
import time
from typing import Optional

import network
import uasyncio
import ure

from webserver.util import CODE_TO_MESSAGE


class Request:
    def __init__(self, method, path, headers, body):
        self.method = method.upper()
        self.path = path.lower()
        self.headers = headers
        self.body = body

    def __repr__(self) -> str:
        return "{}({}, {}, {}, {})".format(
            self.__class__.__name__, self.method, self.path, self.headers, self.body
        )


class HTTPServer:
    backlog = 5
    end_line = "\r\n"
    http_proto_regex = ure.compile(
        "^(GET|HEAD|POST|PUT|DELETE|CONNECT|OPTIONS|TRACE)\s(.*?)\sHTTP\/1\.1$"
    )

    def __init__(self, essid, password, port, handler):
        self.essid = essid
        self.wlan: Optional[network.WLAN] = None
        self.password = password
        self.port = port
        self.handler = handler

    def start(self):
        return uasyncio.start_server(
            self.handle_request, "0.0.0.0", self.port, backlog=self.backlog
        )

    def __enter__(self):
        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)
        print("connecting to network...")
        self.reconnect()
        print("network config:", self.wlan.ifconfig())
        return self

    def __exit__(self, *_):
        if self.wlan and self.wlan.isconnected():
            self.wlan.disconnect()

        return False

    def reconnect(self):
        if self.wlan is not None:
            while not self.wlan.isconnected():
                self.wlan.connect(self.essid, self.password)
                time.sleep(10)
        return

    def parse_request(self, request):
        splitted = request.split("{}{}".format(self.end_line, self.end_line), 1)
        headers = splitted[0]
        body = ""
        try:
            body = splitted[1]
        except IndexError:
            pass
        headers = headers.split(self.end_line)
        http_proto = headers.pop(0)
        match = self.http_proto_regex.search(http_proto)
        if not match:
            return None
        method = match.group(1)
        path = match.group(2)
        headers = dict(header.split(": ", 1) for header in headers)
        del request
        return Request(method, path, headers, body)

    async def handle_request(self, reader, writer):
        self.reconnect()
        try:
            request = None
            request = await reader.read(1024)
            request = self.parse_request(request.decode("utf8"))
            response = self.handler.handle(request)
            print("Content = {}".format(request))
            await writer.awrite(
                "HTTP/1.1 {} {}{}".format(
                    response.code, CODE_TO_MESSAGE(response.code), self.end_line
                )
            )
            for key, value in response.headers.items():
                await writer.awrite("{}: {}{}".format(key, value, self.end_line))
            await writer.awrite(
                "Connection: close{}{}".format(self.end_line, self.end_line)
            )
            await writer.awrite("{}{}".format(response, self.end_line))
            gc.collect()
            await uasyncio.sleep_ms(5)
        except OSError as e:
            print(e)
        finally:
            await reader.drain()
            reader.close
            await reader.wait_closed()
            await writer.drain()
            writer.close()
            await writer.wait_closed()
            # gc_info()
