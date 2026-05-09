from fastapi import APIRouter, Depends, HTTPException, Form, File, UploadFile
import os
import shutil
import uuid
from sqlalchemy.orm import Session

from app.schemas.category_schema import CategoryCreate, CategoryOut, CategoryUpdate
from app.Crud.Categories_Crud import (
    get_all_categories,
    get_category_by_id,
    create_category,
    update_category,
    delete_category,
)
from app.database import get_db
from app.core.utils import sanitize_filename

router = APIRouter(prefix="/category", tags=["Category"])


@router.get("/", response_model=list[CategoryOut])
def get_categories(db: Session = Depends(get_db)):
    return get_all_categories(db)


@router.get("/{category_id}", response_model=CategoryOut)
def get_category_by_id_api(category_id: int, db: Session = Depends(get_db)):
    category = get_category_by_id(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@router.post("/add", response_model=CategoryOut)
def insert_category(
    name: str = Form(...),
    slug: str = Form(None),
    status: int = Form(1),
    image: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    filename = None
    if image and image.filename:
        os.makedirs("app/public/categories", exist_ok=True)
        
        # 🔍 Safe extension
        ext = os.path.splitext(image.filename)[1].lower()
        if ext not in [".jpg", ".jpeg", ".png", ".webp"]:
            raise HTTPException(400, "Invalid image format")
            
        filename = sanitize_filename(image.filename)
        file_path = os.path.join("app/public/categories", filename)
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)

    category_data = CategoryCreate(name=name, slug=slug, status=status, image=filename)
    return create_category(db, category_data)


@router.put("/update/{category_id}", response_model=CategoryOut)
def update_category_api(
    category_id: int,
    name: str = Form(None),
    slug: str = Form(None),
    status: int = Form(None),
    image: UploadFile = File(None),
    db: Session = Depends(get_db),
):
    db_category = get_category_by_id(db, category_id)
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")

    filename = db_category.image
    if image and image.filename:
        # 📁 Ensure folder exists
        os.makedirs("app/public/categories", exist_ok=True)
        
        # 🔍 Safe extension
        ext = os.path.splitext(image.filename)[1].lower()
        if ext not in [".jpg", ".jpeg", ".png", ".webp"]:
            raise HTTPException(400, "Invalid image format")
            
        # 🗑️ Delete old image
        if db_category.image:
            old_path = os.path.join("app/public/categories", db_category.image)
            if os.path.exists(old_path):
                try:
                    os.remove(old_path)
                except:
                    pass

        filename = sanitize_filename(image.filename)
        file_path = os.path.join("app/public/categories", filename)
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)

    category_data = CategoryUpdate(
        name=name if name is not None else db_category.name,
        slug=slug if slug is not None else db_category.slug,
        status=status if status is not None else db_category.status,
        image=filename
    )
    
    updated_category = update_category(db, category_id, category_data)
    return updated_category


@router.delete("/{category_id}")
def remove_category(category_id: int, db: Session = Depends(get_db)):
    category = get_category_by_id(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    delete_category(db, category)
    return {"message": "Category deleted successfully"}
