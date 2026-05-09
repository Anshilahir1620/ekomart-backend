from sqlalchemy import (
    Column,
    Integer,
    String,
    SmallInteger,
    TIMESTAMP,
    ForeignKey,
    UniqueConstraint,
    text,
)
from app.database import Base


class SubCategory(Base):
    __tablename__ = "subcategories"

    id = Column(Integer, primary_key=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)

    name = Column(String(100), nullable=False)
    slug = Column(String(120), nullable=True)

    status = Column(SmallInteger, server_default=text("1"))
    created_at = Column(
        TIMESTAMP,
        server_default=text("CURRENT_TIMESTAMP")
    )

    __table_args__ = (
        UniqueConstraint(
            "category_id",
            "name",
            name="uniq_subcat_per_cat"
        ),
    )
