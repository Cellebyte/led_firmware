from apiserver.util import code_to_message
import json


class Response:
    def __init__(self, body, code) -> None:
        self.code = code
        self.body = body
        self.message = code_to_message(code)

    def __str__(self):
        return json.dumps(self.body)
