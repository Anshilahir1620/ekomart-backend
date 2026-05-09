from decimal import Decimal
from app.models.categories import Category
from app.Crud.daily_offer_crud import get_active_offer_by_category


def apply_offer(db, product):
    # =========================
    # FIND CATEGORY ID
    # =========================
    category_id = None

    if product.category:
        category = (
            db.query(Category)
            .filter(Category.name == product.category)
            .first()
        )

        if category:
            category_id = category.id

    # no matching category
    if not category_id:
        base_price = product.sale_price or product.regular_price or 0

        return {
            "final_price": float(base_price),
            "discount": 0,
            "offer_applied": False
        }

    # =========================
    # GET ACTIVE OFFER
    # =========================
    offer = get_active_offer_by_category(db, category_id)

    base_price = product.sale_price or product.regular_price

    if base_price is None:
        return {
            "final_price": 0,
            "discount": 0,
            "offer_applied": False
        }

    price = Decimal(str(base_price))

    if not offer:
        return {
            "final_price": float(price),
            "discount": 0,
            "offer_applied": False
        }

    # =========================
    # APPLY DISCOUNT
    # =========================
    if offer.discount_type == "percentage":
        discount = price * (
            Decimal(str(offer.discount_value)) / Decimal("100")
        )
    else:
        discount = Decimal(str(offer.discount_value))

    discount = min(discount, price)

    final_price = price - discount

    return {
        "final_price": float(final_price),
        "discount": float(discount),
        "offer_applied": True,
        "offer_type": offer.discount_type,
        "offer_value": float(offer.discount_value)
    }