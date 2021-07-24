import gc

import network
import uasyncio
import ure


class Request:
    def __init__(self, method, path, headers, body):
        self.method = method.upper()
        self.path = path.lower()
        self.headers = headers
        self.body = body

    def __repr__(self) -> str:
        return "Request({}, {}, {}, {})".format(
            self.method, self.path, self.headers, self.body
        )


class HTTPServer:
    backlog = 5
    end_line = "\r\n"
    http_proto_regex = ure.compile(
        "^(GET|HEAD|POST|PUT|DELETE|CONNECT|OPTIONS|TRACE)\s(.*?)\sHTTP\/1\.1$"
    )

    def __init__(self, essid, password, port, handler):
        self.essid = essid
        self.wlan = None
        self.socket = None
        self.password = password
        self.port = port
        self.handler = handler

    def start(self):
        return uasyncio.start_server(
            self.handle_request, "0.0.0.0", self.port, backlog=self.backlog
        )

    def reconnect(self):
        while not self.wlan.isconnected():
            pass
        return

    def start_internet_connection(self):
        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)
        if not self.wlan.isconnected():
            print("connecting to network...")
        self.wlan.connect(self.essid, self.password)
        while not self.wlan.isconnected():
            pass
        print("network config:", self.wlan.ifconfig())

    def init(self):
        self.start_internet_connection()

    def parse_request(self, request):
        splitted = request.split("{}{}".format(self.end_line, self.end_line), 1)
        headers = splitted[0]
        body = splitted[1]
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
        try:
            request = None
            request = await reader.read(1024)
            request = self.parse_request(request.decode("utf8"))
            response = self.handler.handle(request)
            print("Content = {}".format(request))
            await writer.awrite(
                "HTTP/1.1 {} {}{}".format(
                    response.code, response.message, self.end_line
                )
            )
            await writer.awrite("Content-Type: application/json{}".format(self.end_line))
            await writer.awrite("Connection: close{}{}".format(self.end_line, self.end_line))
            await writer.awrite("{}{}".format(response, self.end_line))
            await reader.drain()
            reader.close
            await reader.wait_closed()
            await writer.drain()
            writer.close()
            await writer.wait_closed()

            gc.collect()
            await uasyncio.sleep_ms(10)
        except OSError as e:
            print(e)
