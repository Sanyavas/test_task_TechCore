from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from db.models import Product
from schemas.products import ProductModel


async def get_products(db: AsyncSession) -> Sequence[Product]:
    """Функція для отримання всіх продуктів з бази даних."""
    result = await db.execute(select(Product))
    products = result.scalars().all()

    return products


async def get_product_id(product_id: int, db: AsyncSession) -> Product:
    """Функція для отримання продукту за його унікальним ID."""
    result = await db.execute(select(Product).filter_by(product_id=product_id))
    product = result.scalar_one_or_none()

    return product


async def create_product(body: ProductModel, db: AsyncSession) -> Product:
    """Функція для створення нового продукту в базі даних."""
    product = Product(**body.model_dump())
    db.add(product)
    await db.commit()
    await db.refresh(product)
    return product


async def update_product(product_id: int, body: ProductModel, db: AsyncSession):
    """Функція для оновлення даних продукту."""
    product = await get_product_id(product_id, db)

    if product:
        product.name = body.name
        product.description = body.description
        product.price = body.price
        product.external_id = body.external_id

        await db.commit()
        await db.refresh(product)

    return product


async def delete_product(product_id: int, db: AsyncSession) -> None:
    """Функція для видалення продукту з бази даних."""
    product = await get_product_id(product_id, db)
    if product:
        await db.delete(product)
        await db.commit()
