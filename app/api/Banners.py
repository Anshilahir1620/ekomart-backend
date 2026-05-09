from fastapi import APIRouter, Depends, HTTPException, Form, File, UploadFile
import os
import shutil
from sqlalchemy.orm import Session

from app.schemas.Banner_schema import BannerCreate, BannerOut, BannerUpdate
from app.Crud.Banners_Crud import (
    get_all_banners,
    get_banner_by_id,
    create_banner,
    update_banner,
    delete_banner,
)
from app.database import get_db
from app.core.utils import sanitize_filename

router = APIRouter(prefix="/banner", tags=["Banner"])


@router.get("/", response_model=list[BannerOut])
def get_banners(db: Session = Depends(get_db)):
    return get_all_banners(db)


@router.get("/{banner_id}", response_model=BannerOut)
def get_banner_by_id_api(banner_id: int, db: Session = Depends(get_db)):
    banner = get_banner_by_id(db, banner_id)
    if not banner:
        raise HTTPException(status_code=404, detail="Banner not found")
    return banner


@router.post("/add", response_model=BannerOut)
def create_banner_api(
    badge: str = Form(None),
    title1: str = Form(...),
    highlight: str = Form(None),
    title2: str = Form(None),
    desc1: str = Form(None),
    desc2: str = Form(None),
    alt: str = Form(None),
    image: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    filename = ""
    if image and image.filename:
        os.makedirs("app/public/banners", exist_ok=True)
        filename = sanitize_filename(image.filename)
        file_path = os.path.join("app/public/banners", filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)

    banner_data = BannerCreate(
        badge=badge,
        title1=title1,
        highlight=highlight,
        title2=title2,
        desc1=desc1,
        desc2=desc2,
        alt=alt,
        image=filename
    )
    
    db_banner = create_banner(db, banner_data)
    db.commit()
    db.refresh(db_banner)
    return db_banner


@router.put("/update/{banner_id}", response_model=BannerOut)
def update_banner_api(
    banner_id: int,
    badge: str = Form(None),
    title1: str = Form(None),
    highlight: str = Form(None),
    title2: str = Form(None),
    desc1: str = Form(None),
    desc2: str = Form(None),
    alt: str = Form(None),
    image: UploadFile = File(None),
    db: Session = Depends(get_db),
):
    db_banner = get_banner_by_id(db, banner_id)
    if not db_banner:
        raise HTTPException(status_code=404, detail="Banner not found")

    filename = db_banner.image
    if image and image.filename:
        os.makedirs("app/public/banners", exist_ok=True)
        
        # Delete old image if exists
        if db_banner.image:
            old_path = os.path.join("app/public/banners", db_banner.image)
            if os.path.exists(old_path):
                try:
                    os.remove(old_path)
                except:
                    pass
        
        filename = sanitize_filename(image.filename)
        file_path = os.path.join("app/public/banners", filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)

    banner_update_data = BannerUpdate(
        badge=badge if badge is not None else db_banner.badge,
        title1=title1 if title1 is not None else db_banner.title1,
        highlight=highlight if highlight is not None else db_banner.highlight,
        title2=title2 if title2 is not None else db_banner.title2,
        desc1=desc1 if desc1 is not None else db_banner.desc1,
        desc2=desc2 if desc2 is not None else db_banner.desc2,
        alt=alt if alt is not None else db_banner.alt,
        image=filename
    )

    updated_banner = update_banner(db, banner_id, banner_update_data)
    db.commit()
    db.refresh(updated_banner)
    return updated_banner


@router.delete("/{banner_id}")
def remove_banner(banner_id: int, db: Session = Depends(get_db)):
    banner = get_banner_by_id(db, banner_id)
    if not banner:
        raise HTTPException(status_code=404, detail="Banner not found")
    delete_banner(db, banner)
    db.commit()
    return {"message": "Banner deleted successfully"}
