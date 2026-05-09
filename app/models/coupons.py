from sqlalchemy import Column, Integer, String, DECIMAL, Boolean, DateTime, TIMESTAMP, ForeignKey, func
from sqlalchemy.orm import relationship
from app.database import Base


class Coupon(Base):
    __tablename__ = "coupons"

    id = Column(Integer, primary_key=True, index=True)

    code = Column(String(50), unique=True, nullable=False, index=True)

    discount_type = Column(String(20), nullable=False)  
    discount_value = Column(DECIMAL(10, 2), nullable=False)

    min_order_amount = Column(DECIMAL(10, 2), server_default="0")
    max_discount_amount = Column(DECIMAL(10, 2), nullable=True)

    usage_limit = Column(Integer, nullable=True)
    usage_per_user = Column(Integer, server_default="1")

    start_date = Column(DateTime)
    expiry_date = Column(DateTime)

    is_active = Column(Boolean, server_default="1")

    created_at = Column(TIMESTAMP, server_default=func.now())


class CouponUsage(Base):
    __tablename__ = "coupon_usages"

    id = Column(Integer, primary_key=True, index=True)

    coupon_id = Column(Integer, ForeignKey("coupons.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)

    used_at = Column(TIMESTAMP, server_default=func.now())

    coupon = relationship("Coupon")
    user = relationship("User")
    order = relationship("Order")