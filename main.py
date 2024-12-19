import uvicorn

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.session import get_db
from src.routes import products
from src.utils.py_logger import get_logger

logger = get_logger(__name__)

app = FastAPI()
logger.info("App is starting..")

app.include_router(products.router)

# @app.get("/")
# def root():
#     return {"message": "Welcome to FastAPI!"}

@app.get("/")
async def healthchecker_db(db: AsyncSession = Depends(get_db)):
    """Функція для перевірки з'єднання з базою даних."""
    try:
        result = await db.execute(text("SELECT 1"))
        if result is None:
            raise HTTPException(status_code=500, detail="Database is not configured correctly")
        return {"message": "Database is working! Welcome to FastAPI!"}
    except Exception as e:
        logger.error(f"Error connecting to the DATABASE")
        raise HTTPException(status_code=500, detail="Error connecting to the database")


if __name__ == '__main__':
    uvicorn.run("main:app", host="127.0.0.1", port=8001, reload=True)