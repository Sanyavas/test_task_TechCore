import httpx
from typing import Any

from fastapi import HTTPException

from src.utils.py_logger import get_logger

logger = get_logger(__name__)


async def fetch_product_from_api(external_id: str) -> Any:
    """Отримання продукту з зовнішнього API."""

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"https://my-json-server.typicode.com/Sanyavas/test_items/products/?external_id={external_id}")
            # response = await client.get(f"https://jsonplaceholder.typicode.com/posts/{external_id}")
            response.raise_for_status()
            data = response.json()
            if not data:
                raise HTTPException(status_code=404, detail=f"Product with ID {external_id} not found.")
            return data

    except httpx.HTTPStatusError as http_err:
        logger.error(f"HTTP error for ID {external_id}: {http_err.response.status_code} {http_err.response.text}")
        raise HTTPException(status_code=502, detail=f"External API returned an error for ID {external_id}.")
    except httpx.RequestError as req_err:
        logger.error(f"Network error for ID {external_id}: {req_err}")
        raise HTTPException(status_code=503, detail="External API is unavailable.")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error.")

