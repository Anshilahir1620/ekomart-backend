from fastapi import HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from datetime import datetime
from decimal import Decimal

from app.services.email_service import send_order_email
from app.services.offer_service import apply_offer
from app.services.discount_service import apply_best_discount
from app.services.pricing_helper import calculate_item_price

from app.models.products import Product
from app.models.coupons import CouponUsage
from app.models.users import User

from app.Crud.Coupons_Crud import (
    get_coupon_by_code,
    get_coupon_usage_count,
    get_user_coupon_usage,
)

from app.Crud.Order_Crud import create_order


def create_order_service(
    db: Session,
    order_data,
    user_id: int,
    background_tasks: BackgroundTasks = None
):

    if not order_data.items:
        raise HTTPException(status_code=400, detail="Order items required")

    # =========================
    # INITIAL VALUES
    # =========================
    total_amount = Decimal("0")      # before discount
    final_amount = Decimal("0")      # after discount
    discount = Decimal("0")

    coupon = None
    coupon_id = None
    coupon_code = None

    # =========================
    # COUPON BASIC VALIDATION
    # =========================
    if order_data.coupon_code:

        coupon = get_coupon_by_code(db, order_data.coupon_code)

        if not coupon:
            raise HTTPException(status_code=400, detail="Invalid coupon")

        if not coupon.is_active:
            raise HTTPException(status_code=400, detail="Coupon inactive")

        now = datetime.now()

        if coupon.start_date and now < coupon.start_date:
            raise HTTPException(status_code=400, detail="Coupon not started")

        if coupon.expiry_date and now > coupon.expiry_date:
            raise HTTPException(status_code=400, detail="Coupon expired")

        if coupon.usage_limit:
            total_usage = get_coupon_usage_count(db, coupon.id)
            if total_usage >= coupon.usage_limit:
                raise HTTPException(status_code=400, detail="Coupon limit reached")

        user_usage = get_user_coupon_usage(db, coupon.id, user_id)
        if user_usage >= coupon.usage_per_user:
            raise HTTPException(status_code=400, detail="Coupon already used")


    # =========================
    # PRODUCT LOOP
    # =========================
    for item in order_data.items:

        product = (
            db.query(Product)
            .filter(Product.id == item.product_id)
            .with_for_update()
            .first()
        )

        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        if product.stock < item.quantity:
            raise HTTPException(
                status_code=400,
                detail=f"{product.product_name} out of stock"
            )

        # 🔥 USE CENTRALIZED PRICING
        pricing = calculate_item_price(db, product, coupon=coupon)
        
        item_total = Decimal(str(pricing["base_price"])) * item.quantity
        total_amount += item_total

        item_final_price = Decimal(str(pricing["final_price"]))
        item_final_total = item_final_price * item.quantity

        final_amount += item_final_total
        discount += (item_total - item_final_total)

    # =========================
    # COUPON MIN ORDER CHECK
    # total_amount = before discount
    # =========================
    if coupon and coupon.min_order_amount:
        if total_amount < Decimal(str(coupon.min_order_amount)):
            raise HTTPException(
                status_code=400,
                detail="Minimum order not reached"
            )

        coupon_id = coupon.id
        coupon_code = coupon.code

    # =========================
    # CREATE ORDER
    # =========================
    db_order = create_order(db, order_data, user_id)

    # keep same column names
    db_order.total_amount = float(total_amount)       # before discount
    db_order.discount_amount = float(discount)
    db_order.final_amount = float(final_amount)       # payable

    db_order.coupon_id = coupon_id
    db_order.coupon_code = coupon_code

    # =========================
    # PAYMENT UPDATE
    # =========================
    if db_order.payments and len(db_order.payments) > 0:
        db_order.payments[0].amount = float(final_amount)

    # =========================
    # SAVE COUPON USAGE
    # =========================
    if coupon_id:
        usage = CouponUsage(
            coupon_id=coupon_id,
            user_id=user_id,
            order_id=db_order.id
        )
        db.add(usage)

    db.commit()
    db.refresh(db_order)

    # =========================
    # EMAIL
    # =========================
    if background_tasks:
        user = db.query(User).filter(User.id == user_id).first()

        if user and user.email:
            background_tasks.add_task(
                send_order_email,
                user.email,
                user.name,
                db_order
            )

    return db_order








