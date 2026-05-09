from sqlalchemy.orm import Session
from app.models.brands import Brand
from app.schemas.Brands_schema import BrandCreate, BrandUpdate


def get_all_brands(db: Session):
    return db.query(Brand).all()


def get_brand_by_id(db: Session, brand_id: int):
    return db.query(Brand).filter(Brand.id == brand_id).first()


def create_brand(db: Session, brand: BrandCreate):
    db_brand = Brand(
        name=brand.name,
        logo=brand.logo,
        status=1
    )
    db.add(db_brand)
    db.commit()
    db.refresh(db_brand)
    return db_brand


def update_brand(db: Session, brand_id: int, brand: BrandUpdate):
    db_brand = get_brand_by_id(db, brand_id)
    if not db_brand:
        return None

    for key, value in brand.model_dump(exclude_unset=True).items():
        setattr(db_brand, key, value)

    db.commit()
    db.refresh(db_brand)
    return db_brand


def delete_brand(db: Session, brand: Brand):
    db.delete(brand)
    db.commit()
