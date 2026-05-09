from sqlalchemy.orm import Session ,joinedload
from app.models.users import User
from app.schemas.user_schema import UserCreate, UserUpdate , AdminCreate
from app.core.security import hash_password, verify_password
from fastapi import HTTPException
from app.models.roles import Role




def get_all_users(db: Session):
    return db.query(User).all()


def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def create_admin_user(db: Session, user_data: AdminCreate):
    
    existing = db.query(User).filter(User.email == user_data.email).first()
    if existing:
        raise HTTPException(400, "Email already exists")

    role = db.query(Role).filter(Role.role_name == user_data.role.value).first()
    if not role:
        raise HTTPException(400, "Invalid role")

    new_user = User(
        name=user_data.name,
        email=user_data.email,
        password=hash_password(user_data.password),
        role_id=role.id
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user    

def create_user(db: Session, user: UserCreate):
    existing = db.query(User).filter(User.email == user.email).first()
    if existing:
        raise HTTPException(400, "Email already exists")

    hashed_password = hash_password(user.password)

    db_user = User(
        name=user.name,
        email=user.email,
        password=hashed_password,
        role_id=3,
        status=1,
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def authenticate_user(db: Session, name: str, password: str):
    user = (db.query(User).options(joinedload(User.role))  .filter(User.name == name).first())
    if not user:
        return None

    if not verify_password(password, user.password):
        return None

    return user


def update_user(db: Session, user_id: int, user: UserUpdate):
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        return None

    update_data = user.model_dump(exclude_unset=True)

    for key, value in update_data.items():

        if value is None or (isinstance(value, str) and not value.strip()):
            continue  

        if key == "password":
            value = hash_password(value)
        
        if key == "email":
            existing = db.query(User).filter(User.email == value).first()
            if existing and existing.id != user_id:
                raise HTTPException(400, "Email already exists")

        setattr(db_user, key, value)

    db.commit()
    db.refresh(db_user)

    return db_user


def delete_user(db: Session, user: User):
    try:
        db.delete(user)
        db.commit()
    except:
        db.rollback()
        raise HTTPException(500, "Delete failed")
