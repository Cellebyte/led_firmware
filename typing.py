typings = False
Union = None
Optional = None
Any = None
Tuple = None

try:
    import typing

    typings = True
except ImportError:
    pass

if typings:
    # This is needed to mock typings for execution on the micropython kernel.
    Union = typing.Union
    Optional = typing.Optional
    Any = typing.Any
    Tuple = typing.Tuple
else:

    class Mock:
        pass

    Union = Mock
    Optional = Mock
    Any = Mock
    Tuple = Mock

Union = Union
Optional = Optional
Any = Any
Tuple = Tuple
