# Useful errors


def IS_REQUIRED(name: str) -> str:
    return "{} is required".format(name)


PUT_NOT_USEFUL = "Nothing useful provided for update!"
IMPLEMENTATION_NEEDED = "This function needs to be implemented by a Child Animation"
MISSING_STATE_FILE = "Cannot find state file {}"
ALL_UNSUPPORTED = ({"error": "All not supported.", "code": 501}, 501)
BODY_MISSING = ({"error": "Body needs to be provided!", "code": 400}, 400)


def EXCEPTION_ERROR(e: Exception):
    return {"error": "{}".format(e), "code": 400}, 400


def VALUE_NOT_IN_RANGE(cls: str, prefix: str, value, min: int, max: int):
    return "{} {} `{}` not in {} - {}".format(cls, prefix, value, min, max)


def VALUE_NOT_IN_LIST(cls: str, prefix: str, value, allowed_values: list):
    return "{} {} `{}` not in [{}]".format(
        cls, prefix, value, ", ".join(allowed_values)
    )


def VALUE_NOT_OF_TYPE(cls: str, prefix: str, value, allowed_type):
    return "{} {} value `{}` is of type {} should be an {}".format(
        cls, prefix, value, type(value), allowed_type
    )
