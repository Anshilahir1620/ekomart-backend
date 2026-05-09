from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class CouponCreate(BaseModel):
    code: str
    discount_type: str
    discount_value: float

    min_order_amount: float = 0
    max_discount_amount: Optional[float] = None

    usage_limit: Optional[int] = None
    usage_per_user: int = 1

    start_date: datetime
    expiry_date: datetime

    is_active: bool = True

class CouponResponse(BaseModel):
    id: int
    code: str
    discount_type: str
    discount_value: float

    min_order_amount: float
    max_discount_amount: Optional[float]

    usage_limit: Optional[int]
    usage_per_user: int

    start_date: Optional[datetime]
    expiry_date: Optional[datetime]

    is_active: bool

    class Config:
        from_attributes = True

class CartItemInput(BaseModel):
    product_id: int
    quantity: int

class ApplyCouponRequest(BaseModel):
    code: str
    user_id: int
    items: Optional[list[CartItemInput]] = None
    cart_total: Optional[float] = None  # Fallback

class ApplyCouponResponse(BaseModel):
    success: bool
    coupon_id: Optional[int]
    code: Optional[str]
    discount: Optional[float]
    final_amount: Optional[float]
    message: Optional[str]

class CouponUpdate(BaseModel):
    code: Optional[str] = None
    discount_type: Optional[str] = None
    discount_value: Optional[float] = None
    min_order_amount: Optional[float] = None
    max_discount_amount: Optional[float] = None
    usage_limit: Optional[int] = None
    usage_per_user: Optional[int] = None
    start_date: Optional[datetime] = None
    expiry_date: Optional[datetime] = None
    is_active: Optional[bool] = None