from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field

class ProductModel(BaseModel):

    product_id: int
    name: str = Field(min_length=1, max_length=50)
    description: str = Field(max_length=1024)
    price: Decimal
    external_id: int


class ProductResponse(ProductModel):

    product_id: int
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    class Config:
        from_attributes = True