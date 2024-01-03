import logging
import jwt
from datetime import datetime, timedelta
from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from lib.mysql_helper import MysqlHelper
# from lib.redis_helper import RedisHelper

from model import BaseError, ErrorCode
from model.account import Account
from sql import account_dao
from setting import TOKEN_SECRET_KEY, TOKEN_EXPIRATION

security = HTTPBearer()
logger = logging.getLogger()

"""
    如果接入redis，用户token应存入redis
    当前存入全局环境并不合理，仅用于示例
"""
account_token_map = {}


class AuthService(object):
    @classmethod
    def create_token(cls, uid, payload) -> str:
        """
        创建token
        :param uid: 用户id
        :param payload: 其他信息
        :return: token
        """
        data = {
            "uid": uid,
            **payload,
            "exp": datetime.utcnow() + timedelta(seconds=TOKEN_EXPIRATION)  # 过期时间
        }
        return jwt.encode(data, TOKEN_SECRET_KEY, algorithm="HS256")

    @classmethod
    def decode_token(cls, token) -> dict:
        """
        解析token
        :param token: token
        :return: 解析后信息
        """
        try:
            payload = jwt.decode(token, TOKEN_SECRET_KEY, algorithms=["HS256"])
            logger.info(f'token解析信息：{payload}')
            return payload
        except jwt.ExpiredSignatureError:  # token已过期
            raise BaseError(code=ErrorCode.TokenExpError.value[0], msg=ErrorCode.TokenExpError.value[1], scene="decode_token")
        except jwt.InvalidTokenError:  # 无效token
            raise BaseError(code=ErrorCode.TokenError.value[0], msg=ErrorCode.TokenError.value[1], scene="decode_token")

    @classmethod
    def del_token(cls, uid):
        """
        删除token
        :param uid: 用户id
        """
        # RedisHelper.delete(uid)
        del account_token_map[uid]

    @classmethod
    def get_token(cls, uid) -> str:
        """
        获取token
        :param uid: 用户id
        :return: token
        """
        # return RedisHelper.get(uid)
        # 判断是否过期
        _temp = account_token_map.get(uid)
        if _temp:
            if _temp.get("exp") < datetime.utcnow().timestamp():
                return _temp.get("token")
            else:
                cls.del_token(uid)

    @classmethod
    def set_token(cls, uid, token):
        """
        设置token
        :param uid: 用户id
        :param token: token
        """
        # RedisHelper.set(uid, token, ex=TOKEN_EXPIRATION)
        account_token_map[uid] = {
            "token": token,
            "exp": TOKEN_EXPIRATION
        }

    @classmethod
    async def check_token(cls, token) -> Account:
        """
        校验token
        :param token: token
        :return: 校验通过返回用户信息
        """
        if not token:
            raise BaseError(code=ErrorCode.TokenError.value[0], msg=ErrorCode.TokenError.value[1], scene="check_token: no token")

        _json = cls.decode_token(token)
        _uid = _json.get("uid")
        if not _uid:
            raise BaseError(code=ErrorCode.TokenError.value[0], msg=ErrorCode.TokenError.value[1], scene="check_token: no uid")

        # 查找token
        _token = cls.get_token(_uid)
        if not _token:
            raise BaseError(code=ErrorCode.TokenExpError.value[0], msg=ErrorCode.TokenExpError.value[1], scene="check_token: redis no token")
        elif _token != token:
            raise BaseError(code=ErrorCode.TokenError.value[0], msg=ErrorCode.TokenError.value[1], scene="check_token: token is not same")

        # 查找用户信息
        async with MysqlHelper.get_async_session() as session:
            account = await account_dao.get_by_id(session, _uid)

        if not account:
            raise BaseError(code=ErrorCode.TokenError.value[0], msg=ErrorCode.TokenError.value[1], scene="check_token: account not exist")

        return account


# 接口依赖注入（获取用户信息）
async def get_user_info(authorization: HTTPAuthorizationCredentials = Depends(security)) -> Account:
    token = authorization.credentials
    logger.info(f'{token=}')
    return await AuthService.check_token(token)
