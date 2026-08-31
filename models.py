from sqlalchemy import ForeignKey
from sqlalchemy import String,Integer,Float,DateTime
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from datetime import datetime

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id : Mapped[int] = mapped_column(Integer, primary_key=True)
    full_name : Mapped[str] = mapped_column(String(100))
    email : Mapped[str] = mapped_column(String(100))
    password : Mapped[str] = mapped_column(String(200))
    phone_number: Mapped[str] = mapped_column(String(20))

class Product(Base):
    __tablename__ = "products"

    id : Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id : Mapped[int] = mapped_column(ForeignKey("users.id"))
    product_name : Mapped[str] = mapped_column(String(100))
    buying_price : Mapped[float] = mapped_column(Float)
    selling_price : Mapped[float] = mapped_column(Float)

class Sale(Base):
    __tablename__ = "sales"
    
    id : Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id : Mapped[int] = mapped_column(ForeignKey("users.id"))
    sale_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

class Sales_detail(Base):
    __tablename__ = "sales_details"

    id : Mapped[int] = mapped_column(Integer, primary_key=True)
    product_id : Mapped[int] = mapped_column(ForeignKey("products.id"))
    sales_id : Mapped[int] = mapped_column(ForeignKey("sales.id"))
    quantity : Mapped[int] = mapped_column(Integer)

class Purchase(Base):
    __tablename__ = "purchases"

    id : Mapped[int] = mapped_column(Integer, primary_key=True)
    product_id : Mapped[int] = mapped_column(ForeignKey("products.id"))
    quantity : Mapped[int] = mapped_column(Integer)
    buying_price : Mapped[float] = mapped_column(Float)
    purchase_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)


class Payment(Base):
    __tablename__ = "payments"

    id : Mapped[int] = mapped_column(Integer, primary_key=True)
    sales_id : Mapped[int] = mapped_column(ForeignKey("sales.id"))
    amount: Mapped[float] = mapped_column(Float)
    payment_method: Mapped[str] = mapped_column(String(30))
    payment_status: Mapped[str] = mapped_column(String(30))
    payment_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

