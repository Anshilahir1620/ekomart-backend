from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.role_schema import RoleCreate, RoleUpdate, RoleOut
from app.Crud.Roles_Crud import (
    create_role,
    get_roles,
    get_role_by_id,
    update_role,
    delete_role,
)

router = APIRouter(prefix="/roles", tags=["Roles"])


@router.post("/", response_model=RoleOut)
def add_role(role: RoleCreate, db: Session = Depends(get_db)):
    new_role = create_role(db, role)
    if not new_role:
        raise HTTPException(status_code=400,detail="Role already exists")
    return new_role



@router.get("/", response_model=list[RoleOut])
def list_roles(db: Session = Depends(get_db)):
    return get_roles(db)


@router.put("/{role_id}", response_model=RoleOut)
def edit_role(role_id: int, role: RoleUpdate, db: Session = Depends(get_db)):
    db_role = get_role_by_id(db, role_id)
    if not db_role:
        raise HTTPException(status_code=404, detail="Role not found")

    return update_role(db, db_role, role)


@router.delete("/{role_id}")
def remove_role(role_id: int, db: Session = Depends(get_db)):
    db_role = get_role_by_id(db, role_id)
    if not db_role:
        raise HTTPException(status_code=404, detail="Role not found")

    delete_role(db, db_role)
    return {"message": "Role deleted successfully"}
