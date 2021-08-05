import json

import ure
from driver.led import LEDDriver
from webserver.http import Request

from apiserver.constants import BODY_MISSING, EXCEPTION_ERROR
from .objects.response import Response
from .objects.animation import Animation
from .objects.rgb import RGB


class APIHandler:
    led_paths = ["/leds", "/leds/"]
    led_path_regex = ure.compile("/leds/(\d+)")
    len_paths = ["/lens", "/lens/"]
    color_paths = ["/colors", "/colors/"]
    color_path_regex = ure.compile("/colors/(\d+)/?")
    animation_paths = ["/animation", "/animation/"]
    animation_path_regex = ure.compile(
        "/animation/({})/?".format("|".join(Animation.SUPPORTED))
    )

    def __init__(self, leds) -> None:
        self.leds: LEDDriver = leds

    def get_animations_options(self, animation: Animation):
        return Response(self.leds.animations[animation].as_dict(), 200)

    def put_animations_options(self, body, animation: Animation):
        if not body:
            return BODY_MISSING
        try:
            return Response(
                self.leds.animations[animation].update(json.loads(body)).as_dict(), 200
            )
        except (ValueError, TypeError) as e:
            return EXCEPTION_ERROR(e)

    def post_animation(self, body: dict):
        if not body:
            return BODY_MISSING
        try:
            animation = Animation(**(json.loads(body)))
            self.leds.animation = animation
        except (ValueError, TypeError) as e:
            return EXCEPTION_ERROR(e)
        return Response(animation.as_dict(), 201)

    def get_animation(self):
        return Response(
            self.leds.animation.as_dict(),
            200,
        )

    def post_leds(self, body, unit=None):
        if not body:
            return BODY_MISSING
        try:
            rgb = RGB(**(json.loads(body)))
        except (ValueError, TypeError) as e:
            return EXCEPTION_ERROR(e)
        if unit is None:
            self.leds.set_all(rgb)
        else:
            # If a single LED gets set Move controller to manual mode
            self.leds.animation = Animation("manual")
            self.leds.set(rgb, unit)
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
        elif self.animation_path_regex.match(request.path):
            animation_match = self.animation_path_regex.match(request.path)
            animation = Animation(animation=str(animation_match.group(1)))
            if "GET" == request.method:
                return self.get_animations_options(animation=animation)
            elif "PUT" == request.method:
                return self.put_animations_options(request.body, animation=animation)

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
