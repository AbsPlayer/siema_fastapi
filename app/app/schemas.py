import datetime

from pydantic import BaseModel


class Category(BaseModel):
    name: str


class Product(BaseModel):
    name: str
    price: float
    category_id: int


class Sale(BaseModel):
    quantity: int
    created_at: datetime.datetime
    product_id: int
