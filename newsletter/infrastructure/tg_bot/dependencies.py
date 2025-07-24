from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from newsletter.infrastructure.db.postres import async_session_factory


async def use_db_session() -> AsyncGenerator[AsyncSession]:
    async with async_session_factory() as s:
        yield s
        await s.commit()
