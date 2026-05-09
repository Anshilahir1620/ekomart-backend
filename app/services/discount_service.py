from decimal import Decimal


def apply_best_discount(product, coupon=None, offer_data=None):
    base_price = product.sale_price or product.regular_price

    if base_price is None:
        return {
            "final_price": 0,
            "discount": 0,
            "applied": None
        }

    price = Decimal(str(base_price))

    # =========================
    # OFFER VALUES
    # =========================
    offer_price = price
    offer_discount = Decimal("0")

    if offer_data:
        offer_price = Decimal(str(offer_data["final_price"]))
        offer_discount = Decimal(str(offer_data["discount"]))

    # =========================
    # COUPON VALUES
    # =========================
    coupon_price = price
    coupon_discount = Decimal("0")

    if coupon:
        if coupon.discount_type == "percentage":
            coupon_discount = price * (
                Decimal(str(coupon.discount_value)) / Decimal("100")
            )

            if getattr(coupon, "max_discount_amount", None):
                coupon_discount = min(
                    coupon_discount,
                    Decimal(str(coupon.max_discount_amount))
                )

        else:
            coupon_discount = Decimal(str(coupon.discount_value))

        # prevent over-discount
        coupon_discount = min(coupon_discount, price)

        coupon_price = price - coupon_discount

    # =========================
    # BEST DISCOUNT WINS
    # Tie = Offer wins
    # =========================
    if coupon and coupon_price < offer_price:
        return {
            "final_price": float(coupon_price),
            "discount": float(coupon_discount),
            "applied": "coupon"
        }

    return {
        "final_price": float(offer_price),
        "discount": float(offer_discount),
        "applied": "offer" if offer_data else None
    }