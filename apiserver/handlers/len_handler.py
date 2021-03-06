from collections import OrderedDict
from typing import Optional

from apiserver.handlers.base_handler import BaseHandler
from apiserver.response import Response
from driver.led import LEDDriver
from webserver.http import Request


class LenHandler(BaseHandler):
    paths = ["/api/v1/lens", "/api/v1/lens/"]

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
            elif "OPTIONS" == request.method:
                return Response(body={}, code=200, headers=self.headers)
        return None
