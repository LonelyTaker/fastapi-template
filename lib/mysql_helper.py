import contextlib
from asyncio import current_task
from sqlalchemy.ext.asyncio import \
    create_async_engine, \
    AsyncEngine, \
    AsyncSession, \
    async_scoped_session, \
    async_sessionmaker

from setting import MYSQL_INFO


# mysql工具类
class MysqlHelper(object):
    __engine: AsyncEngine = None
    __ScopedSession = None

    @classmethod
    async def depends_async_session(cls):
        try:
            async with cls.__ScopedSession() as session:
                yield session
        finally:
            await cls.__ScopedSession.remove()

    @classmethod
    @contextlib.asynccontextmanager
    async def get_async_session(cls):
        session: AsyncSession = cls.__ScopedSession()
        try:
            yield session
        finally:
            await session.close()
            await cls.__ScopedSession.remove()

    @classmethod
    def init(cls):
        if cls.__engine:
            cls.__engine.dispose()
        # 创建引擎
        cls.__engine = create_async_engine(**MYSQL_INFO)
        # 创建会话
        session_factory = async_sessionmaker(bind=cls.__engine)
        # 使用scoped_session维护session
        cls.__ScopedSession = async_scoped_session(session_factory, scopefunc=current_task)
