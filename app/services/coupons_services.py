from fastapi import HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP

from app.schemas.Coupons_schema import ApplyCouponRequest, CouponCreate
from app.Crud.Coupons_Crud import (
    get_coupon_by_code,
    get_coupon_usage_count,
    get_user_coupon_usage,
    create_coupon
)


# =========================
# COMMON VALIDATION
# =========================
def validate_coupon(db: Session, coupon, user_id: int, cart_total: Decimal):

    if not coupon:
        raise HTTPException(status_code=404, detail="Invalid coupon")

    if coupon.discount_type not in ["percentage", "fixed"]:
        raise HTTPException(
            status_code=400,
            detail="Invalid coupon configuration"
        )

    if not coupon.is_active:
        raise HTTPException(status_code=400, detail="Coupon inactive")

    now = datetime.now()

    if coupon.start_date and now < coupon.start_date:
        raise HTTPException(status_code=400, detail="Coupon not started")

    if coupon.expiry_date and now > coupon.expiry_date:
        raise HTTPException(status_code=400, detail="Coupon expired")

    if coupon.min_order_amount:
        if cart_total < Decimal(str(coupon.min_order_amount)):
            raise HTTPException(
                status_code=400,
                detail="Minimum order not reached"
            )

    if coupon.usage_limit:
        total_usage = get_coupon_usage_count(db, coupon.id)
        if total_usage >= coupon.usage_limit:
            raise HTTPException(
                status_code=400,
                detail="Coupon usage limit reached"
            )

    user_usage = get_user_coupon_usage(db, coupon.id, user_id)
    if user_usage >= coupon.usage_per_user:
        raise HTTPException(
            status_code=400,
            detail="Coupon already used"
        )


from app.services.pricing_helper import calculate_item_price
from app.models.products import Product

# =========================
# APPLY COUPON
# =========================
def apply_coupon(db: Session, data: ApplyCouponRequest):

    # Basic request validation
    if not data.user_id:
        raise HTTPException(status_code=400, detail="User id required")

    if not data.code:
        raise HTTPException(status_code=400, detail="Coupon code required")

    # Fetch coupon
    coupon = get_coupon_by_code(db, data.code.strip())
    if not coupon:
        raise HTTPException(status_code=404, detail="Invalid coupon")

    # =========================
    # ELIGIBILITY CALCULATION
    # =========================
    total_eligible_amount = Decimal("0")
    total_cart_amount = Decimal("0")
    
    if data.items:
        for item in data.items:
            product = db.query(Product).filter(Product.id == item.product_id).first()
            if not product:
                continue
            
            pricing = calculate_item_price(db, product)
            item_total = Decimal(str(pricing["final_price"])) * item.quantity
            total_cart_amount += item_total
            
            if pricing["is_coupon_eligible"]:
                total_eligible_amount += item_total
    else:
        # Fallback for legacy calls
        total_cart_amount = Decimal(str(data.cart_total or 0))
        total_eligible_amount = total_cart_amount

    if total_cart_amount <= 0:
        raise HTTPException(status_code=400, detail="Cart total must be greater than 0")

    # Shared validation (using total_cart_amount for min_order check)
    validate_coupon(db, coupon, data.user_id, total_cart_amount)

    if total_eligible_amount <= 0:
         raise HTTPException(
            status_code=400, 
            detail="Coupon not applicable on discounted products."
        )

    # =========================
    # DISCOUNT CALCULATION
    # =========================
    discount = Decimal("0")

    if coupon.discount_type == "percentage":
        discount = total_eligible_amount * (
            Decimal(str(coupon.discount_value)) / Decimal("100")
        )

        if coupon.max_discount_amount:
            discount = min(
                discount,
                Decimal(str(coupon.max_discount_amount))
            )

    else:  # fixed
        discount = Decimal(str(coupon.discount_value))

    # prevent over-discount
    discount = min(discount, total_eligible_amount)

    final_amount = total_cart_amount - discount

    return {
        "success": True,
        "coupon_id": coupon.id,
        "code": coupon.code,
        "discount": float(
            discount.quantize(
                Decimal("0.01"),
                rounding=ROUND_HALF_UP
            )
        ),
        "final_amount": float(
            final_amount.quantize(
                Decimal("0.01"),
                rounding=ROUND_HALF_UP
            )
        )
    }


# =========================
# CREATE COUPON
# =========================
def create_coupon_service(db: Session, data: CouponCreate):

    # Clean code input
    code = data.code.strip().upper()

    if not code:
        raise HTTPException(
            status_code=400,
            detail="Coupon code required"
        )

    if data.discount_type not in ["percentage", "fixed"]:
        raise HTTPException(
            status_code=400,
            detail="Invalid discount type"
        )

    if data.discount_value <= 0:
        raise HTTPException(
            status_code=400,
            detail="Invalid discount value"
        )

    if (
        data.discount_type == "percentage"
        and data.discount_value > 100
    ):
        raise HTTPException(
            status_code=400,
            detail="Percentage greater than 100 not allowed"
        )

    # Duplicate check
    existing = get_coupon_by_code(db, code)
    if existing:
        raise HTTPException(
            status_code=400,
            detail="Coupon already exists"
        )

    # keep backend compatible
    data.code = code

    return create_coupon(db, data)