from pydantic import BaseModel, Field
from typing import Optional, List, Any, TypeVar, Generic
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
    entity: Optional[T] = Field(default=None, description="实体对象")


class ListData(BaseModel, Generic[T]):
    list: List[T] = Field(default_factory=list, description="列表数据")


class PageListData(BaseModel, Generic[T]):
    list: List[T] = Field(default_factory=list, description="列表数据")
    totalCount: int = Field(default=0, description="总记录数")


# 基础结果类
class StdResData(BaseModel):
    code: int = Field(..., description="状态码")
    message: str = Field(..., description="提示信息")
    type: str = Field(..., description="数据类型")
    data: Optional[Any] = Field(default=None, description="响应数据")


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
