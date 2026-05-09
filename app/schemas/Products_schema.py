from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# =========================
# CREATE PRODUCT
# =========================
class ProductCreate(BaseModel):
    product_name: str

    regular_price: Optional[float] = None
    sale_price: Optional[float] = None

    size: Optional[str] = None
    weight: Optional[float] = None
    rating: Optional[float] = None
    life: Optional[int] = None

    type: Optional[str] = None
    brand: Optional[str] = None

    nutrition_energy_kcal: Optional[float] = None
    nutrition_protein_g: Optional[float] = None
    nutrition_magnetiam_kcal: Optional[float] = None
    nutrition_calory_kcal: Optional[float] = None
    nutrition_vitamine_kcal: Optional[float] = None

    stock: int
    sku: Optional[str] = None

    category: Optional[str] = None
    subcategory_id: Optional[int] = None

    tag: Optional[str] = None
    description: Optional[str] = None
    image: Optional[str] = None


# =========================
# PRODUCT RESPONSE
# =========================
class ProductOut(BaseModel):
    id: int
    product_name: str

    regular_price: Optional[float] = None
    sale_price: Optional[float] = None

    # 🔥 CENTRALIZED PRICING FIELDS
    original_price: Optional[float] = None
    offer_price: Optional[float] = None
    coupon_discount: Optional[float] = 0
    final_price: Optional[float] = None
    offer_applied: Optional[bool] = False
    is_coupon_eligible: Optional[bool] = True
    discount: Optional[float] = 0
    offer_type: Optional[str] = None
    offer_value: Optional[float] = None

    size: Optional[str] = None
    weight: Optional[float] = None
    rating: Optional[float] = None
    life: Optional[int] = None

    stock: int

    type: Optional[str] = None
    brand: Optional[str] = None

    category: Optional[str] = None
    subcategory_id: Optional[int] = None

    tag: Optional[str] = None
    description: Optional[str] = None
    image: Optional[str] = None

    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# =========================
# UPDATE PRODUCT
# =========================
class ProductUpdate(BaseModel):
    product_name: Optional[str] = None
    regular_price: Optional[float] = None
    sale_price: Optional[float] = None

    stock: Optional[int] = None

    description: Optional[str] = None
    image: Optional[str] = None

    class Config:
        from_attributes = True