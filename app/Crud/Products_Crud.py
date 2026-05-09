from sqlalchemy.orm import Session
from app.models.products import Product
from app.schemas.Products_schema import ProductCreate, ProductUpdate


def get_all_products(db: Session):
    return db.query(Product).all()


def get_product_by_id(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()


def create_product(db: Session, product: ProductCreate):
    db_product = Product(
        product_name=product.product_name,
        regular_price=product.regular_price,
        sale_price=product.sale_price,
        size=product.size,
        weight=product.weight,
        rating=product.rating,
        life=product.life,
        type=product.type,
        brand=product.brand,
        nutrition_energy_kcal=product.nutrition_energy_kcal,
        nutrition_protein_g=product.nutrition_protein_g,
        nutrition_magnetiam_kcal=product.nutrition_magnetiam_kcal,
        nutrition_calory_kcal=product.nutrition_calory_kcal,
        nutrition_vitamine_kcal=product.nutrition_vitamine_kcal,
        stock=product.stock,
        sku=product.sku,
        category=product.category,
        subcategory_id=product.subcategory_id,
        tag=product.tag,
        description=product.description,
        image=product.image,
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def update_product(db: Session, product_id: int, product: ProductUpdate):
    db_product = get_product_by_id(db, product_id)
    if not db_product:
        return None

    for key, value in product.model_dump(exclude_unset=True).items():
        setattr(db_product, key, value)

    db.commit()
    db.refresh(db_product)
    return db_product


def delete_product(db: Session, product: Product):
    db.delete(product)
    db.commit()
