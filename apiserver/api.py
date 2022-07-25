from webserver.http import Request

from apiserver.handlers.base_handler import BaseHandler
from apiserver.response import Response


class API:
    headers = {
        "Content-Type": "application/json",
        "Access-Control-Allow-Headers": "Content-Type",
        "Access-Control-Allow-Methods": "DELETE",
    }

    def __init__(self) -> None:
        self.handler = {}

    def register_handler(self, handler: BaseHandler):
        assert isinstance(handler, BaseHandler)
        self.handler[handler.paths[0]] = handler

    def router(self, request: Request) -> Response:
        response = None
        if "Origin" in request.headers.keys():
            self.headers.update(
                {"Access-Control-Allow-Origin": request.headers["Origin"]}
            )
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
                    ),
                    "code": 501,
                },
                501,
                headers=self.headers,
            )
        response.headers.update(self.headers)
        return response

    def handle(self, request: Request) -> Response:
        if request is None:
            return Response(
                {"error": "HTTP 1.1 only supported.", "code": 505},
                505,
            )
        return self.router(request)
