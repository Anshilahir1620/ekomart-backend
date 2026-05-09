from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class BrandCreate(BaseModel):
    name: str
    logo: Optional[str] = None


class BrandOut(BaseModel):
    id: int
    name: str
    logo: Optional[str] = None
    status: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class BrandUpdate(BaseModel):
    name: Optional[str] = None
    logo: Optional[str] = None
    status: Optional[int] = None

    class Config:
        from_attributes = True
