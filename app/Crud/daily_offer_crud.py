from sqlalchemy.orm import Session
from datetime import datetime, timezone
from app.models.daily_offer import DailyOffer


def create_offer(db: Session, offer):
    # 🔥 prevent overlapping offers (same category + active period)
    existing = db.query(DailyOffer).filter(
        DailyOffer.category_id == offer.category_id,
        DailyOffer.is_active == True,
        DailyOffer.start_date <= offer.end_date,
        DailyOffer.end_date >= offer.start_date
    ).first()

    if existing:
        raise Exception("An active offer already exists for this category in given date range")

    db_offer = DailyOffer(**offer.dict())
    db.add(db_offer)
    db.commit()
    db.refresh(db_offer)
    return db_offer


def get_all_offers(db: Session):
    return db.query(DailyOffer).all()


def get_offer_by_id(db: Session, offer_id: int):
    return db.query(DailyOffer).filter(DailyOffer.id == offer_id).first()


def delete_offer(db: Session, offer_id: int):
    offer = get_offer_by_id(db, offer_id)
    if offer:
        db.delete(offer)
        db.commit()
    return offer


# 🔥 CORE FUNCTION (FIXED)
def get_active_offer_by_category(db: Session, category_id: int):
    now = datetime.now(timezone.utc)  # ✅ FIXED

    return db.query(DailyOffer).filter(
        DailyOffer.category_id == category_id,
        DailyOffer.is_active == True,
        DailyOffer.start_date <= now,
        DailyOffer.end_date >= now
    ).order_by(DailyOffer.id.desc()).first()