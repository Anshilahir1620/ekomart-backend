from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class SubCategoryCreate(BaseModel):
    name:str
    category_id:int
    slug:Optional[str] = None

class SubCategoryOut(BaseModel):
    id:int
    category_id:int
    name:str
    slug:str|None
    status:int
    created_at:datetime

    class Config:
        from_attributes= True

class SubCategoryUpdate(BaseModel):
    name:Optional[str] = None
    slug:Optional[str] = None
    status:Optional[int] = None
    category_id:Optional[int] = None
    
