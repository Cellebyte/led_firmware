import json
from . import util


class Response:
    def __init__(self, body, code) -> None:
        self.code = code
        self.body = body
        self.message = util.code_to_message(code)

    def __str__(self):
        return json.dumps(self.body)


class APIServer:
    def __init__(self, led) -> None:
        self.led = led

    def loop(self, request):
        if request is None:
            return Response({}, 505)
        return Response(json.loads(request.body), 201)
