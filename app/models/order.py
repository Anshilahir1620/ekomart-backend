from sqlalchemy import Column, Integer, DECIMAL, String,TIMESTAMP, ForeignKey, text, Text
from sqlalchemy.orm import relationship
from app.database import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)

    total_amount = Column(DECIMAL(10, 2), nullable=False)
    final_amount = Column(DECIMAL(10, 2), nullable=False)

    discount_amount = Column(DECIMAL(10, 2), server_default="0")

    status = Column(String(50), server_default="PENDING")

    shipping_name = Column(String(100), nullable=True)
    shipping_phone = Column(String(20), nullable=True)
    shipping_address = Column(Text, nullable=True)
    shipping_city = Column(String(100), nullable=True)
    shipping_state = Column(String(100), nullable=True)
    shipping_pincode = Column(String(20), nullable=True)

    created_at = Column(
        TIMESTAMP,
        server_default=text("CURRENT_TIMESTAMP")
    )

    coupon_id = Column(Integer, ForeignKey("coupons.id"), nullable=True)
    coupon_code = Column(String(50), nullable=True)

    items = relationship(
        "OrderItem",
        back_populates="order",
        cascade="all, delete"
    )

    payments = relationship(
        "Payment",
        backref="order",
        cascade="all, delete"
    )

    coupon = relationship("Coupon")


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)

    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)

    quantity = Column(Integer, nullable=False)
    price = Column(DECIMAL(10, 2), nullable=False)

    order = relationship("Order", back_populates="items")
    product = relationship("Product")
