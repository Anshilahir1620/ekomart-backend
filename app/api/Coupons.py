from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.Coupons_schema import (
    CouponCreate,
    ApplyCouponRequest,
    CouponUpdate
)
from app.services.coupons_services import apply_coupon, create_coupon_service
from app.Crud.Coupons_Crud import (
    get_all_coupons,
    update_coupon,
    deactivate_coupon
)

router = APIRouter(prefix="/coupon", tags=["Coupon"])


# =========================
# APPLY COUPON
# =========================
@router.post("/apply")
def apply_coupon_api(data: ApplyCouponRequest, db: Session = Depends(get_db)):
    return apply_coupon(db, data)


# =========================
# CREATE COUPON
# =========================
@router.post("/")
def create_coupon_api(data: CouponCreate, db: Session = Depends(get_db)):
    return create_coupon_service(db, data)


# =========================
# GET ALL
# =========================
@router.get("/")
def get_coupons_api(db: Session = Depends(get_db)):
    return get_all_coupons(db)


# =========================
# UPDATE
# =========================
@router.put("/{coupon_id}")
def update_coupon_api(coupon_id: int, data: CouponUpdate, db: Session = Depends(get_db)):
    coupon = update_coupon(db, coupon_id, data.model_dump(exclude_unset=True))

    if not coupon:
        raise HTTPException(status_code=404, detail="Coupon not found")

    return coupon


# =========================
# DEACTIVATE
# =========================
@router.patch("/{coupon_id}/deactivate")
def deactivate_coupon_api(coupon_id: int, db: Session = Depends(get_db)):
    coupon = deactivate_coupon(db, coupon_id)

    if not coupon:
        raise HTTPException(status_code=404, detail="Coupon not found")

    return {"message": "Coupon deactivated"}