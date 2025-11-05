from __future__ import annotations

from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from .config import get_settings


_settings = get_settings()


def _create_engine() -> AsyncEngine:
    url = str(_settings.database_url)
    if "+psycopg" not in url:
        # ensure async driver
        url = url.replace("postgresql", "postgresql+psycopg")
    return create_async_engine(url, future=True, echo=False)


engine: AsyncEngine = _create_engine()
SessionFactory = async_sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)


@asynccontextmanager
async def session_scope() -> AsyncSession:
    async with SessionFactory() as session:  # type: ignore[call-arg]
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


__all__ = ["engine", "SessionFactory", "session_scope"]
