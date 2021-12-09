typings = False
Union = None
Optional = None
Any = None
try:
    import typing

    typings = True
except ImportError:
    pass


class Mock:
    pass


if typings:
    # This is needed to mock typings for execution on the micropython kernel.
    Union = typing.Union
    Optional = typing.Optional
    Any = typing.Any
else:
    Union = Mock
    Optional = Mock
    Any = Mock

Union = Union
Optional = Optional
Any = Any
