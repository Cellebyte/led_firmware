from objects.response import Response
from webserver.http import Request

from apiserver.handlers.base_handler import BaseHandler


class API:
    def __init__(self) -> None:
        self.handler = {}

    def register_handler(self, handler: BaseHandler):
        assert isinstance(handler, BaseHandler)
        self.handler[handler.paths[0]] = handler

    def router(self, request: Request) -> Response:
        response = None
        for path in self.handler.keys():
            if request.path.startswith(path):
                response = self.handler[path].router(request)
            else:
                continue
        if response is None:
            return Response(
                {
                    "error": "METHOD {} :: PATH {} unsupported!".format(
                        request.method, request.path
                    )
                },
                501,
            )
        return response

    def handle(self, request: Request) -> Response:
        if request is None:
            return Response(
                {
                    "error": "HTTP 1.1 only supported.",
                },
                505,
            )
        return self.router(request)
