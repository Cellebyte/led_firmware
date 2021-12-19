import json

from errors import VALUE_NOT_OF_TYPE


class Response:
    def __init__(self, body: dict, code: int) -> None:
        self.code = code
        self.body = body

    @property
    def body(self) -> dict:
        return self._body

    @body.setter
    def body(self, value: dict):
        if not isinstance(value, dict):
            raise ValueError(
                VALUE_NOT_OF_TYPE(self.__class__.__name__, "body", value, dict)
            )
        self._body = value

    @property
    def code(self) -> int:
        return self._code

    @code.setter
    def code(self, value: int):
        if not isinstance(value, int):
            raise ValueError(
                VALUE_NOT_OF_TYPE(self.__class__.__name__, "code", value, int)
            )
        self._code = value

    @classmethod
    def from_dict(cls, body, code):
        return cls(body, code)

    def __str__(self):
        return json.dumps(self.body)
