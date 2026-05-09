from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class CategoryCreate(BaseModel):
    name: str
    slug: Optional[str] = None
    status: Optional[int] = 1
    image: Optional[str] = None   # ✅ optional


class CategoryOut(BaseModel):
    id: int
    name: str
    slug: Optional[str]
    status: int
    created_at: datetime
    image: Optional[str]          # ✅ optional

    class Config:
        from_attributes = True


class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    slug: Optional[str] = None
    status: Optional[int] = None
    image: Optional[str] = None   # ✅ FIXED