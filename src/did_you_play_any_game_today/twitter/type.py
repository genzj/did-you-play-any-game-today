import typing

T = typing.TypeVar('T')


class ResponseData(typing.Generic[T], typing.TypedDict):
    data: T
