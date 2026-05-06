from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database import Base

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)  # "income" или "expense"

    transactions = relationship("Transaction", back_populates="category")

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    type = Column(String, nullable=False)  # "income" или "expense"
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    note = Column(String, nullable=True)
    date = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    category = relationship("Category", back_populates="transactions")