from sqlalchemy import Column, Integer, String, SmallInteger, TIMESTAMP, text,Text
from app.database import Base



class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    slug = Column(String(120), nullable=True)
    status = Column(SmallInteger, server_default=text("1"))
    image = Column(Text, nullable=True)
    created_at = Column(
        TIMESTAMP,
        server_default=text("CURRENT_TIMESTAMP")
    )
