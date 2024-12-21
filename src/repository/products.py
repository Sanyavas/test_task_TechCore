import asyncio
import httpx
from typing import Sequence

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.db.models import Product
from src.schemas.products import ProductModel
from src.utils.featch_product_api import fetch_product_from_api
from src.utils.py_logger import get_logger

logger = get_logger(__name__)


async def get_all_products(db: AsyncSession) -> Sequence[Product]:
    """Функція для отримання всіх продуктів з бази даних."""

    result = await db.execute(select(Product))
    products = result.scalars().all()

    return products


async def get_product_id(product_id: int, db: AsyncSession) -> Product:
    """Функція для отримання продукту за його унікальним ID."""

    result = await db.execute(select(Product).filter(Product.product_id == product_id))
    product = result.scalar_one_or_none()

    return product


async def get_all_id_of_products(db: AsyncSession) -> list[int]:
    """Функція для отримання всіх external_id продуктів з бази даних."""

    result = await db.execute(select(Product.external_id))
    external_ids = [row[0] for row in result.fetchall()]

    return external_ids


async def create_product(body: ProductModel, db: AsyncSession) -> Product:
    """Функція для створення нового продукту в базі даних."""

    product = Product(**body.model_dump())
    db.add(product)
    await db.commit()
    await db.refresh(product)
    logger.info(f"Product created in the database.")

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
        logger.info(f"Update product with ID {product_id}")

    return product


async def delete_product(product_id: int, db: AsyncSession) -> bool:
    """Функція для видалення продукту з бази даних."""

    product = await get_product_id(product_id, db)
    if product:
        await db.delete(product)
        await db.commit()
        logger.info(f"Deleted product with ID {product_id}")

    return product



async def fetch_and_update_products(external_ids: list[str | int], db: AsyncSession):
    """Функція для отримання даних із зовнішнього API та оновлення бази даних."""

    # Паралельне виконання запитів до API
    tasks = [fetch_product_from_api(str(external_id)) for external_id in external_ids]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    for external_id, result in zip(external_ids, results):

        if isinstance(result, Exception):
            logger.error(f"Error fetching product with external_id: {external_id} - {result}")
            continue

        if isinstance(result, list) and len(result) == 1:
            product = result[0]

            name = product.get("name")
            description = product.get("description")
            price = product.get("price")

            # Перевірка та оновлення або створення продукту
            query_result = await db.execute(select(Product).filter_by(external_id=external_id))
            existing_product = query_result.scalar_one_or_none()

            if existing_product:
                existing_product.name = name
                existing_product.description = description
                existing_product.price = price
                logger.info(f"Product with external_id {external_id} updated in DB")
            else:
                new_product = Product(external_id=external_id, name=name, description=description, price=price)
                db.add(new_product)
                logger.info(f"Product with external_id {external_id} added in DB")
        else:
            logger.error(f"Error: Unexpected data structure for external_id {external_id}, got: {result}")

    await db.commit()



async def fetch_and_update_products_in_background(external_ids: list[int], db: AsyncSession):
    """Фонова задача для оновлення продуктів."""

    try:
        await fetch_and_update_products(external_ids, db)
        logger.info(f"Products updated successfully! Total count: {len(external_ids)}.")
    except Exception as e:
        logger.error(f"Error occurred while updating products: {e}")
        raise HTTPException(status_code=500, detail="Failed to update products")
