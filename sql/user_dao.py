from sqlalchemy.ext.asyncio import AsyncConnection
from sqlalchemy import func, insert, delete, update, select

from model.table import User


class UserDao:
    # 添加用户
    @staticmethod
    async def add_one(conn: AsyncConnection, payload):
        await conn.execute(insert(User).values(payload))
        await conn.commit()

    # 删除用户
    @staticmethod
    async def del_by_id(conn: AsyncConnection, user_id):
        await conn.execute(delete(User).where(User.c.id == user_id))
        await conn.commit()

    # 更新用户
    @staticmethod
    async def update_by_id(conn: AsyncConnection, user_id, payload):
        await conn.execute(update(User).where(User.c.id == user_id).values(payload))
        await conn.commit()

    # 查询用户
    @staticmethod
    async def get_list(conn: AsyncConnection, payload):
        page_no = payload.pageNo
        page_size = payload.pageSize

        query_list_result = await conn.execute(
            select(User).offset((page_no - 1) * page_size).limit(page_size)
        )
        query_list = query_list_result.fetchall()
        query_count_result = await conn.execute(select(func.count(User.c.id)))
        query_count = query_count_result.scalar()
        return query_count, query_list
