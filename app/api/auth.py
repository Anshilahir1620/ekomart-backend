from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import jwt, JWTError

from app.database import get_db
from app.Crud.User_Crud import authenticate_user
from app.core.security import (
    create_access_token,
    create_refresh_token,
    SECRET_KEY,
    ALGORITHM
)

from pydantic import BaseModel

router = APIRouter(prefix="/auth", tags=["Auth"])



class RefreshTokenRequest(BaseModel):
    refresh_token: str


@router.post("/login")
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    db_user = authenticate_user(db, form_data.username, form_data.password)

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    role_name = db_user.role.role_name


    access_token = create_access_token(
        data={
            "sub": str(db_user.id),
            "username": db_user.name,
            "role": role_name
        }
    )

    refresh_token = create_refresh_token(
        data={
            "sub": str(db_user.id),
            "username": db_user.name,
            "role": role_name
        }
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "user": {
            "id": db_user.id,
            "name": db_user.name,
            "email": db_user.email,
            "role": role_name   
        }
    }




@router.post("/refresh")
def refresh_token_api(request: RefreshTokenRequest):
    try:
        payload = jwt.decode(
            request.refresh_token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Invalid token type")

        user_id = payload.get("sub")
        username = payload.get("username")

        new_access_token = create_access_token(
            data={"sub": user_id, "username": username }
        )

        return {
            "access_token": new_access_token,
            "token_type": "bearer"
        }

    except JWTError as e:
        print(" Refresh Token Error:", str(e)) 
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired refresh token"
        )