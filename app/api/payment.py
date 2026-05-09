# app/api/payment.py

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
import hmac
import hashlib
import json
import os

from app.database import get_db
from app.dependencies.auth import get_current_user
from app.models.users import User

from app.schemas.Payment_schema import (
    PaymentOut,
    RazorpayOrderCreate,
    RazorpayOrderResponse,
    RazorpayVerify
)

from app.Crud.Payment_Crud import (
    get_payment_by_order,
    create_razorpay_order,
    save_payment_success,
    get_payment_by_razorpay_order
)

router = APIRouter(prefix="/payments", tags=["Payments"])


@router.post("/razorpay/create", response_model=RazorpayOrderResponse)
def create_order(
    data: RazorpayOrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    payment = get_payment_by_order(db, data.order_id)

    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")

    if payment.order.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed")

    return create_razorpay_order(db, payment)


# ✅ VERIFY PAYMENT
@router.post("/razorpay/verify", response_model=PaymentOut)
def verify_payment(
    data: RazorpayVerify,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    payment = get_payment_by_order(db, data.order_id)

    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")

    if payment.order.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed")

    secret = os.getenv("RAZORPAY_SECRET")
    if not secret:
        raise HTTPException(status_code=500, detail="Razorpay secret not configured")

    body = f"{data.razorpay_order_id}|{data.razorpay_payment_id}"

    generated_signature = hmac.new(
        bytes(secret, "utf-8"),
        bytes(body, "utf-8"),
        hashlib.sha256
    ).hexdigest()

    if generated_signature != data.razorpay_signature:
        raise HTTPException(status_code=400, detail="Invalid signature")

    return save_payment_success(
        db,
        payment,
        data.razorpay_order_id,
        data.razorpay_payment_id,
        data.razorpay_signature
    )


# ✅ WEBHOOK
@router.post("/razorpay/webhook")
async def razorpay_webhook(
    request: Request,
    db: Session = Depends(get_db)
):
    payload = await request.body()
    signature = request.headers.get("X-Razorpay-Signature")
    secret = os.getenv("RAZORPAY_WEBHOOK_SECRET")

    if not signature or not secret:
        raise HTTPException(status_code=400, detail="Missing signature or secret")

    # Verify signature
    generated_signature = hmac.new(
        bytes(secret, "utf-8"),
        payload,
        hashlib.sha256
    ).hexdigest()

    if generated_signature != signature:
        raise HTTPException(status_code=400, detail="Invalid webhook signature")

    data = json.loads(payload)
    event = data.get("event")

    if event == "payment.captured":
        payment_data = data["payload"]["payment"]["entity"]
        razorpay_order_id = payment_data.get("order_id")
        razorpay_payment_id = payment_data.get("id")
        razorpay_signature = "WEBHOOK_VERIFIED"  # Signature not usually needed for webhook if body is verified

        # Find payment by razorpay_order_id
        payment = get_payment_by_razorpay_order(db, razorpay_order_id)
        if payment:
             save_payment_success(
                db,
                payment,
                razorpay_order_id,
                razorpay_payment_id,
                razorpay_signature
            )

    return {"status": "ok"}


# ✅ GET PAYMENT
@router.get("/{order_id}", response_model=PaymentOut)
def get_payment(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    payment = get_payment_by_order(db, order_id)

    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")

    if payment.order.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed")

    return payment