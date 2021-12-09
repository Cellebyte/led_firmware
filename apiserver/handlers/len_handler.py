from typing import Optional

from apiserver.handlers.base_handler import BaseHandler
from driver.led import LEDDriver
from objects.response import Response
from webserver.http import Request


class LenHandler(BaseHandler):
    paths = ["/lens", "/lens/"]

    def __init__(self, leds: LEDDriver) -> None:
        self.leds = leds

    def get_strip(self) -> Response:
        return self.response.from_dict(
            {
                "last": self.leds.len_leds - 1,
                "first": 0,
            },
            200,
        )

    def router(self, request: Request) -> Optional[Response]:
        if request.path in self.paths:
            if "GET" == request.method:
                return self.get_strip()
        return None
