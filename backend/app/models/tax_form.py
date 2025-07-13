from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..core.database import Base

class TaxForm(Base):
    __tablename__ = "tax_forms"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    form_type = Column(String, nullable=False)  # "1040", "1040EZ", etc.
    tax_year = Column(Integer, nullable=False)
    status = Column(String, default="draft")  # draft, submitted, accepted, rejected
    form_data = Column(JSON)
    calculated_tax = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="tax_forms")
