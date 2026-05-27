from pydantic import BaseModel, Field
from typing import Optional, List, Any, TypeVar, Generic
from enum import Enum, unique

T = TypeVar("T")


@unique
class StdDataType(Enum):
    Entity = "EntityData"
    List = "ListData"
    PageList = "PageListData"
    Simple = "SimpleData"
    Error = "ErrorData"


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
    type: str = Field(default=StdDataType.Entity.value, description="响应类型")
    data: EntityData = Field(default_factory=EntityData, description="响应数据")

    @classmethod
    def create(cls, code: int, message: str, entity: T | None = None):
        return cls(
            code=code,
            message=message,
            data=EntityData(entity=entity),
        )


# 列表结果
class StdListRes(StdResData, Generic[T]):
    type: str = Field(default=StdDataType.List.value, description="响应类型")
    data: ListData = Field(default_factory=ListData, description="响应数据")

    @classmethod
    def create(cls, code: int, message: str, list: List[T]):
        return cls(code=code, message=message, data=ListData(list=list))


# 分页列表结果
class StdPagingListRes(StdResData, Generic[T]):
    type: str = Field(default=StdDataType.PageList.value, description="响应类型")
    data: PageListData = Field(default_factory=PageListData, description="响应数据")

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
    type: str = Field(default=StdDataType.Simple.value, description="响应类型")

    @classmethod
    def create(cls, code: int, message: str):
        return cls(code=code, message=message)


# 错误结果
class StdErrorRes(StdResData):
    type: str = Field(default=StdDataType.Error.value, description="响应类型")

    @classmethod
    def create(cls, code: int, message: str):
        return cls(code=code, message=message)
