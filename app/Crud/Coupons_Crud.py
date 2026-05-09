from sqlalchemy.orm import Session
from app.models.coupons import CouponUsage, Coupon


# =========================
# CREATE
# =========================
def create_coupon(db: Session, coupon_data):
    db_coupon = Coupon(**coupon_data.model_dump())

    db.add(db_coupon)
    db.commit()
    db.refresh(db_coupon)

    return db_coupon


# =========================
# READ
# =========================
def get_coupon_by_code(db: Session, code: str):
    return db.query(Coupon).filter(Coupon.code == code).first()


def get_all_coupons(db: Session):
    return db.query(Coupon).order_by(Coupon.id.desc()).all()


# =========================
# USAGE TRACKING
# =========================
def get_coupon_usage_count(db: Session, coupon_id: int):
    return db.query(CouponUsage).filter(
        CouponUsage.coupon_id == coupon_id
    ).count()


def get_user_coupon_usage(db: Session, coupon_id: int, user_id: int):
    return db.query(CouponUsage).filter(
        CouponUsage.coupon_id == coupon_id,
        CouponUsage.user_id == user_id
    ).count()


def create_coupon_usage(db: Session, coupon_id: int, user_id: int, order_id: int):
    usage = CouponUsage(
        coupon_id=coupon_id,
        user_id=user_id,
        order_id=order_id
    )

    db.add(usage)
    db.commit()
    db.refresh(usage)

    return usage


# =========================
# UPDATE
# =========================
def update_coupon(db: Session, coupon_id: int, data: dict):
    coupon = db.query(Coupon).filter(Coupon.id == coupon_id).first()

    if not coupon:
        return None

    allowed_fields = [
        "code",
        "discount_type",
        "discount_value",
        "min_order_amount",
        "max_discount_amount",
        "usage_limit",
        "usage_per_user",
        "start_date",
        "expiry_date",
        "is_active"
    ]

    for key, value in data.items():
        if key in allowed_fields:
            setattr(coupon, key, value)

    db.commit()
    db.refresh(coupon)

    return coupon


# =========================
# SOFT DELETE
# =========================
def deactivate_coupon(db: Session, coupon_id: int):
    coupon = db.query(Coupon).filter(Coupon.id == coupon_id).first()

    if not coupon:
        return None

    coupon.is_active = False

    db.commit()
    db.refresh(coupon)

    return coupon