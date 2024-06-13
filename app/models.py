from sqlalchemy import Column, Integer, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from .database import Base

class Configuration(Base):
    __tablename__ = "configurations"

    id = Column(Integer, primary_key=True, index=True)
    country_code = Column(String, nullable=False)
    business_name = Column(String, nullable=False)  # New column for business name
    data = Column(JSONB, nullable=False)  # Store dynamic data in a JSONB column

    __table_args__ = (UniqueConstraint('country_code', 'business_name', name='uix_country_business'),)
