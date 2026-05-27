from pydantic import BaseModel, Field


# 用户登录请求参数校验
class LoginReq(BaseModel):
    account: str = Field(..., max_length=100, description="登录账号")
    password: str = Field(..., min_length=6, max_length=32, description="登录密码")
