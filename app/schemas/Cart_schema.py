from pydantic import BaseModel
from typing import List


class CartItemCreate(BaseModel):
    product_id: int
    quantity: int


class CartItemOut(BaseModel):
    product_id: int
    quantity: int
    price_at_time: float
    subtotal:float

    class Config:
        from_attributes = True


class CartResponse(BaseModel):
    items: List[CartItemOut]
    cart_total: float

class CartOut(BaseModel):
    id: int
    user_id: int
    items: List[CartItemOut]

    class Config:
        orm_mode = True