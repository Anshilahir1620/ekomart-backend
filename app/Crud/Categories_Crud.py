from sqlalchemy.orm import Session
from app.models.categories import Category
from app.schemas.category_schema import CategoryCreate, CategoryUpdate


def get_all_categories(db: Session):
    return db.query(Category).all()


def get_category_by_id(db: Session, category_id: int):
    return db.query(Category).filter(Category.id == category_id).first()


def create_category(db: Session, category: CategoryCreate):
    db_category = Category(
        name=category.name,
        slug=category.slug,
        image=category.image,
        status=category.status if category.status is not None else 1
    )
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


def update_category(db: Session, category_id: int, category: CategoryUpdate):
    db_category = get_category_by_id(db, category_id)
    if not db_category:
        return None

    for key, value in category.model_dump(exclude_unset=True).items():
        setattr(db_category, key, value)

    db.commit()
    db.refresh(db_category)
    return db_category


def delete_category(db: Session, category: Category):
    db.delete(category)
    db.commit()
