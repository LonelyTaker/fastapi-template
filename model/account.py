from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from pydantic import BaseModel, Field

from model.base import Base


class Account(Base):
    __tablename__ = "account"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    account: Mapped[str] = mapped_column(unique=True, comment='账号')
    password: Mapped[str] = mapped_column(comment='密码')
    create_time: Mapped[datetime] = mapped_column(default=datetime.now, comment="创建时间")
    update_time: Mapped[datetime] = mapped_column(default=datetime.now, onupdate=datetime.now, comment="更新时间")


# 用户登录请求参数校验
class LoginReq(BaseModel):
    account: str = Field(...)
    password: str = Field(...)
