from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.conf.messages import ProductMessages
from src.db.session import get_db
from src.schemas.products import ProductResponse, ProductModel
from src.repository import products as repo_products


router = APIRouter(tags=["Products"], prefix='/products')


@router.get(path="/",
            response_model=list[ProductResponse],
            summary="Get all products")
async def get_products(db: AsyncSession = Depends(get_db)):
    """Отримати всі продукти."""
    products = await repo_products.get_products(db)
    return products


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
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ProductMessages.NOT_FOUND)
    return {"detail": ProductMessages.DELETED_PRODUCT}