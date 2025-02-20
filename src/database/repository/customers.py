from sqlalchemy.orm import Session

from src.database.models import CustomerModel

class CustomerRepository:
    """
    Repository class for managing CustomerModel entities in the database.
    Methods:
    --------
    __init__(db: Session):
        Initializes the repository with a database session.
    create(data: dict) -> CustomerModel:
        Creates a new customer record in the database.
    get_by_id(id: int) -> CustomerModel:
        Retrieves a customer record by its ID.
    get_by_email(email: str) -> CustomerModel:
        Retrieves a customer record by its email.
    get_all(skip: int, limit: int) -> list[CustomerModel]:
        Retrieves a list of customer records with pagination.
    update(id: int, data: dict) -> CustomerModel:
        Updates an existing customer record by its ID.
    delete(id: int) -> bool:
        Deletes a customer record by its ID.
    """
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, data: dict) -> CustomerModel:
        customer = CustomerModel(**data)
        self.db.add(customer)
        self.db.commit()
        self.db.refresh(customer)
        return customer
    
    def get_by_id(self, id: int) -> CustomerModel:
        return self.db.query(CustomerModel).filter(CustomerModel.id == id).first()

    def get_by_email(self, email: str) -> CustomerModel:
        return self.db.query(CustomerModel).filter(CustomerModel.email == email).first()
    
    def get_all(self, skip, limit) -> list[CustomerModel]:
        return self.db.query(CustomerModel).offset(skip).limit(limit).all()

    def update(self, id: int, data: dict) -> CustomerModel:
        customer = self.get_by_id(id)
        if customer:
            for key, value in data.items():
                setattr(customer, key, value)
            self.db.commit()
            self.db.refresh(customer)
            return customer
        return None
    
    def delete(self, id: int) -> bool:
        customer = self.get_by_id(id)
        if customer:
            self.db.delete(customer)
            self.db.commit()
            return True
        return False