# from fastapi import HTTPException
# from sqlalchemy.orm import Session
# from datetime import datetime
# from decimal import Decimal
# from fastapi import BackgroundTasks

# from app.services.email_service import send_order_email
# from app.services.offer_service import apply_offer
# from app.services.discount_service import apply_best_discount

# from app.models.products import Product
# from app.models.coupons import CouponUsage
# from app.models.users import User

# from app.Crud.Coupons_Crud import (
#     get_coupon_by_code,
#     get_coupon_usage_count,
#     get_user_coupon_usage,
# )

# from app.Crud.Order_Crud import create_order


# def create_order_service(db: Session, order_data, user_id: int, background_tasks: BackgroundTasks = None):

#     if not order_data.items:
#         raise HTTPException(400, "Order items required")

#     total_amount = Decimal("0")

#     coupon = None
#     coupon_id = None
#     coupon_code = None

#     # =========================
#     # COUPON VALIDATION (ONLY VALIDATION, NOT APPLY)
#     # =========================
#     if order_data.coupon_code:

#         coupon = get_coupon_by_code(db, order_data.coupon_code)

#         if not coupon:
#             raise HTTPException(400, "Invalid coupon")

#         if not coupon.is_active:
#             raise HTTPException(400, "Coupon inactive")

#         now = datetime.now()

#         if coupon.start_date and now < coupon.start_date:
#             raise HTTPException(400, "Coupon not started")

#         if coupon.expiry_date and now > coupon.expiry_date:
#             raise HTTPException(400, "Coupon expired")

#         if coupon.usage_limit:
#             total_usage = get_coupon_usage_count(db, coupon.id)
#             if total_usage >= coupon.usage_limit:
#                 raise HTTPException(400, "Coupon limit reached")

#         user_usage = get_user_coupon_usage(db, coupon.id, user_id)
#         if user_usage >= coupon.usage_per_user:
#             raise HTTPException(400, "Coupon already used")

#     # =========================
#     # PRODUCT LOOP (APPLY BEST DISCOUNT)
#     # =========================
#     for item in order_data.items:

#         product = (
#             db.query(Product)
#             .filter(Product.id == item.product_id)
#             .with_for_update()
#             .first()
#         )

#         if not product:
#             raise HTTPException(404, "Product not found")

#         if product.stock < item.quantity:
#             raise HTTPException(400, f"{product.product_name} out of stock")

#         base_price = product.sale_price or product.regular_price

#         if base_price is None:
#             raise HTTPException(400, f"Price not set for {product.product_name}")

#         base_price = Decimal(base_price)

#         # 🔥 APPLY OFFER
#         offer_data = apply_offer(db, product)

#         # 🔥 APPLY BEST (COUPON vs OFFER)
#         best = apply_best_discount(
#             product=product,
#             coupon=coupon,
#             offer_data=offer_data
#         )

#         final_price = Decimal(best["final_price"])

#         total_amount += final_price * item.quantity

#     # =========================
#     # FINAL VALUES
#     # =========================
#     final_amount = total_amount
#     discount = Decimal("0")  # already applied in price

#     if coupon:
#         coupon_id = coupon.id
#         coupon_code = coupon.code

#     # =========================
#     # CREATE ORDER
#     # =========================
#     db_order = create_order(db, order_data, user_id)

#     db_order.discount_amount = float(discount)
#     db_order.final_amount = float(final_amount)
#     db_order.total_amount = float(final_amount)
#     db_order.coupon_id = coupon_id
#     db_order.coupon_code = coupon_code

#     # =========================
#     # PAYMENT UPDATE
#     # =========================
#     if db_order.payments and len(db_order.payments) > 0:
#         db_order.payments[0].amount = float(final_amount)

#     # =========================
#     # COUPON USAGE
#     # =========================
#     if coupon_id:
#         usage = CouponUsage(
#             coupon_id=coupon_id,
#             user_id=user_id,
#             order_id=db_order.id
#         )
#         db.add(usage)

#     db.commit()
#     db.refresh(db_order)

#     # =========================
#     # EMAIL
#     # =========================
#     if background_tasks:
#         user = db.query(User).filter(User.id == user_id).first()

#         if user and user.email:
#             background_tasks.add_task(
#                 send_order_email,
#                 user.email,
#                 user.name,
#                 db_order
#             )

#     return db_order

