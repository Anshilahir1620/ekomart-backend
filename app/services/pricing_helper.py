from decimal import Decimal, ROUND_HALF_UP
from sqlalchemy.orm import Session
from app.services.offer_service import apply_offer
from app.models.products import Product

def calculate_item_price(db: Session, product: Product, coupon=None):
    """
    Centralized pricing logic for Ekomart.
    Priority:
    1. Product Offer Price (Category based)
    2. Coupon Discount (Only if no offer)
    3. Final Total
    """
    
    # 1. Get Base Price
    base_price = Decimal(str(product.sale_price or product.regular_price or 0))
    regular_price = Decimal(str(product.regular_price or 0))
    
    # 2. Check for Category Offer
    offer = apply_offer(db, product)
    
    offer_applied = offer.get("offer_applied", False)
    offer_discount = Decimal(str(offer.get("discount", 0)))
    offer_price = Decimal(str(offer.get("final_price", base_price)))
    
    coupon_discount = Decimal("0")
    
    # 3. Coupon Logic
    # Rule: If product has an offer, coupon does NOT apply.
    if not offer_applied and coupon:
        if coupon.discount_type == "percentage":
            coupon_discount = base_price * (Decimal(str(coupon.discount_value)) / Decimal("100"))
            if coupon.max_discount_amount:
                coupon_discount = min(coupon_discount, Decimal(str(coupon.max_discount_amount)))
        else:
            coupon_discount = Decimal(str(coupon.discount_value))
        
        # Prevent over-discounting
        coupon_discount = min(coupon_discount, base_price)

    final_price = offer_price if offer_applied else (base_price - coupon_discount)

    return {
        "original_price": float(regular_price),
        "base_price": float(base_price),
        "offer_price": float(offer_price) if offer_applied else None,
        "offer_discount": float(offer_discount),
        "offer_type": offer.get("offer_type"),
        "offer_value": float(offer.get("offer_value", 0)),
        "coupon_discount": float(coupon_discount),
        "final_price": float(final_price.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)),
        "offer_applied": offer_applied,
        "coupon_applied": coupon_discount > 0,
        "is_coupon_eligible": not offer_applied
    }
