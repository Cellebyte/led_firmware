from typing import Optional

from apiserver.handlers.base_handler import BaseHandler
from apiserver.response import Response
from driver.util import gc_info
from webserver.http import Request


class GCHandler(BaseHandler):
    paths = ["/api/v1/gc", "/api/v1/gc/"]

    def router(self, request: Request) -> Optional[Response]:
        if request.path in self.paths:
            if "GET" == request.method:
                gc_info()
                return Response.from_dict({}, 200)
            elif "OPTIONS" == request.method:
                return Response(body={}, code=200, headers=self.headers)
        return None
