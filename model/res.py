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


# 基础结果类
class StdResData(BaseModel):
    code: int
    message: str
    type: str
    data: Any = None


# 标准结果
class StdEntityRes(StdResData, Generic[T]):
    type: str = StdDataType.entity.value
    data: EntityData = EntityData()

    @classmethod
    def create(cls, code: int, message: str, entity: T):
        return cls(
            code=code,
            message=message,
            data=EntityData(entity=entity),
        )


# 列表结果
class StdListRes(StdResData, Generic[T]):
    type: str = StdDataType.list.value
    data: ListData = ListData()

    @classmethod
    def create(cls, code: int, message: str, list: List[T]):
        return cls(code=code, message=message, data=ListData(list=list))


# 分页列表结果
class StdPagingListRes(StdResData, Generic[T]):
    type: str = StdDataType.page_list.value
    data: PageListData = PageListData()

    @classmethod
    def create(
        cls,
        code: int,
        message: str,
        list: List[T],
        totalCount: int,
    ):
        return cls(
            code=code,
            message=message,
            data=PageListData(list=list, totalCount=totalCount),
        )


# 简易结果
class StdSimpleRes(StdResData):
    type: str = StdDataType.simple.value

    @classmethod
    def create(cls, code: int, message: str):
        return cls(code=code, message=message)


# 错误结果
class StdErrorRes(StdResData):
    type: str = StdDataType.error.value

    @classmethod
    def create(cls, code: int, message: str):
        return cls(code=code, message=message)
