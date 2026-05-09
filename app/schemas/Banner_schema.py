from pydantic import BaseModel
from typing import Optional


class BannerCreate(BaseModel):
    badge: Optional[str] = None
    title1: str
    highlight: Optional[str] = None
    title2: Optional[str] = None
    desc1: Optional[str] = None
    desc2: Optional[str] = None
    image: str
    alt: Optional[str] = None



class BannerOut(BaseModel):
    id: int
    badge: Optional[str] = None
    title1: str
    highlight: Optional[str] = None
    title2: Optional[str] = None
    desc1: Optional[str] = None
    desc2: Optional[str] = None
    image: str
    alt: Optional[str] = None

    class Config:
        from_attributes = True


class BannerUpdate(BaseModel):
    badge: Optional[str] = None
    title1: Optional[str] = None
    highlight: Optional[str] = None
    title2: Optional[str] = None
    desc1: Optional[str] = None
    desc2: Optional[str] = None
    image: Optional[str] = None
    alt: Optional[str] = None

    class Config:
        from_attributes = True
