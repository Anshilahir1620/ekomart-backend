from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    SmallInteger,
    ForeignKey,
    text,
)
from app.database import Base
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)

    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)

    role_id = Column(
        Integer,
        ForeignKey("roles.id"),
        server_default=text("2")
    )

    mobile = Column(String(20), nullable=True)
    city = Column(String(100), nullable=True)
    state = Column(String(100), nullable=True)
    pincode = Column(String(10), nullable=True)

    address = Column(Text, nullable=True)
    profile_photo = Column(String(255), nullable=True)

    status = Column(SmallInteger, server_default=text("1"))
    name = Column(String(100), nullable=True)

    role = relationship("Role", backref="users")
