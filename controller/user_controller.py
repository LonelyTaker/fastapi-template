import logging
from fastapi import APIRouter, Request, Depends

from lib.logging_helper import LoggingHelper
from lib.mysql_helper import MysqlHelper

from model import BaseRes, BaseError, ErrorCode
from model.user import UserAddReq, UserDelReq, UserUpdateReq, UserListReq
from sql import user_dao

logger = logging.getLogger()
router = APIRouter(prefix=f'/user', tags=['用户相关接口'])


@router.post("/add", response_model=BaseRes)
@LoggingHelper.log_request
async def add(request: Request, payload: UserAddReq, session=Depends(MysqlHelper.depends_async_session)):
    try:
        await user_dao.add_one(session, {
            "name": payload.name,
            "age": payload.age,
            "sex": payload.sex.value
        })
    except Exception as e:
        logger.error(str(e))
        raise BaseError(*ErrorCode.UserAddError.value, scene="add")

    return {
        "code": ErrorCode.Ok.value[0],
        "msg": ErrorCode.Ok.value[1]
    }


@router.post("/delete", response_model=BaseRes)
@LoggingHelper.log_request
async def delete(request: Request, payload: UserDelReq, session=Depends(MysqlHelper.depends_async_session)):
    try:
        await user_dao.del_by_id(session, payload.userId)
    except Exception as e:
        logger.error(str(e))
        raise BaseError(*ErrorCode.UserDelError.value, scene="delete")

    return {
        "code": ErrorCode.Ok.value[0],
        "msg": ErrorCode.Ok.value[1]
    }


@router.post("/update", response_model=BaseRes)
@LoggingHelper.log_request
async def update(request: Request, payload: UserUpdateReq, session=Depends(MysqlHelper.depends_async_session)):
    data = {}
    if payload.name is not None:
        data['name'] = payload.name
    if payload.age is not None:
        data['age'] = payload.age
    if payload.sex is not None:
        data['sex'] = payload.sex.value

    try:
        await user_dao.update_by_id(session, payload.userId, data)
    except Exception as e:
        logger.error(str(e))
        raise BaseError(*ErrorCode.UserUpdateError.value, scene="update")

    return {
        "code": ErrorCode.Ok.value[0],
        "msg": ErrorCode.Ok.value[1]
    }


@router.post("/list", response_model=BaseRes)
@LoggingHelper.log_request
async def get_list(request: Request, payload: UserListReq, session=Depends(MysqlHelper.depends_async_session)):
    try:
        query_total, query_list = await user_dao.get_list(session, payload)
    except Exception as e:
        logger.error(str(e))
        raise BaseError(*ErrorCode.UserListError.value, scene="get_list")

    return {
        "code": ErrorCode.Ok.value[0],
        "msg": ErrorCode.Ok.value[1],
        "data": {
            "total": query_total,
            "list": [{
                "id": row.id,
                "name": row.name,
                "age": row.age,
                "sex": row.sex
            } for row in query_list]
        }
    }
