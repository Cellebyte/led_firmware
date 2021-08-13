from apiserver.handlers.base_handler import BaseHandler
from driver.led import LEDDriver
from webserver.http import Request
from errors import BODY_MISSING, EXCEPTION_ERROR
from objects.response import Response
import ure
import json
from objects.animation import Animation


class AnimationHandler(BaseHandler):
    paths = ["/animation", "/animation/"]
    path_regex = ure.compile("/animation/({})/?".format("|".join(Animation.SUPPORTED)))

    def __init__(self, leds: LEDDriver) -> None:
        self.leds = leds

    def get_animations_options(self, animation: Animation) -> Response:
        return self.response.from_dict(
            self.leds.animations[animation].as_dict(),
            200,
        )

    def put_animations_options(self, body, animation: Animation) -> Response:
        if not body:
            return self.response.from_dict(*BODY_MISSING)
        try:
            return self.response.from_dict(
                self.leds.animations[animation].update(json.loads(body)).as_dict(),
                200,
            )
        except (ValueError, TypeError) as e:
            return self.response.from_dict(*EXCEPTION_ERROR(e))

    def post_animation(self, body: dict) -> Response:
        if not body:
            return self.response.from_dict(*BODY_MISSING)
        try:
            animation = Animation(**(json.loads(body)))
            self.leds.animation = animation
            return self.response.from_dict(animation.as_dict(), 201)
        except (ValueError, TypeError) as e:
            return self.response.from_dict(*EXCEPTION_ERROR(e))

    def get_animation(self) -> Response:
        return self.response.from_dict(self.leds.animation.as_dict(), 200)

    def router(self, request: Request) -> Response:
        if request.path in self.paths:
            if "POST" == request.method:
                return self.post_animation(request.body)
            elif "GET" == request.method:
                return self.get_animation()
        elif match := self.path_regex.match(request.path):
            animation = Animation(animation=str(match.group(1)))
            if "GET" == request.method:
                return self.get_animations_options(animation=animation)
            elif "PUT" == request.method:
                return self.put_animations_options(request.body, animation=animation)
        return None
