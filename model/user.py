from datetime import datetime
from typing import Optional
from enum import IntEnum, unique
from sqlalchemy.orm import Mapped, mapped_column
from pydantic import BaseModel, Field

from model.base import Base


class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[Optional[str]] = mapped_column(comment="名字")
    age: Mapped[Optional[int]] = mapped_column(comment="年龄")
    sex: Mapped[Optional[int]] = mapped_column(comment="性别")
    create_time: Mapped[datetime] = mapped_column(default=datetime.now, comment="创建时间")
    update_time: Mapped[datetime] = mapped_column(default=datetime.now, onupdate=datetime.now, comment="更新时间")


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
