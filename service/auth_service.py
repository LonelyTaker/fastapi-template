import jwt
from datetime import datetime, timedelta
from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from lib.configure import Configure
from lib.logging import logger
from lib.mysql import MysqlHelper

# from lib.redis import RedisHelper

from model.base import StdError, ErrorCode

from sql import AccountDao

security = HTTPBearer()

"""
    如果接入redis，用户token应存入redis
    当前存入全局环境并不合理，仅用于示例
"""
account_token_map = {}


class AuthService:
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
            "exp": datetime.utcnow()
            + timedelta(seconds=Configure.get("token", "expiration")),  # 过期时间
        }
        return jwt.encode(data, Configure.get("token", "secret_key"), algorithm="HS256")

    @classmethod
    def decode_token(cls, token) -> dict:
        """
        解析token
        :param token: token
        :return: 解析后信息
        """
        try:
            payload = jwt.decode(
                token, Configure.get("token", "secret_key"), algorithms=["HS256"]
            )
            logger.info(f"token解析信息：{payload}")
            return payload
        except jwt.ExpiredSignatureError:  # token已过期
            raise StdError(*ErrorCode.TokenExpError.value)
        except jwt.InvalidTokenError:  # 无效token
            raise StdError(*ErrorCode.TokenError.value)

    @classmethod
    def del_token(cls, uid):
        """
        删除token
        :param uid: 用户id
        """
        # RedisHelper.delete(uid)
        try:
            del account_token_map[uid]
        except Exception:
            pass

    @classmethod
    def get_token(cls, uid) -> str | None:
        """
        获取token
        :param uid: 用户id
        :return: token
        """
        # return RedisHelper.get(uid)
        # 判断是否过期（非线程安全）
        _temp = account_token_map.get(uid)
        if _temp:
            if _temp.get("exp") > datetime.utcnow().timestamp():
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
            "exp": datetime.utcnow().timestamp() + Configure.get("token", "expiration"),
        }

    @classmethod
    async def check_token(cls, token):
        """
        校验token
        :param token: token
        :return: 校验通过返回用户信息
        """
        if not token:
            raise StdError(*ErrorCode.TokenError.value)

        _json = cls.decode_token(token)
        _uid = _json.get("uid")
        if not _uid:
            raise StdError(*ErrorCode.TokenError.value)

        # 查找token
        _token = cls.get_token(_uid)
        if not _token:
            raise StdError(*ErrorCode.TokenExpError.value)
        elif _token != token:
            raise StdError(*ErrorCode.TokenError.value)

        # 查找用户信息
        async with MysqlHelper.get_async_connection() as conn:
            account = await AccountDao.get_by_id(conn, _uid)

        if not account:
            raise StdError(*ErrorCode.TokenError.value)

        return account


# 接口依赖注入（获取用户信息）
async def get_user_info(
    authorization: HTTPAuthorizationCredentials = Depends(security),
):
    token = authorization.credentials
    logger.info(f"{token=}")
    return await AuthService.check_token(token)
