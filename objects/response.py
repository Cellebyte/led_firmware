import json


class Response:
    def __init__(self, body, code) -> None:
        self.code = code
        self.body = body

    def from_dict(self, body, code) -> 'Response':
        self.code = code
        self.body = body
        return self

    def __str__(self):
        return json.dumps(self.body)
