# app/models/shop.py
from sqlalchemy import Column, Integer, String
from app.database import Base

class Shop(Base):
    __tablename__ = "shops"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    category = Column(String, nullable=False)
    location = Column(String, nullable=True)  # later: GPS coordinates
