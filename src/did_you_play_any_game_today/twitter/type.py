import typing
from pydantic import BaseModel

T = typing.TypeVar('T')


class ResponseData(typing.Generic[T], BaseModel):
    data: T
