from apiserver.handlers.base_handler import BaseHandler
from driver.led import LEDDriver
from webserver.http import Request
import ure
from errors import ALL_UNSUPPORTED, BODY_MISSING, EXCEPTION_ERROR
from objects.animation import Animation
from objects.response import Response
from objects.rgb import RGB
import json


class LEDHandler(BaseHandler):
    paths = ["/leds", "/leds/"]
    path_regex = ure.compile("/leds/(\d+)")

    def __init__(self, leds: LEDDriver) -> None:
        self.leds = leds

    def post_leds(self, body, unit=None) -> Response:
        if not body:
            return Response(*BODY_MISSING)
        try:
            rgb = RGB(**(json.loads(body)))
        except (ValueError, TypeError) as e:
            return Response(*EXCEPTION_ERROR(e))
        # If the led endpoint is used controller gets forced to manual mode
        self.leds.animation = Animation("manual")
        if unit is None:
            self.leds.set_all(rgb)
        else:
            self.leds.set(rgb, unit)
        return Response(rgb.as_dict(), 201)

    def get_leds(self, unit=None) -> Response:
        if unit is None:
            return Response(*ALL_UNSUPPORTED)
        elif unit < self.leds.len_leds:
            rgb = RGB(0, 0, 0)
            rgb.from_vector(self.leds.pixels[unit])
            return Response(rgb.as_dict(), 200)
        else:
            return Response({"error": "LED unavailable!"}, 404)

    def router(self, request: Request) -> Response:
        if request.path in self.paths:
            if "POST" == request.method:
                return self.post_leds(request.body)
            elif "GET" == request.method:
                return self.get_leds()
        elif self.path_regex.match(request.path):
            match = self.path_regex.match(request.path)
            led = int(match.group(1))
            if "POST" == request.method:
                return self.post_leds(request.body, unit=led)
            elif "GET" == request.method:
                return self.get_leds(unit=led)
        return None
