# app/api/order.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.Order_Schema import OrderCreate, OrderOut
from app.Crud.Order_Crud import create_order, get_all_orders, get_orders_by_user, get_order_by_id
from fastapi import BackgroundTasks

from app.dependencies.auth import get_current_user
from app.models.users import User  
from app.services.order_services import create_order_service
router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("/", response_model=OrderOut)
def create_order_api(
    order: OrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    background_tasks: BackgroundTasks = None
):
    return create_order_service(db, order, current_user.id , background_tasks)


@router.get("/my", response_model=list[OrderOut])
def get_my_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_orders_by_user(db, current_user.id)


@router.get("/{order_id}", response_model=OrderOut)
def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    order = get_order_by_id(db, order_id)

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    if order.user_id != current_user.id and getattr(current_user, "role", None) != "admin":
        raise HTTPException(status_code=403, detail="Not allowed")

    return order


@router.get("/", response_model=list[OrderOut])
def get_all_orders_api(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if getattr(current_user, "role", None) != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")

    return get_all_orders(db)