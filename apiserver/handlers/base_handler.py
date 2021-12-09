from typing import Optional

from errors import IMPLEMENTATION_NEEDED
from objects.response import Response
from webserver.http import Request


class BaseHandler:
    paths = ["/"]
    response = Response({}, 200)

    def router(self, request: Request) -> Optional[Response]:
        raise NotImplementedError(IMPLEMENTATION_NEEDED)
