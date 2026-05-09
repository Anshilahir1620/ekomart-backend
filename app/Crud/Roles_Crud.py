from sqlalchemy.orm import Session
from app.models.roles import Role
from app.schemas.role_schema import RoleCreate, RoleUpdate


def create_role(db: Session, role: RoleCreate):
    existing_role = (
        db.query(Role).filter(Role.role_name == role.role_name).first())
    if existing_role:
        return None  
    db_role = Role(role_name=role.role_name)
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role


def get_roles(db: Session):
    return db.query(Role).all()


def get_role_by_id(db: Session, role_id: int):
    return db.query(Role).filter(Role.id == role_id).first()


def update_role(db: Session, db_role: Role, role: RoleUpdate):
    update_data = role.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_role, key, value)

    db.commit()
    db.refresh(db_role)
    return db_role


def delete_role(db: Session, db_role: Role):
    db.delete(db_role)
    db.commit()
