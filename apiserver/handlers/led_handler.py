import json
from typing import Optional

import ure
from apiserver.handlers.base_handler import BaseHandler
from driver.led import LEDDriver
from errors import ALL_UNSUPPORTED, BODY_MISSING, EXCEPTION_ERROR
from objects.animation import Animation
from objects.response import Response
from objects.rgb import RGB
from webserver.http import Request


class LEDHandler(BaseHandler):
    paths = ["/leds", "/leds/"]
    path_regex = ure.compile("/leds/(\d+)")

    def __init__(self, leds: LEDDriver) -> None:
        self.leds = leds
        self.rgb = RGB(0, 0, 0)
        self.animation = Animation("manual")

    def post_leds(self, body, unit=None) -> Response:
        if not body:
            return self.response.from_dict(*BODY_MISSING)
        try:
            rgb = self.rgb.from_dict(json.loads(body))
        except (ValueError, TypeError, KeyError) as e:
            return self.response.from_dict(*EXCEPTION_ERROR(e))
        # If the led endpoint is used controller gets forced to manual mode
        self.leds.animation = self.animation
        if unit is None:
            self.leds.set_all(rgb)
        else:
            self.leds.set(rgb, unit)
        return self.response.from_dict(rgb.as_dict(), 201)

    def get_leds(self, unit=None) -> Response:
        if unit is None:
            return self.response.from_dict(*ALL_UNSUPPORTED)
        self.rgb.from_vector(self.leds.pixels[unit])
        return self.response.from_dict(self.rgb.as_dict(), 200)

    def router(self, request: Request) -> Optional[Response]:
        if request.path in self.paths:
            if "POST" == request.method:
                return self.post_leds(request.body)
            elif "GET" == request.method:
                return self.get_leds()
        elif match := self.path_regex.match(request.path):
            led = int(match.group(1))
            if led >= self.leds.len_leds:
                return self.response.from_dict({"error": "LED unavailable!"}, 404)
            if "POST" == request.method:
                return self.post_leds(request.body, unit=led)
            elif "GET" == request.method:
                return self.get_leds(unit=led)
        return None
