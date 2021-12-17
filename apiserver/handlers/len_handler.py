from collections import OrderedDict
from typing import Optional

from apiserver.handlers.base_handler import BaseHandler
from driver.led import LEDDriver
from apiserver.response import Response
from webserver.http import Request


class LenHandler(BaseHandler):
    paths = ["/lens", "/lens/"]

    def __init__(self, leds: LEDDriver) -> None:
        self.leds = leds

    def get_strip(self) -> Response:
        return Response.from_dict(
            OrderedDict(
                [
                    ("first", 0),
                    ("last", self.leds.len_leds - 1),
                ]
            ),
            200,
        )

    def router(self, request: Request) -> Optional[Response]:
        if request.path in self.paths:
            if "GET" == request.method:
                return self.get_strip()
        return None
