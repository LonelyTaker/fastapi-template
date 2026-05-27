import contextlib
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncEngine,
)

from lib.configure import Configure


class MysqlHelper:
    __engine: AsyncEngine

    @classmethod
    async def depends_async_connection(cls):
        """依赖注入：获取连接"""
        async with cls.__engine.connect() as conn:
            yield conn

    @classmethod
    @contextlib.asynccontextmanager
    async def get_async_connection(cls):
        conn = await cls.__engine.connect()
        try:
            yield conn
        finally:
            await conn.close()

    @classmethod
    async def init(cls):
        """初始化引擎"""
        cls.__engine = create_async_engine(**Configure.get("mysql"))

    @classmethod
    async def dispose(cls):
        """销毁引擎"""
        await cls.__engine.dispose()
