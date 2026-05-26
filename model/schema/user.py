from pydantic import BaseModel, Field
from enum import IntEnum, unique


@unique
class Sex(IntEnum):
    woman = 0
    man = 1


# 用户新增请求参数校验
class UserAddReq(BaseModel):
    name: str = Field(..., max_length=50)
    age: int | None = Field(None)
    sex: Sex | None = Field(None)


# 用户删除请求参数校验
class UserDelReq(BaseModel):
    userId: int = Field(...)


# 用户更新请求参数校验
class UserUpdateReq(BaseModel):
    userId: int = Field(...)
    name: str | None = Field(None, max_length=50)
    age: int | None = Field(None)
    sex: Sex | None = Field(None)


# 用户查询请求参数校验
class UserListReq(BaseModel):
    pageNo: int = Field(..., ge=1)
    pageSize: int = Field(..., ge=1)
