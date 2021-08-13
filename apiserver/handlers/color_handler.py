from apiserver.handlers.base_handler import BaseHandler
from driver.color_store import ColorStore
from webserver.http import Request
from errors import ALL_UNSUPPORTED
from objects.response import Response
import ure


class ColorHandler(BaseHandler):
    paths = ["/colors", "/colors/"]
    path_regex = ure.compile("/colors/(\d+)/?")

    def __init__(self, color_store: ColorStore) -> None:
        self.color_store = color_store

    def get_colors(self, slot=None) -> Response:
        if slot is None:
            return self.response.from_dict(*ALL_UNSUPPORTED)
        else:
            color = self.color_store[slot]
            return self.response.from_dict(color.as_dict() if color else color, 200)

    def post_colors(self, body, slot=None):
        raise NotImplementedError()

    def delete_colors(self, slot=None):
        raise NotImplementedError()

    def router(self, request: Request) -> Response:
        if request.path in self.paths:
            if "GET" == request.method:
                return self.get_colors()
            elif "DELETE" == request.method:
                return self.delete_colors()
        elif match := self.path_regex.match(request.path):
            slot = int(match.group(1))
            if "GET" == request.method:
                return self.get_colors(slot=slot)
            elif "POST" == request.method:
                return self.post_colors(request.body, slot=slot)
            elif "DELETE" == request.method:
                return self.delete_colors(slot=slot)
        return None
