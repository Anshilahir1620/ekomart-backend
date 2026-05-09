from sqlalchemy import (Column,Integer,String,SmallInteger,TIMESTAMP,text,)
from app.database import Base


class Brand(Base):
    __tablename__ = "brands"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    logo = Column(String(255), nullable=True)

    status = Column(SmallInteger, server_default=text("1"))

    created_at = Column(
        TIMESTAMP,
        server_default=text("CURRENT_TIMESTAMP")
    )

    updated_at = Column(
        TIMESTAMP,
        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP")
    )
