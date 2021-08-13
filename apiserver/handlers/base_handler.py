from objects.response import Response
from webserver.http import Request
from errors import IMPLEMENTATION_NEEDED


class BaseHandler:
    response = Response({}, 200)

    def router(self, request: Request) -> Response:
        raise NotImplementedError(IMPLEMENTATION_NEEDED)
