from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.subcategory_schema import (
    SubCategoryCreate,
    SubCategoryOut,
    SubCategoryUpdate,
)
from app.Crud.SubCategories_Crud import (
    get_all_subcategory,
    get_subcategory_by_id,
    create_subcategory,
    update_subcategory,
    delete_subcategory,
)
from app.database import get_db

router = APIRouter(prefix="/subcategory", tags=["SubCategory"])


@router.get("/", response_model=list[SubCategoryOut])
def get_subcategories(db: Session = Depends(get_db)):
    return get_all_subcategory(db)


@router.get("/{subcategory_id}", response_model=SubCategoryOut)
def get_subcategory_by_id_api(
    subcategory_id: int,
    db: Session = Depends(get_db),
):
    subcategory = get_subcategory_by_id(db, subcategory_id)
    if not subcategory:
        raise HTTPException(status_code=404, detail="SubCategory not found")
    return subcategory


@router.post("/add", response_model=SubCategoryOut)
def insert_subcategory(
    subcategory: SubCategoryCreate,
    db: Session = Depends(get_db),
):
    return create_subcategory(db, subcategory)


@router.put("/update/{subcategory_id}", response_model=SubCategoryOut)
def update_subcategory_api(
    subcategory_id: int,
    subcategory: SubCategoryUpdate,
    db: Session = Depends(get_db),
):
    updated_subcategory = update_subcategory(db, subcategory_id, subcategory)
    if not updated_subcategory:
        raise HTTPException(status_code=404, detail="SubCategory not found")
    return updated_subcategory


@router.delete("/{subcategory_id}")
def remove_subcategory(
    subcategory_id: int,
    db: Session = Depends(get_db),
):
    subcategory = get_subcategory_by_id(db, subcategory_id)
    if not subcategory:
        raise HTTPException(status_code=404, detail="SubCategory not found")

    delete_subcategory(db, subcategory)
    return {"message": "SubCategory deleted successfully"}
