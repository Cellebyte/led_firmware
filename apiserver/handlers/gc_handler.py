from collections import OrderedDict
from typing import Optional

from apiserver.handlers.base_handler import BaseHandler
from apiserver.response import Response
from driver.util import gc_info
from webserver.http import Request


class GCHandler(BaseHandler):
    paths = ["/gc", "/gc/"]

    def router(self, request: Request) -> Optional[Response]:
        if request.path in self.paths:
            if "GET" == request.method:
                gc_info()
                return Response.from_dict({}, 200)
        return None
