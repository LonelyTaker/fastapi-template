from pydantic import BaseModel, Field
from typing import Optional, List, Any, TypeVar, Generic
from enum import Enum, unique

from .error import ErrorCode

T = TypeVar("T")


@unique
class StdDataType(Enum):
    Entity = "EntityData"
    List = "ListData"
    PageList = "PageListData"
    Simple = "SimpleData"
    Error = "ErrorData"


# 结果基础类
class StdRes(BaseModel):
    type: StdDataType = Field(..., description="响应类型")
    code: int = Field(default=ErrorCode.Ok.code, description="状态码")
    message: str = Field(default=ErrorCode.Ok.msg, description="提示信息")
    data: Optional[Any] = Field(default=None, description="响应数据")


# 标准结果
class EntityData(BaseModel, Generic[T]):
    entity: Optional[T] = Field(default=None, description="实体对象")


class StdEntityRes(StdRes, Generic[T]):
    type: StdDataType = Field(default=StdDataType.Entity, description="响应类型")
    data: EntityData = Field(default_factory=EntityData, description="响应数据")

    @classmethod
    def create(cls, entity: T | None = None):
        return cls(
            data=EntityData(entity=entity),
        )


# 列表结果
class ListData(BaseModel, Generic[T]):
    list: List[T] = Field(default_factory=list, description="列表数据")


class StdListRes(StdRes, Generic[T]):
    type: StdDataType = Field(default=StdDataType.List, description="响应类型")
    data: ListData = Field(default_factory=ListData, description="响应数据")

    @classmethod
    def create(cls, list: List[T]):
        return cls(data=ListData(list=list))


# 分页列表结果
class PageListData(BaseModel, Generic[T]):
    list: List[T] = Field(default_factory=list, description="列表数据")
    totalCount: int = Field(default=0, description="总记录数")


class StdPagingListRes(StdRes, Generic[T]):
    type: StdDataType = Field(default=StdDataType.PageList, description="响应类型")
    data: PageListData = Field(default_factory=PageListData, description="响应数据")

    @classmethod
    def create(
        cls,
        list: List[T],
        totalCount: int,
    ):
        return cls(data=PageListData(list=list, totalCount=totalCount))


# 简易结果
class StdSimpleRes(StdRes):
    type: StdDataType = Field(default=StdDataType.Simple, description="响应类型")


# 错误结果
class StdErrorRes(StdRes):
    type: StdDataType = Field(default=StdDataType.Error, description="响应类型")
    code: int = Field(default=ErrorCode.UnexpectedError.code, description="状态码")
    message: str = Field(default=ErrorCode.UnexpectedError.msg, description="提示信息")
