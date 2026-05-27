from fastapi import APIRouter, Request, Depends

from lib.logging import LoggingHelper, logger
from lib.mysql import MysqlHelper

from model.res import StdSimpleRes, StdPagingListRes
from model.error import StdError, ErrorCode
from model.schema.user import UserAddReq, UserDelReq, UserUpdateReq, UserListReq

from sql import UserDao

router = APIRouter(prefix=f"/user", tags=["用户相关接口"])


@router.post("/add", response_model=StdSimpleRes)
@LoggingHelper.log_request
async def add(
    request: Request,
    payload: UserAddReq,
    conn=Depends(MysqlHelper.depends_async_connection),
):
    try:
        await UserDao.add_one(
            conn,
            {
                "name": payload.name,
                "age": payload.age,
                "sex": payload.sex.value if payload.sex is not None else None,
            },
        )
        await conn.commit()
    except Exception as e:
        logger.error(str(e))
        raise StdError(*ErrorCode.UserAddError.value)

    return StdSimpleRes.create(*ErrorCode.Ok.value)


@router.post("/delete", response_model=StdSimpleRes)
@LoggingHelper.log_request
async def delete(
    request: Request,
    payload: UserDelReq,
    conn=Depends(MysqlHelper.depends_async_connection),
):
    try:
        await UserDao.del_by_id(conn, payload.userId)
        await conn.commit()
    except Exception as e:
        logger.error(str(e))
        raise StdError(*ErrorCode.UserDelError.value)

    return StdSimpleRes.create(*ErrorCode.Ok.value)


@router.post("/update", response_model=StdSimpleRes)
@LoggingHelper.log_request
async def update(
    request: Request,
    payload: UserUpdateReq,
    conn=Depends(MysqlHelper.depends_async_connection),
):
    data = {}
    if payload.name is not None:
        data["name"] = payload.name
    if payload.age is not None:
        data["age"] = payload.age
    if payload.sex is not None:
        data["sex"] = payload.sex.value

    try:
        await UserDao.update_by_id(conn, payload.userId, data)
        await conn.commit()
    except Exception as e:
        logger.error(str(e))
        raise StdError(*ErrorCode.UserUpdateError.value)

    return StdSimpleRes.create(*ErrorCode.Ok.value)


@router.post("/list", response_model=StdPagingListRes)
@LoggingHelper.log_request
async def get_list(
    request: Request,
    payload: UserListReq,
    conn=Depends(MysqlHelper.depends_async_connection),
):
    try:
        query_total, query_list = await UserDao.get_list(
            conn, payload.pageNo, payload.pageSize
        )
    except Exception as e:
        logger.error(str(e))
        raise StdError(*ErrorCode.UserListError.value)

    return StdPagingListRes.create(*ErrorCode.Ok.value, query_list, query_total)
