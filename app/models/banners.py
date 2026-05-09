from sqlalchemy import Column, Integer, String
from app.database import Base


class Banner(Base):
    __tablename__ = "banners"

    id = Column(Integer, primary_key=True, index=True)

    badge = Column(String(150), nullable=True)
    title1 = Column(String(100), nullable=False)
    highlight = Column(String(100), nullable=True)
    title2 = Column(String(100), nullable=True)

    desc1 = Column(String(255), nullable=True)
    desc2 = Column(String(255), nullable=True)

    image = Column(String(255), nullable=False)
    alt = Column(String(150), nullable=True)
