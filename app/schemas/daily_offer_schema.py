from pydantic import BaseModel, field_validator, ValidationInfo
from datetime import datetime
from typing import Literal


class DailyOfferBase(BaseModel):
    category_id: int
    discount_type: Literal["percentage", "flat"]
    discount_value: float
    start_date: datetime
    end_date: datetime
    is_active: bool = True

    # =========================
    # VALIDATE DISCOUNT VALUE
    # =========================
    @field_validator("discount_value")
    @classmethod
    def validate_discount(
        cls,
        v: float,
        info: ValidationInfo
    ):
        if v <= 0:
            raise ValueError(
                "Discount must be greater than 0"
            )

        discount_type = info.data.get("discount_type")

        if (
            discount_type == "percentage"
            and v > 100
        ):
            raise ValueError(
                "Percentage cannot exceed 100"
            )

        return v

    # =========================
    # VALIDATE DATE RANGE
    # =========================
    @field_validator("end_date")
    @classmethod
    def validate_dates(
        cls,
        v: datetime,
        info: ValidationInfo
    ):
        start_date = info.data.get("start_date")

        if start_date and v < start_date:
            raise ValueError(
                "end_date must be after start_date"
            )

        return v


class DailyOfferCreate(DailyOfferBase):
    pass


class DailyOfferOut(DailyOfferBase):
    id: int

    class Config:
        from_attributes = True


# =========================
# TODAY OFFER PRODUCT
# =========================
class OfferProductOut(BaseModel):
    id: int
    product_name: str
    image: str
    regular_price: float
    sale_price: float
    final_price: float
    discount: float


# =========================
# TODAY OFFER RESPONSE
# =========================
class TodayOfferOut(BaseModel):
    category_id: int
    category_name: str
    category_slug: str
    category_image: str | None = None
    offer_type: str
    offer_value: float
    products: list[OfferProductOut]