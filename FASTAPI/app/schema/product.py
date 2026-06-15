# improved validations
from pydantic import BaseModel, Field 
from typing import Annotated 

class Product(BaseModel):
    id: str
    sku: Annotated[
        str,
        Field(
            min_length=6,
            max_length=30,
            title="sku",
            description="Stock Keeping Unit",
            example="734-hdf-435-3d",
        ),
    ]
    name: str