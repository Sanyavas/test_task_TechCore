from typing import Union

from fastapi import APIRouter, HTTPException, status, Depends, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

from src.conf.messages import ProductMessages
from src.db.session import get_db
from src.schemas.products import ProductResponse, ProductModel
from src.repository import products as repo_products
from src.utils.featch_product_api import fetch_product_from_api

router = APIRouter(tags=["Products"], prefix='/products')


@router.get(path="/",
            response_model=list[ProductResponse],
            summary="Get all products")
async def get_products(db: AsyncSession = Depends(get_db)):
    """Отримати всі продукти."""

    products = await repo_products.get_all_products(db)
    if products is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ProductMessages.NOT_FOUND)
    return products


@router.get("/fetch_external/",
            summary="Get all external products")
async def get_all_fetch_external_product():
    """Отримання всіх продуктів із зовнішнього API"""
    try:
        products = await fetch_product_from_api()
        if not products:
            raise HTTPException(status_code=404, detail="No products found.")
        return {"message": products}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get(path="/{product_id}",
            response_model=ProductResponse,
            summary="Get product by ID")
async def get_product(product_id: int, db: AsyncSession = Depends(get_db)):
    """Отримати продукт за унікальним ID."""

    product = await repo_products.get_product_id(product_id, db)
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ProductMessages.NOT_FOUND)
    return product


@router.post(path="/",
             response_model=ProductResponse,
             status_code=status.HTTP_201_CREATED,
             summary="Create a new product")
async def create_contact(body: ProductModel, db: AsyncSession = Depends(get_db)):
    """Створити новий продукт."""

    product = await repo_products.create_product(body, db)
    return product


@router.put(path="/{product_id}",
            response_model=ProductResponse,
            summary="Update product by ID")
async def update_contact(body: ProductModel, product_id: int, db: AsyncSession = Depends(get_db)):
    """Оновити продукт за його унікальним ID."""

    product = await repo_products.update_product(product_id, body, db)
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ProductMessages.NOT_FOUND)
    return product


@router.delete(path="/{product_id}",
               response_model=dict,
               summary="Delete product by ID")
async def delete_product(product_id: int, db: AsyncSession = Depends(get_db)):
    """Видалити продукт за його унікальним ID."""

    product = await repo_products.delete_product(product_id, db)
    if product is None:  # Якщо None або False
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ProductMessages.NOT_FOUND)
    return {"detail": ProductMessages.DELETED_PRODUCT}


@router.post("/fetch_external/",
             summary="Fetch and update external products",
             status_code=status.HTTP_201_CREATED)
async def fetch_external_products(external_ids: list[Union[str, int]] = [101, "105", 120], db: AsyncSession = Depends(get_db)):
    """Створює або оновлює записи в БД."""

    if not external_ids:
        raise HTTPException(status_code=400, detail="No external_ids provided")

    await repo_products.fetch_and_update_products(external_ids, db)
    return {"message": "Products updated successfully"}


@router.post("/refresh_all/",
             summary="Refresh all product data",
             status_code=status.HTTP_201_CREATED)
async def refresh_all_products(background_tasks: BackgroundTasks, db: AsyncSession = Depends(get_db)):
    """Запуск фонової задачі з оновлення всіх продуктів."""

    external_ids = await repo_products.get_all_id_of_products(db)
    if not external_ids:
        raise HTTPException(status_code=400, detail="No products found in the database")

    background_tasks.add_task(repo_products.fetch_and_update_products_in_background, external_ids, db)

    return {"message": "Product update task has been started in the background"}
