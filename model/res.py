from pydantic import BaseModel
from typing import List, Any, TypeVar, Generic
from enum import Enum, unique

T = TypeVar("T")


@unique
class StdDataType(Enum):
    entity = "EntityData"
    list = "ListData"
    page_list = "PageListData"
    simple = "SimpleData"
    error = "ErrorData"


# 定义各类型的 data 模型（泛型）
class EntityData(BaseModel, Generic[T]):
    entity: T | None = None


class ListData(BaseModel, Generic[T]):
    list: List[T] = []


class PageListData(BaseModel, Generic[T]):
    list: List[T] = []
    totalCount: int = 0


class SimpleData(BaseModel):
    message: str | None = None


class ErrorData(BaseModel):
    message: str | None = None


# 基础结果类
class StdResData(BaseModel):
    code: int
    message: str
    type: str
    data: Any = None


class StdEntityRes(StdResData, Generic[T]):
    type: str = StdDataType.entity.value
    data: EntityData = EntityData()

    @classmethod
    def create(cls, code: int, message: str, entity: T | None = None):
        return cls(
            code=code,
            message=message,
            data=EntityData(entity=entity),
        )


class StdListRes(StdResData, Generic[T]):
    type: str = StdDataType.list.value
    data: ListData = ListData()

    @classmethod
    def create(cls, code: int, message: str, list: List[T] | None = None):
        return cls(code=code, message=message, data=ListData(list=list or []))


class StdPagingListRes(StdResData, Generic[T]):
    type: str = StdDataType.page_list.value
    data: PageListData = PageListData()

    @classmethod
    def create(
        cls,
        code: int,
        message: str,
        list: List[T] | None = None,
        totalCount: int = 0,
    ):
        return cls(
            code=code,
            message=message,
            data=PageListData(list=list or [], totalCount=totalCount),
        )


class StdSimpleRes(StdResData):
    type: str = StdDataType.simple.value
    data: SimpleData = SimpleData()

    @classmethod
    def create(cls, code: int, message: str):
        return cls(code=code, message=message, data=SimpleData(message=message))


class StdErrorRes(StdResData):
    type: str = StdDataType.error.value
    data: ErrorData = ErrorData()

    @classmethod
    def create(cls, code: int, message: str):
        return cls(code=code, message=message, data=ErrorData(message=message))
