from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.daily_offer import DailyOffer
from app.models.categories import Category
from app.models.products import Product
from app.database import get_db
from app.services.offer_service import apply_offer
from datetime import datetime


from app.schemas.daily_offer_schema import (
    DailyOfferCreate,
    DailyOfferOut,
    TodayOfferOut
)
from app.Crud.daily_offer_crud import (
    create_offer,
    get_all_offers,
    delete_offer,
    get_offer_by_id
)

from app.dependencies.auth import get_current_user
from app.models.users import User


router = APIRouter(
    prefix="/offers",
    tags=["Daily Offers"]
)


# =========================
# COMMON ADMIN CHECK
# =========================
def validate_admin(current_user):
    role_name = getattr(current_user.role,"role_name","").lower()

    if role_name != "admin":
        raise HTTPException(status_code=403,detail="Not authorized")


# =========================
# CREATE OFFER
# =========================
@router.post("/", response_model=DailyOfferOut)
def create_offer_api(
    offer: DailyOfferCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    validate_admin(current_user)

    try:
        return create_offer(db, offer)

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )




@router.get("/today", response_model=list[TodayOfferOut])
def get_today_offers(db: Session = Depends(get_db)):

    now = datetime.now()

    offers = db.query(DailyOffer).filter(
        DailyOffer.is_active == True,
        DailyOffer.start_date <= now,
        DailyOffer.end_date >= now
    ).all()

    result = []

    for offer in offers:

        category = db.query(Category).filter(
            Category.id == offer.category_id
        ).first()

        if not category:
            continue

        products = db.query(Product).filter(
            Product.category == category.name
        ).all()

        product_list = []

        from app.services.pricing_helper import calculate_item_price

        for product in products:
            pricing = calculate_item_price(db, product)

            product_list.append({
                "id": product.id,
                "product_name": product.product_name,
                "image": product.image,
                "regular_price": pricing["original_price"],
                "sale_price": pricing["base_price"],
                "final_price": pricing["final_price"],
                "discount": pricing["offer_discount"]
            })

        result.append({
            "category_id": category.id,
            "category_name": category.name,
            "category_slug": category.slug,
            "category_image": category.image,
            "offer_type": offer.discount_type,
            "offer_value": float(offer.discount_value),
            "products": product_list
        })

    return result





# =========================
# GET ALL OFFERS
# =========================
@router.get("/", response_model=list[DailyOfferOut])
def get_offers_api(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    validate_admin(current_user)

    return get_all_offers(db)


# =========================
# GET SINGLE OFFER
# =========================
@router.get("/{offer_id}", response_model=DailyOfferOut)
def get_offer_api(
    offer_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    validate_admin(current_user)

    offer = get_offer_by_id(db, offer_id)

    if not offer:
        raise HTTPException(
            status_code=404,
            detail="Offer not found"
        )

    return offer


# =========================
# UPDATE OFFER
# =========================
@router.put("/{offer_id}", response_model=DailyOfferOut)
def update_offer_api(
    offer_id: int,
    offer: DailyOfferCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    validate_admin(current_user)

    db_offer = get_offer_by_id(db, offer_id)

    if not db_offer:
        raise HTTPException(
            status_code=404,
            detail="Offer not found"
        )

    try:
        update_data = offer.dict()

        for key, value in update_data.items():
            setattr(db_offer, key, value)

        db.commit()
        db.refresh(db_offer)

        return db_offer

    except Exception as e:
        db.rollback()

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


# =========================
# DELETE OFFER
# =========================
@router.delete("/{offer_id}")
def delete_offer_api(
    offer_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    validate_admin(current_user)

    deleted = delete_offer(db, offer_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Offer not found"
        )

    return {
        "message": "Offer deleted successfully"
    }