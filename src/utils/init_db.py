import asyncio

from sqlalchemy import text

from src.db.session import engine, SessionLocal
from src.db.models import Base, Product

async def init_db():
    """Функція створення таблиць у базі даних."""
    async with engine.begin() as conn:
        print("Creating tables...")
        await conn.run_sync(Base.metadata.create_all)
        print("Tables created successfully!")

async def seed_data():
    """Функція для наповнення бази даних тестовими даними."""
    async with SessionLocal() as session:
        # Перевіряємо, чи база вже заповнена
        result = await session.execute(text("SELECT COUNT(*) FROM products"))
        count = result.scalar()

        if count > 0:
            print("Database already has data. Skipping seeding.")
            return

        # Додавання тестових даних
        print("Seeding data...")
        products = [
            Product(name="Product 1", description="Description 1", price=9.99, external_id=1),
            Product(name="Product 2", description="Description 2", price=19.99, external_id=2),
        ]
        session.add_all(products)
        await session.commit()
        print("Data seeded successfully!")

async def main():
    await init_db()
    # await seed_data()

if __name__ == "__main__":
    asyncio.run(main())
