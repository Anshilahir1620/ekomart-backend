# app/schemas/payment_schema.py

from pydantic import BaseModel

class PaymentCreate(BaseModel):
    order_id: int
    payment_method: str
    amount: float


class PaymentOut(BaseModel):
    id: int
    order_id: int
    payment_status: str
    payment_method: str
    amount: float

    class Config:
        from_attributes = True


class PaymentUpdate(BaseModel):
    order_id: int
    status: str
    transaction_id: str | None = None


class RazorpayOrderCreate(BaseModel):
    order_id: int


class RazorpayOrderResponse(BaseModel):
    razorpay_order_id: str
    amount: int
    currency: str
    order_id: int


class RazorpayVerify(BaseModel):
    order_id: int
    razorpay_order_id: str
    razorpay_payment_id: str
    razorpay_signature: str