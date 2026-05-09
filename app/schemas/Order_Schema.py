# app/schemas/order_schema.py

from pydantic import BaseModel, Field, model_validator
from typing import List, Optional
from datetime import datetime
from app.schemas.Payment_schema import PaymentOut
from enum import Enum

class PaymentMethod(str, Enum):
    COD = "COD"
    CARD = "CARD"
    UPI = "UPI"
    NETBANKING = "NETBANKING"


class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int = Field(gt=0)


class OrderCreate(BaseModel):
    user_id: Optional[int] = None
    items: List[OrderItemCreate]
    payment_method: PaymentMethod

    

    
    coupon_code: Optional[str] = None

    shipping_name: str
    shipping_phone: str
    shipping_address: str
    shipping_city: str
    shipping_state: Optional[str] = None
    shipping_pincode: Optional[str] = None


class OrderItemOut(BaseModel):
    product_id: int
    quantity: int
    price: float
    # New fields from relationship
    product_name: Optional[str] = None
    image: Optional[str] = None

    @model_validator(mode="before")
    @classmethod
    def flatten_product(cls, data):
        if hasattr(data, "product") and data.product:
            # Add to the data so Pydantic can pick it up
            data.product_name = data.product.product_name
            data.image = data.product.image
        return data

    class Config:
        from_attributes = True




class OrderOut(BaseModel):
    id: int
    user_id: Optional[int]

    total_amount: float
    discount_amount: float
    final_amount: float

    coupon_code: Optional[str] = None

    status: str
    created_at: datetime

    shipping_name: Optional[str] = None
    shipping_phone: Optional[str] = None
    shipping_address: Optional[str] = None
    shipping_city: Optional[str] = None
    shipping_state: Optional[str] = None
    shipping_pincode: Optional[str] = None

    items: List[OrderItemOut]
    payments: List[PaymentOut] = []

    class Config:
        from_attributes = True