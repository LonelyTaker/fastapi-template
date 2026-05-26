from pydantic import BaseModel, Field


# 用户登录请求参数校验
class LoginReq(BaseModel):
    account: str = Field(...)
    password: str = Field(...)
