from sqlalchemy.orm import DeclarativeBase
from pydantic import BaseModel
from typing import Any


# ORM基础类
class Base(DeclarativeBase):
    pass


# 基础结果类
class BaseRes(BaseModel):
    code: int
    msg: str
    data: Any = None
