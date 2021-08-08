import json


class Response:
    def __init__(self, body, code) -> None:
        self.code = code
        self.body = body

    def __str__(self):
        return json.dumps(self.body)
