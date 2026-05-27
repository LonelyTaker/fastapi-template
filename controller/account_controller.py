from fastapi import APIRouter, Request, Depends

from lib.logging import LoggingHelper, logger
from lib.mysql import MysqlHelper

from model.res import StdEntityRes, StdSimpleRes
from model.error import StdError, ErrorCode
from model.schema.account import LoginReq

from service import AuthService, get_user_info

from sql import AccountDao

router = APIRouter(prefix=f"/account", tags=["账号相关接口"])


@router.post("/login", response_model=StdEntityRes)
@LoggingHelper.log_request
async def login(
    request: Request,
    payload: LoginReq,
    conn=Depends(MysqlHelper.depends_async_connection),
):
    account_info = await AccountDao.get_by_account(conn, payload.account)
    if not account_info:
        raise StdError(*ErrorCode.AccountNotFountError.value)

    if account_info.get("password") != payload.password:
        raise StdError(*ErrorCode.AccountPwdError.value)

    # 创建token
    token = AuthService.create_token(account_info["id"], {})
    # 存储token
    AuthService.set_token(account_info["id"], token)

    return StdEntityRes.create(*ErrorCode.Ok.value, {"userInfo": {}, "token": token})


@router.get("/test", response_model=StdSimpleRes)
@LoggingHelper.log_request
async def test(request: Request, user_info=Depends(get_user_info)):
    logger.info(user_info)
    return StdSimpleRes.create(*ErrorCode.Ok.value)
