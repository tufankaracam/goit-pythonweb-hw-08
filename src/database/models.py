from sqlalchemy import Column, Integer, String, Boolean, Table, ForeignKey, func, Date
from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from datetime import datetime


class Base(DeclarativeBase):
    pass


class Contact(Base):
    __tablename__ = "contacts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    firstname: Mapped[str] = mapped_column(String(50), nullable=False)
    lastname: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(50), nullable=False)
    phone: Mapped[str] = mapped_column(String(50), nullable=False)
    birthdate: Mapped[datetime] = mapped_column(Date, nullable=False)
    additional: Mapped[str] = mapped_column(String(255), nullable=True)
