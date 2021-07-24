import json

import ure
from driver.led import LEDDriver
from webserver.http import Request

from . import util
from .objects.animation import Animation
from .objects.rgb import RGB


class Response:
    def __init__(self, body, code) -> None:
        self.code = code
        self.body = body
        self.message = util.code_to_message(code)

    def __str__(self):
        return json.dumps(self.body)


class APIHandler:
    led_paths = ["/leds", "/leds/"]
    led_path_regex = ure.compile("/leds/(\d+)")
    len_paths = ["/lens", "/lens/"]
    color_paths = ["/colors", "/colors/"]
    color_path_regex = ure.compile("/colors/(\d+)")
    animation_paths = ["/animation", "/animation/"]

    def __init__(self, leds) -> None:
        self.leds: LEDDriver = leds

    def post_animation(self, body):
        if not body:
            return Response({"error": "Body needs to be provided!"}, 400)
        try:
            animation = Animation(**(json.loads(body)))
            self.leds.set_animation(animation)
        except (ValueError, TypeError) as e:
            return Response({"error": "{}".format(e)}, 400)
        return Response(
            animation.as_dict(),
            201
        )

    def get_animation(self):
        return Response(
            self.leds.animation.as_dict(),
            200,
        )

    def post_leds(self, body, unit=None):
        if not body:
            return Response({"error": "Body needs to be provided!"}, 400)
        try:
            rgb = RGB(**(json.loads(body)))
        except (ValueError, TypeError) as e:
            return Response({"error": "{}".format(e)}, 400)
        if unit is None:
            self.leds.set_all(rgb.as_vector())
        else:
            self.leds.set(rgb.as_vector(), unit)
        self.leds.write()
        return Response(rgb.as_dict(), 201)

    def get_strip(self):
        return Response(
            {
                "last": self.leds.len_leds - 1,
                "first": 0,
            },
            200,
        )

    def get_leds(self, unit=None):
        if unit is None:
            return Response(
                {"error": "scraping data of all leds is not supported"},
                501,
            )
        elif unit < self.leds.len_leds:
            rgb = RGB(0, 0, 0)
            rgb.from_vector(self.leds.pixels[unit])
            return Response(rgb.as_dict(), 200)
        else:
            return Response({"error": "This LED is not connected"}, 404)

    def router(self, request: Request):

        if request.path in self.led_paths:
            if "POST" == request.method:
                return self.post_leds(request.body)
            elif "GET" == request.method:
                return self.get_leds()
        elif self.led_path_regex.match(request.path):
            led_match = self.led_path_regex.match(request.path)
            led = int(led_match.group(1))
            if "POST" == request.method:
                return self.post_leds(request.body, unit=led)
            elif "GET" == request.method:
                return self.get_leds(unit=led)
        elif request.path in self.len_paths:
            if "GET" == request.method:
                return self.get_strip()
        elif request.path in self.animation_paths:
            if "POST" == request.method:
                return self.post_animation(request.body)
            elif "GET" == request.method:
                return self.get_animation()
        return Response(
            {
                "error": "Not supported combination of method and path {} :: {}".format(
                    request.method, request.path
                )
            },
            501,
        )

    def handle(self, request: Request):
        if request is None:
            return Response(
                {
                    "error": "I did not understand you!",
                },
                505,
            )
        return self.router(request)
