import json

import ure
from driver.led import LEDDriver
from webserver.http import Request

from errors import BODY_MISSING, EXCEPTION_ERROR

from objects.animation import Animation
from objects.response import Response
from objects.rgb import RGB


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
            return Response(BODY_MISSING)
        try:
            return Response(
                self.leds.animations[animation].update(json.loads(body)).as_dict(), 200
            )
        except (ValueError, TypeError) as e:
            return Response(EXCEPTION_ERROR(e))

    def post_animation(self, body: dict):
        if not body:
            return Response(BODY_MISSING)
        try:
            animation = Animation(**(json.loads(body)))
            self.leds.animation = animation
        except (ValueError, TypeError) as e:
            return Response(EXCEPTION_ERROR(e))
        return Response(animation.as_dict(), 201)

    def get_animation(self):
        return Response(
            self.leds.animation.as_dict(),
            200,
        )

    def post_leds(self, body, unit=None):
        if not body:
            return Response(BODY_MISSING)
        try:
            rgb = RGB(**(json.loads(body)))
        except (ValueError, TypeError) as e:
            return Response(EXCEPTION_ERROR(e))
        # If the led endpoint is used controller gets forced to manual mode
        self.leds.animation = Animation("manual")
        if unit is None:
            self.leds.set_all(rgb)
        else:
            self.leds.set(rgb, unit)
        return Response(rgb.as_dict(), 201)

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

    def get_strip(self):
        return Response(
            {
                "last": self.leds.len_leds - 1,
                "first": 0,
            },
            200,
        )

    def get_colors(self, slot=None):
        raise NotImplementedError()

    def post_colors(self, body, slot=None):
        raise NotImplementedError()

    def delete_colors(slot=None):
        raise NotImplementedError()

    def router(self, request: Request):
        from webserver.constants import METHOD_DELETE, METHOD_GET, METHOD_POST, METHOD_PUT
        if request.path in self.led_paths:
            if METHOD_POST == request.method:
                return self.post_leds(request.body)
            elif METHOD_GET == request.method:
                return self.get_leds()
        elif self.led_path_regex.match(request.path):
            led_match = self.led_path_regex.match(request.path)
            led = int(led_match.group(1))
            if METHOD_POST == request.method:
                return self.post_leds(request.body, unit=led)
            elif METHOD_GET == request.method:
                return self.get_leds(unit=led)
        elif request.path in self.len_paths:
            if METHOD_GET == request.method:
                return self.get_strip()
        elif request.path in self.animation_paths:
            if METHOD_POST == request.method:
                return self.post_animation(request.body)
            elif METHOD_GET == request.method:
                return self.get_animation()
        elif self.animation_path_regex.match(request.path):
            animation_match = self.animation_path_regex.match(request.path)
            animation = Animation(animation=str(animation_match.group(1)))
            if METHOD_GET == request.method:
                return self.get_animations_options(animation=animation)
            elif METHOD_PUT == request.method:
                return self.put_animations_options(request.body, animation=animation)
        elif request.path in self.color_paths:
            if METHOD_GET == request.method:
                return self.get_colors()
            elif METHOD_DELETE == request.method:
                return self.delete_colors()
        elif self.color_path_regex(request.path):
            color_slot_match = self.color_path_regex.match(request.path)
            color_slot = color_slot_match.group(1)
            if METHOD_GET == request.method:
                return self.get_colors(slot=color_slot)
            elif METHOD_POST == request.method:
                return self.post_colors(request.body, slot=color_slot)
            elif METHOD_DELETE == request.method:
                return self.delete_colors(slot=color_slot)

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
                    "error": "HTTP 1.1 only supported.",
                },
                505,
            )
        return self.router(request)
