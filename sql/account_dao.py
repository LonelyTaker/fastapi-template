from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from model.account import Account


# 查询用户（id）
async def get_by_id(session: AsyncSession, uid: int):
    query_item_result = await session.execute(select(Account).where(Account.id == uid))
    query_item = query_item_result.scalar()
    return query_item


# 查询用户（账号密码）
async def get_by_account(session: AsyncSession, account: str):
    query_item_result = await session.execute(select(Account).where(Account.account == account))
    query_item = query_item_result.scalar()
    return query_item
