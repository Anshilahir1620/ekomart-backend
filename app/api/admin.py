from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.user_schema import  AdminCreate
from app.database import get_db
from app.Crud.User_Crud import create_admin_user


router = APIRouter(prefix="/admin", tags=["Admin"])

@router.post("/create-user")
def create_user_by_admin(
    user_data: AdminCreate,
    db: Session = Depends(get_db),
):
    return create_admin_user(db, user_data)