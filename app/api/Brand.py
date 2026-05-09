from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.Brands_schema import BrandCreate, BrandOut, BrandUpdate
from app.Crud.Brand_Crud import (
    get_all_brands,
    get_brand_by_id,
    create_brand,
    update_brand,
    delete_brand,
)
from app.database import get_db

router = APIRouter(prefix="/brand", tags=["Brand"])


@router.get("/", response_model=list[BrandOut])
def get_brands(db: Session = Depends(get_db)):
    return get_all_brands(db)


@router.get("/{brand_id}", response_model=BrandOut)
def get_brand_by_id_api(brand_id: int, db: Session = Depends(get_db)):
    brand = get_brand_by_id(db, brand_id)
    if not brand:
        raise HTTPException(status_code=404, detail="Brand not found")
    return brand


@router.post("/add", response_model=BrandOut)
def insert_brand(brand: BrandCreate, db: Session = Depends(get_db)):
    return create_brand(db, brand)


@router.put("/update/{brand_id}", response_model=BrandOut)
def update_brand_api(
    brand_id: int,
    brand: BrandUpdate,
    db: Session = Depends(get_db),
):
    updated_brand = update_brand(db, brand_id, brand)
    if not updated_brand:
        raise HTTPException(status_code=404, detail="Brand not found")
    return updated_brand


@router.delete("/{brand_id}")
def remove_brand(brand_id: int, db: Session = Depends(get_db)):
    brand = get_brand_by_id(db, brand_id)
    if not brand:
        raise HTTPException(status_code=404, detail="Brand not found")

    delete_brand(db, brand)
    return {"message": "Brand deleted successfully"}
