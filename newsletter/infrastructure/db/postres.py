from typing import cast

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from newsletter.core.config import logging_settings, settings

alchemy_async_engine = create_async_engine(
    url=cast(str, settings.POSTGRES_DSN),
    pool_size=settings.POSTGRES_POOL_MIN_SIZE,
    max_overflow=settings.POSTGRES_POOL_MAX_SIZE - settings.POSTGRES_POOL_MIN_SIZE,
    pool_recycle=3600,
    pool_pre_ping=True,
    echo=logging_settings.IS_NEED_LOG_SQL_QUERIES,
    connect_args={
        "keepalives": 1,
        "keepalives_idle": 30,
        "keepalives_interval": 10,
        "keepalives_count": 5,
    },
)

async_session_factory = async_sessionmaker(alchemy_async_engine, class_=AsyncSession)
