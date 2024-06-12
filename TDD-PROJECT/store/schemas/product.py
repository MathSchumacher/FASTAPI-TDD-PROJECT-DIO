from datetime import datetime
from typing import Annotated, Optional
from bson import Decimal128
from pydantic import UUID4, AfterValidator, BaseModel, Field, model_validator
from store.schemas.base import BaseSchemaMixin, OutMixin
from decimal import Decimal


class ProductBase(BaseModel):
    name: str = Field(..., description="Product Name")
    quantity: int = Field(..., description="Product quantity")
    price: Decimal = Field(..., description="Product price")
    status: bool = Field(..., description="Product status")

class ProductIn(ProductBase, BaseSchemaMixin):
    ...

class ProductOut(ProductIn, OutMixin):
    ...
def convert_decimal_128(v):
    return Decimal128(str(v))

Decimal_ = Annotated[Decimal, AfterValidator(convert_decimal_128)]
class ProductUpdate(BaseSchemaMixin):
    quantity: Optional[int] = Field(..., description="Product quantity")
    price: Optional[Decimal_] = Field(..., description="Product price")
    status: Optional[bool] = Field(..., description="Product status")    

class ProductUpdateOut(ProductOut):
    ...