from pydantic import BaseModel
from typing import Optional


class RoleCreate(BaseModel):
    role_name: str

class RoleOut(BaseModel):
    id: int
    role_name: str

    class Config:
        from_attributes = True

class RoleUpdate(BaseModel):
    role_name: Optional[str] = None