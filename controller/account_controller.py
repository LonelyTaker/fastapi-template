import logging
from fastapi import APIRouter, Request, Depends

from lib.logging_helper import LoggingHelper
from lib.mysql_helper import MysqlHelper

from model import BaseRes, BaseError, ErrorCode
from model.account import Account, LoginReq
from sql import account_dao
from service.auth_service import AuthService, get_user_info

logger = logging.getLogger()
router = APIRouter(prefix=f'/account', tags=['账号相关接口'])


@router.post("/login", response_model=BaseRes)
@LoggingHelper.log_request
async def delete(request: Request, payload: LoginReq, session=Depends(MysqlHelper.depends_async_session)):
    account_info = await account_dao.get_by_account(session, payload.account)
    if not account_info:
        raise BaseError(*ErrorCode.AccountNotFountError.value, scene="login")

    if account_info.password != payload.password:
        raise BaseError(*ErrorCode.AccountPwdError.value, scene="login")

    # 创建token
    token = AuthService.create_token(account_info.id, {})
    # 存储token
    AuthService.set_token(account_info.id, token)

    return {
        "code": ErrorCode.Ok.value[0],
        "msg": ErrorCode.Ok.value[1],
        "data": {
            "userInfo": {},
            "token": token
        }
    }


@router.get("/test", response_model=BaseRes)
@LoggingHelper.log_request
async def delete(request: Request, user_info: Account = Depends(get_user_info)):
    logger.info(user_info)
    return {
        "code": ErrorCode.Ok.value[0],
        "msg": ErrorCode.Ok.value[1]
    }
