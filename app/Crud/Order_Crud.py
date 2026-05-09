from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload
from decimal import Decimal

from app.models.order import Order, OrderItem
from app.models.payment import Payment
from app.models.products import Product
from app.schemas.Order_Schema import OrderCreate


def create_order(db: Session, order_data: OrderCreate, user_id: int):
    try:
        if not order_data.items:
            raise HTTPException(400, "Order items cannot be empty")

        db_order = Order(
            user_id=user_id,
            total_amount=0,
            status="PENDING",
            shipping_name=order_data.shipping_name,
            shipping_phone=order_data.shipping_phone,
            shipping_address=order_data.shipping_address,
            shipping_city=order_data.shipping_city,
            shipping_state=order_data.shipping_state,
            shipping_pincode=order_data.shipping_pincode
        )

        db.add(db_order)
        db.flush()

        total_amount = Decimal("0")

        for item in order_data.items:
            product = (
                db.query(Product)
                .filter(Product.id == item.product_id)
                .with_for_update()
                .first()
            )

            if not product:
                raise HTTPException(404, "Product not found")

            if product.stock < item.quantity:
                raise HTTPException(
                    400,
                    f"{product.product_name} out of stock"
                )

            price = product.sale_price or product.regular_price

            if price is None:
                raise HTTPException(
                    400,
                    f"Price not set for {product.product_name}"
                )

            price = Decimal(str(price))

            db_item = OrderItem(
                order_id=db_order.id,
                product_id=item.product_id,
                quantity=item.quantity,
                price=price
            )

            db.add(db_item)

            total_amount += price * item.quantity
            product.stock -= item.quantity

        db_order.total_amount = float(total_amount)

        payment_method = order_data.payment_method.value

        db_payment = Payment(
            order_id=db_order.id,
            payment_method=payment_method,
            payment_status="pending",
            amount=float(total_amount),
            payment_gateway="RAZORPAY" if payment_method != "COD" else "COD"
        )

        db.add(db_payment)

        db.commit()
        db.refresh(db_order)

        return db_order

    except HTTPException:
        db.rollback()
        raise

    except Exception as e:
        db.rollback()
        raise HTTPException(500, str(e))


def get_order_by_id(db: Session, order_id: int):
    return (
        db.query(Order)
        .options(
            joinedload(Order.items).joinedload(OrderItem.product),
            joinedload(Order.payments)
        )
        .filter(Order.id == order_id)
        .first()
    )


def get_orders_by_user(db: Session, user_id: int):
    return (
        db.query(Order)
        .options(
            joinedload(Order.items).joinedload(OrderItem.product),
            joinedload(Order.payments)
        )
        .filter(Order.user_id == user_id)
        .order_by(Order.id.desc())
        .all()
    )


def get_all_orders(db: Session):
    return (
        db.query(Order)
        .options(
            joinedload(Order.items).joinedload(OrderItem.product),
            joinedload(Order.payments)
        )
        .order_by(Order.id.desc())
        .all()
    )