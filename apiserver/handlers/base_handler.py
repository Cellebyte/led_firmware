from typing import Optional

from apiserver.response import Response
from errors import IMPLEMENTATION_NEEDED
from webserver.http import Request


class BaseHandler:
    paths = ["/"]

    def router(self, request: Request) -> Optional[Response]:
        raise NotImplementedError(IMPLEMENTATION_NEEDED)
