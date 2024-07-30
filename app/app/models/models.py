from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Float, Integer, String, DateTime

from app.database import ModelBase
from .crud import Crud

metadata = ModelBase.metadata


class Category(ModelBase, Crud):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    products = relationship("Product", back_populates="category")


class Product(ModelBase, Crud):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(Float)
    category_id = Column(ForeignKey("category.id"))
    category = relationship("Category", back_populates="products")
    sales = relationship("Sale", back_populates="product")

class Sale(ModelBase, Crud):
    __tablename__ = "sale"

    id = Column(Integer, primary_key=True)
    quantity = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.now(), nullable=False)
    product_id = Column(ForeignKey("product.id"))
    product = relationship("Product", back_populates="sales")