from fastapi import APIRouter, Depends, HTTPException , UploadFile, File
from sqlalchemy.orm import Session
from app.dependencies.auth import get_current_user
from app.models.users import User  
import shutil, os, uuid


from app.schemas.user_schema import (
    UserCreate,
    UserLogin,
    UserUpdate,
    UserOut,
)
from app.Crud.User_Crud import (
    create_user,
    authenticate_user,
    get_user_by_id,
    update_user,
    get_all_users,
    delete_user,
)
from app.database import get_db
from app.core.utils import sanitize_filename

router = APIRouter(prefix="/users", tags=["Users"])

UPLOAD_DIR = "app/public/profile"

@router.post("/upload-profile/{user_id}")
def upload_profile_photo(
    user_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # 🔐 1. Auth check
    if current_user.id != user_id and getattr(current_user, "role", None) != "admin":
        raise HTTPException(403, "Not allowed")

    # 📦 2. Validate file type
    if not file.content_type.startswith("image/"):
        raise HTTPException(400, "Only image allowed")

    # 📏 3. File size limit (2MB)
    file.file.seek(0, 2)
    size = file.file.tell()
    file.file.seek(0)

    if size > 2 * 1024 * 1024:
        raise HTTPException(400, "File too large (max 2MB)")

    # 📁 4. Ensure folder exists
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    # 🔍 5. Safe extension
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in [".jpg", ".jpeg", ".png", ".webp"]:
        raise HTTPException(400, "Invalid image format")

    filename = sanitize_filename(file.filename)
    file_path = os.path.join(UPLOAD_DIR, filename)

    # 👤 6. Get user
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(404, "User not found")

    # 🗑️ 7. Delete old image
    if user.profile_photo:
        old_path = os.path.join(UPLOAD_DIR, user.profile_photo)
        if os.path.exists(old_path):
            os.remove(old_path)

    # 💾 8. Save new file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # 🧾 9. Update DB
    user.profile_photo = filename
    db.commit()
    db.refresh(user)

    return {
        "message": "Uploaded",
        "image_url": f"/public/profile/{filename}"
    }

@router.get("/", response_model=list[UserOut])
def get_users(db: Session = Depends(get_db)):
    return get_all_users(db)


@router.post("/register", response_model=UserOut)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db, user)


# @router.post("/login")
# def login_user(user: UserLogin, db: Session = Depends(get_db)):
#     db_user = authenticate_user(db, user.email, user.password)
#     if not db_user:
#         raise HTTPException(status_code=401, detail="Invalid credentials")

#     return {
#         "message": "Login successful",
#         "user_id": db_user.id,
#     }


@router.get("/{user_id}", response_model=UserOut)
def get_user_by_id_api(user_id: int, db: Session = Depends(get_db)):
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.patch("/update/{user_id}", response_model=UserOut)
def update_user_api(
    user_id: int,
    user: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.id != user_id and getattr(current_user, "role", None) != "admin":
        raise HTTPException(status_code=403, detail="Not allowed")

    updated_user = update_user(db, user_id, user)

    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")

    return updated_user


@router.delete("/{user_id}")
def remove_user(user_id: int, db: Session = Depends(get_db)):
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    delete_user(db, user)
    return {"message": "User deleted successfully"}
