# app/crud/payment_crud.py

from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException
from app.models.payment import Payment
import razorpay
import os


def get_razorpay_client():
    key = os.getenv("RAZORPAY_KEY")
    secret = os.getenv("RAZORPAY_SECRET")

    if not key or not secret:
        raise HTTPException(
            status_code=500,
            detail="Razorpay credentials not configured in backend .env"
        )

    if key.startswith("rzp_live_"):
         raise HTTPException(
            status_code=403,
            detail="CRITICAL SAFETY: Razorpay LIVE keys are blocked. Use TEST mode keys only."
        )

    if not key.startswith("rzp_test_"):
        raise HTTPException(
            status_code=403,
            detail="CRITICAL SAFETY: Razorpay must be in TEST MODE (key should start with rzp_test_)."
        )

    return razorpay.Client(auth=(key, secret))


def get_payment_by_order(db: Session, order_id: int):
    return (
        db.query(Payment)
        .options(joinedload(Payment.order))
        .filter(Payment.order_id == order_id)
        .first()
    )


def get_payment_by_razorpay_order(db: Session, razorpay_order_id: str):
    return (
        db.query(Payment)
        .options(joinedload(Payment.order))
        .filter(Payment.razorpay_order_id == razorpay_order_id)
        .first()
    )


def create_razorpay_order(db: Session, payment: Payment):
    try:
        amount = int(payment.amount * 100)  # paise

        client = get_razorpay_client()
        order = client.order.create({
            "amount": amount,
            "currency": "INR",
            "payment_capture": 1
        })

        payment.razorpay_order_id = order["id"]
        payment.payment_status = "created"  # Updated status
        payment.payment_gateway = "RAZORPAY"

        db.commit()
        db.refresh(payment)

        return {
            "razorpay_order_id": order["id"],
            "amount": amount,
            "currency": "INR",
            "order_id": payment.order_id
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


# ✅ SAVE SUCCESS
def save_payment_success(
    db: Session,
    payment: Payment,
    razorpay_order_id: str,
    razorpay_payment_id: str,
    razorpay_signature: str
):
    try:
        if payment.payment_status == "paid":
            return payment

        payment.payment_status = "paid"
        payment.razorpay_order_id = razorpay_order_id
        payment.razorpay_payment_id = razorpay_payment_id
        payment.razorpay_signature = razorpay_signature
        payment.transaction_id = razorpay_payment_id
        payment.payment_gateway = "RAZORPAY"

        payment.order.status = "CONFIRMED"

        db.commit()
        db.refresh(payment)

        return payment

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))