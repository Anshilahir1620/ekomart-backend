from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Numeric, DateTime
from app.database import Base

class DailyOffer(Base):
    __tablename__ = "daily_offers"

    id = Column(Integer, primary_key=True, index=True)

    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    

    discount_type = Column(String(20), nullable=False)  # percentage / flat
    discount_value = Column(Numeric, nullable=False)

    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)

    is_active = Column(Boolean, default=True)