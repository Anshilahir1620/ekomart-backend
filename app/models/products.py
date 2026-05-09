from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DECIMAL,
    TIMESTAMP,
    ForeignKey,
    text,
)
from app.database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    product_name = Column(String(255), nullable=False)
    regular_price = Column(DECIMAL(10, 2), nullable=True)  
    sale_price = Column(DECIMAL(10, 2), nullable=True)
    size = Column(String(50), nullable=True)
    weight = Column(DECIMAL(10, 2), nullable=True)
    rating = Column(DECIMAL(3, 2), nullable=True)

    life = Column(Integer, nullable=True)
    type = Column(String(100), nullable=True)
    brand = Column(String(100), nullable=True)

    nutrition_energy_kcal = Column(DECIMAL(10, 2), nullable=True)
    nutrition_protein_g = Column(DECIMAL(10, 2), nullable=True)
    nutrition_magnetiam_kcal = Column(DECIMAL(10, 2), nullable=True)
    nutrition_calory_kcal = Column(DECIMAL(10, 2), nullable=True)
    nutrition_vitamine_kcal = Column(DECIMAL(10, 2), nullable=True)

    stock = Column(Integer, server_default=text("0"))
    sku = Column(String(100), nullable=True)

    category = Column(String(100), nullable=True)

    subcategory_id = Column(
        Integer,
        ForeignKey("subcategories.id"),
        nullable=True,
        index=True
    )

    tag = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    image = Column(Text, nullable=True)

    created_at = Column(
        TIMESTAMP,
        server_default=text("CURRENT_TIMESTAMP")
    )

    updated_at = Column(
        TIMESTAMP,
        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP")
    )
