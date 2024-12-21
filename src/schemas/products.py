from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field

class ProductModel(BaseModel):

    name: str
    description: str
    price: Decimal
    external_id: int


class ProductResponse(ProductModel):

    product_id: int
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    class Config:
        from_attributes = True