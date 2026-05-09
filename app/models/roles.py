from sqlalchemy import Column, Integer, String, TIMESTAMP
from app.database import Base

class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True)
    role_name = Column(String(255))
