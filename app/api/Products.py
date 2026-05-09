from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.Products_schema import ProductCreate, ProductOut, ProductUpdate
from app.Crud.Products_Crud import (
    get_all_products,
    get_product_by_id,
    create_product,
    update_product,
    delete_product,
)

from app.database import get_db
from app.services.pricing_helper import calculate_item_price

router = APIRouter(prefix="/product", tags=["Product"])


def build_product_response(product, db):
    pricing = calculate_item_price(db, product)

    data = product.__dict__.copy()

    # Sync pricing fields
    data.update(pricing)
    
    # Keep some legacy compatibility if needed
    data["discount"] = pricing["offer_discount"]

    return data


@router.get("/", response_model=list[ProductOut])
def get_products(db: Session = Depends(get_db)):
    products = get_all_products(db)
    return [build_product_response(p, db) for p in products]


@router.get("/{product_id}", response_model=ProductOut)
def get_product_by_id_api(product_id: int, db: Session = Depends(get_db)):
    product = get_product_by_id(db, product_id)

    if not product:
        raise HTTPException(404, "Product not found")

    return build_product_response(product, db)


@router.post("/add", response_model=ProductOut)
def add_product(product: ProductCreate, db: Session = Depends(get_db)):
    created = create_product(db, product)
    return build_product_response(created, db)


@router.put("/update/{product_id}", response_model=ProductOut)
def update_product_api(
    product_id: int,
    product: ProductUpdate,
    db: Session = Depends(get_db),
):
    updated = update_product(db, product_id, product)

    if not updated:
        raise HTTPException(404, "Product not found")

    return build_product_response(updated, db)


@router.delete("/{product_id}")
def remove_product(product_id: int, db: Session = Depends(get_db)):
    product = get_product_by_id(db, product_id)

    if not product:
        raise HTTPException(404, "Product not found")

    delete_product(db, product)

    return {"message": "Product deleted successfully"}