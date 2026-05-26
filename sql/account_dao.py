from sqlalchemy.ext.asyncio import AsyncConnection
from sqlalchemy import select

from model.table import Account


class AccountDao:

    @staticmethod
    async def get_by_id(conn: AsyncConnection, uid: int):
        """查询用户（id）"""
        query_item_result = await conn.execute(
            select(Account).where(Account.c.id == uid)
        )
        query_item = query_item_result.fetchone()
        return query_item

    @staticmethod
    async def get_by_account(conn: AsyncConnection, account: str):
        """查询用户（账号密码）"""
        query_item_result = await conn.execute(
            select(Account).where(Account.c.account == account)
        )
        query_item = query_item_result.fetchone()
        return query_item
