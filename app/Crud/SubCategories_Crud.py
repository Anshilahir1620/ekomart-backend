from sqlalchemy.orm import Session
from app.models.subcategories import SubCategory
from app.schemas.subcategory_schema import SubCategoryCreate, SubCategoryUpdate


def get_all_subcategory(db: Session):
    return db.query(SubCategory).all()


def get_subcategory_by_id(db: Session, subcategory_id: int):
    return db.query(SubCategory).filter(SubCategory.id == subcategory_id).first()


def create_subcategory(db: Session, subcategory: SubCategoryCreate):
    db_subcategory = SubCategory(
        name=subcategory.name,
        slug=subcategory.slug,
        category_id=subcategory.category_id,
        status=1,
    )
    db.add(db_subcategory)
    db.commit()
    db.refresh(db_subcategory)
    return db_subcategory


def update_subcategory(
    db: Session,
    subcategory_id: int,
    subcategory: SubCategoryUpdate,
):
    db_subcategory = get_subcategory_by_id(db, subcategory_id)
    if not db_subcategory:
        return None

    for key, value in subcategory.model_dump(exclude_unset=True).items():
        setattr(db_subcategory, key, value)

    db.commit()
    db.refresh(db_subcategory)
    return db_subcategory


def delete_subcategory(db: Session, subcategory: SubCategory):
    db.delete(subcategory)
    db.commit()
