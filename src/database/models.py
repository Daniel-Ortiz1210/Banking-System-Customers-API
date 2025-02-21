from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

from src.database.connection import engine

from datetime import datetime, timezone

Base = declarative_base()

class CustomerModel(Base):
    """
    CustomerModel represents a customer entity in the database.

    Attributes:
        id (int): The primary key for the customer, auto-incremented.
        name (str): The name of the customer.
        email (str): The unique email address of the customer.
        phone (str): The phone number of the customer.
    """
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(255))
    last_name = Column(String(255))
    email = Column(String(255), unique=True)
    phone = Column(String(255))
    password = Column(String(255))
    created_at = Column(DateTime(), default=datetime.now(timezone.utc).isoformat())
    updated_at = Column(DateTime(), default=datetime.now(timezone.utc).isoformat())

Base.metadata.create_all(engine)
