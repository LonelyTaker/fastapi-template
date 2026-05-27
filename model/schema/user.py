from pydantic import BaseModel, Field
from typing import Optional
from enum import IntEnum, unique


@unique
class Sex(IntEnum):
    woman = 0
    man = 1


# 用户新增请求参数校验
class UserAddReq(BaseModel):
    name: str = Field(..., max_length=50, description="用户姓名")
    age: Optional[int] = Field(None, description="用户年龄")
    sex: Optional[Sex] = Field(None, description="用户性别：0-女，1-男")


# 用户删除请求参数校验
class UserDelReq(BaseModel):
    userId: int = Field(..., description="用户ID")


# 用户更新请求参数校验
class UserUpdateReq(BaseModel):
    userId: int = Field(..., description="用户ID")
    name: Optional[str] = Field(None, max_length=50, description="用户姓名")
    age: Optional[int] = Field(None, description="用户年龄")
    sex: Optional[Sex] = Field(None, description="用户性别：0-女，1-男")


# 用户查询请求参数校验
class UserListReq(BaseModel):
    pageNo: int = Field(..., ge=1, description="页码，从1开始")
    pageSize: int = Field(..., ge=1, description="每页数量")
