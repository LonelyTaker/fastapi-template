from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, insert, delete, update, select

from model.user import User


# 添加用户
async def add_one(session: AsyncSession, payload):
    await session.execute(insert(User).values(payload))
    await session.commit()


# 删除用户
async def del_by_id(session: AsyncSession, user_id):
    await session.execute(delete(User).where(User.id == user_id))
    await session.commit()


# 更新用户
async def update_by_id(session: AsyncSession, user_id, payload):
    await session.execute(update(User).where(User.id == user_id).values(payload))
    await session.commit()


# 查询用户
async def get_list(session: AsyncSession, payload):
    page_no = payload.pageNo
    page_size = payload.pageSize

    query_list_result = await session.execute(select(User).offset((page_no - 1) * page_size).limit(page_size))
    query_list = query_list_result.scalars().all()
    query_count_result = await session.execute(select(func.count(User.id)))
    query_count = query_count_result.scalar()
    return query_count, query_list
