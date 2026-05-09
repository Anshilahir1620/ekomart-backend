from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.products import Product
from app.models.categories import Category
from sqlalchemy import or_

router = APIRouter(prefix="/search", tags=["Search"])

@router.get("/")
def search(q: str, db: Session = Depends(get_db)):
    if not q:
        return {"products": [], "categories": []}
        
    products = db.query(Product).filter(
        or_(
            Product.product_name.ilike(f"%{q}%"),
            Product.description.ilike(f"%{q}%"),
            Product.tag.ilike(f"%{q}%")
        )
    ).limit(10).all()
    
    categories = db.query(Category).filter(
        Category.name.ilike(f"%{q}%")
    ).limit(5).all()
    
    return {
        "products": [
            {
                "id": p.id,
                "name": p.product_name,
                "image": p.image,
                "price": p.sale_price or p.regular_price,
                "category": p.category
            } for p in products
        ],
        "categories": [
            {
                "id": c.id,
                "name": c.name,
                "image": c.image,
                "slug": c.slug
            } for c in categories
        ]
    }
