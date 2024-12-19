
from pydantic import BaseModel, Field

class ItemModel(BaseModel):

    item_id: int
    name: str = Field(min_length=1, max_length=50)
    description: str = Field(max_length=1024)
    price: str
    external_id: int