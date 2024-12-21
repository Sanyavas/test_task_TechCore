from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy import inspect

from src.db.models import Base
from src.utils.py_logger import get_logger

logger = get_logger(__name__)

DATABASE_URL = "sqlite+aiosqlite:///./test.db"

engine = create_async_engine(DATABASE_URL, echo=False)
SessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession,
                                  expire_on_commit=False)


async def get_db() -> AsyncSession:
    async with SessionLocal() as session:
        try:
            yield session
        except Exception as err:
            logger.error(f"ERROR session DB: {err}")
            await session.rollback()
            raise  # Підняти виключення повторно
        finally:
            await session.close()


async def init_db():
    """Функція для створення таблиць у базі даних, якщо їх ще немає."""
    async with engine.begin() as conn:
        try:
            # Використовуємо run_sync для синхронної перевірки наявності таблиці
            table_exists = await conn.run_sync(lambda conn: inspect(conn).has_table('products'))

            if not table_exists:
                logger.info("Creating tables...")
                await conn.run_sync(Base.metadata.create_all)
                logger.info("Tables created successfully!")
            else:
                logger.info("Tables already exist.")
        except Exception as e:
            logger.error(f"Error while creating tables: {e}")


