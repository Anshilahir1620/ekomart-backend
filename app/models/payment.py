# app/models/payment.py

from sqlalchemy import Column, Integer, String, DECIMAL ,Enum, TIMESTAMP, ForeignKey, text
from app.database import Base
import enum

class PaymentMethod(enum.Enum):
    UPI = "UPI"
    CARD = "CARD"
    COD = "COD"

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)

    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"))

    payment_method = Column(Enum(PaymentMethod), nullable=False) 
    payment_status = Column(String(50), default="PENDING")

    transaction_id = Column(String(255), nullable=True)
    payment_gateway = Column(String(100), nullable=True)

    razorpay_order_id = Column(String(255), nullable=True)
    razorpay_payment_id = Column(String(255), nullable=True)
    razorpay_signature = Column(String(255), nullable=True)

    amount = Column(DECIMAL(10, 2), nullable=False)

    created_at = Column(
        TIMESTAMP,
        server_default=text("CURRENT_TIMESTAMP")
    )

    updated_at = Column(
        TIMESTAMP,
        server_default=text("CURRENT_TIMESTAMP"),
        onupdate=text("CURRENT_TIMESTAMP")
    )