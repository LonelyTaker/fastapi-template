from typing import Tuple, List
from sqlalchemy.ext.asyncio import AsyncConnection
from sqlalchemy import insert, delete, update, select, func, desc

from model.table import user_table


class UserDao:
    @staticmethod
    async def add_one(conn: AsyncConnection, payload: dict):
        await conn.execute(insert(user_table).values(payload))

    @staticmethod
    async def del_by_id(conn: AsyncConnection, user_id: int):
        await conn.execute(delete(user_table).where(user_table.c.id == user_id))

    @staticmethod
    async def update_by_id(conn: AsyncConnection, user_id: int, payload: dict):
        await conn.execute(
            update(user_table).where(user_table.c.id == user_id).values(payload)
        )

    @staticmethod
    async def get_list(
        conn: AsyncConnection, page_no: int, page_size: int
    ) -> Tuple[int, List[dict]]:
        query_list_result = await conn.execute(
            select(user_table)
            .order_by(desc(user_table.c.id))
            .offset((page_no - 1) * page_size)
            .limit(page_size)
        )
        query_list = [dict(row._mapping) for row in query_list_result.fetchall()]
        query_count_result = await conn.execute(select(func.count(user_table.c.id)))
        query_count = query_count_result.scalar() or 0
        return query_count, query_list
