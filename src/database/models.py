from sqlalchemy import Column, Integer, String

from src.database.connection import Base, get_database_connection

class CustomerModel(Base):
    """
    CustomerModel represents a customer entity in the database.

    Attributes:
        id (int): The primary key for the customer, auto-incremented.
        name (str): The name of the customer.
        email (str): The unique email address of the customer.
        phone (str): The phone number of the customer.

    Methods:
        __repr__(): Returns a string representation of the CustomerModel instance.
    """
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))
    email = Column(String(255), unique=True)
    phone = Column(String(255))

    def __repr__(self):
        return f'<Customer(id={self.id}, name={self.name}, email={self.email}, phone={self.phone})>'
