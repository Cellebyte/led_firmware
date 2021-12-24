import json
from typing import Optional

import ure
from apiserver.handlers.base_handler import BaseHandler
from apiserver.response import Response
from driver.led import LEDDriver
from errors import BODY_MISSING, EXCEPTION_ERROR
from objects.animation import Animation
from webserver.http import Request


class AnimationHandler(BaseHandler):
    paths = ["/animation", "/animation/"]
    path_regex = ure.compile("/animation/({})/?".format("|".join(Animation.SUPPORTED)))

    def __init__(self, leds: LEDDriver) -> None:
        self.leds = leds

    def get_animations_options(self, animation: Animation) -> Response:
        return Response.from_dict(
            self.leds.animations[animation].as_dict(),
            200,
        )

    def put_animations_options(self, body, animation: Animation) -> Response:
        if not body:
            return Response.from_dict(*BODY_MISSING)
        try:
            return Response.from_dict(
                self.leds.animations[animation].update(json.loads(body)).as_dict(),
                200,
            )
        except (ValueError, TypeError) as e:
            return Response.from_dict(*EXCEPTION_ERROR(e))

    def post_animation(self, body: str) -> Response:
        if not body:
            return Response.from_dict(*BODY_MISSING)
        try:
            animation = Animation.from_dict(json.loads(body))
            self.leds.animation = animation
            return Response.from_dict(animation.as_dict(), 201)
        except (ValueError, TypeError) as e:
            return Response.from_dict(*EXCEPTION_ERROR(e))

    def get_animation(self) -> Response:
        return Response.from_dict(self.leds.animation.as_dict(), 200)

    def router(self, request: Request) -> Optional[Response]:
        if request.path in self.paths:
            if "POST" == request.method:
                return self.post_animation(request.body)
            elif "GET" == request.method:
                return self.get_animation()
        elif match := self.path_regex.match(request.path):
            animation = Animation(animation=str(match.group(1)))
            try:
                if "GET" == request.method:
                    return self.get_animations_options(animation=animation)
                elif "PUT" == request.method:
                    return self.put_animations_options(
                        request.body, animation=animation
                    )
            except KeyError as e:
                Response.from_dict(*EXCEPTION_ERROR(e))
        return None
