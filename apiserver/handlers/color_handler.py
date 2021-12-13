from typing import Optional

import ure
import json
from apiserver.handlers.base_handler import BaseHandler
from driver import color_store
from driver.color_store import ColorStore
from errors import ALL_UNSUPPORTED, EXCEPTION_ERROR
from objects.response import Response
from objects.rgb import RGB
from webserver.http import Request


class ColorHandler(BaseHandler):
    paths = ["/colors", "/colors/"]
    path_regex = ure.compile("/colors/(\d+)/?")

    def __init__(self, color_store: ColorStore) -> None:
        self.color_store = color_store

    def get_colors(self, slot=None) -> Response:
        if slot is None:
            return self.response.from_dict(self.color_store.as_dict(), 200)
        else:
            color = self.color_store[slot]
            return self.response.from_dict(color.as_dict() if color else color, 200)

    def post_colors(self, body, slot=None):
        color = RGB.from_dict(json.loads(body))
        if slot is None:
            free_slot = None
            for key in self.color_store:
                if self.color_store[key] is None:
                    free_slot = key
                    break
            assert (
                free_slot is not None
            ), "The Color Store is full please define a slot to overwrite"
            self.color_store[free_slot] = color
        else:
            self.color_store[slot] = color
        return self.response.from_dict(color.as_dict(), 201)

    def delete_colors(self, slot=None):
        if slot is not None:
            color = self.color_store.delete(slot)
            if color is not None:
                return self.response.from_dict(color.as_dict(), 200)
            return None

    def router(self, request: Request) -> Optional[Response]:
        if request.path in self.paths:
            if "GET" == request.method:
                return self.get_colors()
            elif "POST" == request.method:
                return self.post_colors(request.body)
            elif "DELETE" == request.method:
                return self.delete_colors()
        elif match := self.path_regex.match(request.path):
            try:
                slot = int(match.group(1))
                if "GET" == request.method:
                    return self.get_colors(slot=slot)
                elif "POST" == request.method:
                    return self.post_colors(request.body, slot=slot)
                elif "DELETE" == request.method:
                    return self.delete_colors(slot=slot)
            except AssertionError as e:
                return self.response.from_dict(*EXCEPTION_ERROR(e))
        return None
