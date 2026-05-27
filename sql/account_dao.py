from sqlalchemy.ext.asyncio import AsyncConnection
from sqlalchemy import select

from model.table import account_table


class AccountDao:
    @staticmethod
    async def get_by_id(conn: AsyncConnection, uid: int) -> dict | None:
        query_item_result = await conn.execute(
            select(account_table).where(account_table.c.id == uid)
        )
        row = query_item_result.fetchone()
        return dict(row._mapping) if row else None

    @staticmethod
    async def get_by_account(conn: AsyncConnection, account: str) -> dict | None:
        query_item_result = await conn.execute(
            select(account_table).where(account_table.c.account == account)
        )
        row = query_item_result.fetchone()
        return dict(row._mapping) if row else None
