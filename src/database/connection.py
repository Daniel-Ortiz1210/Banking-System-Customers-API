import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from src.utils.config import Config

settings = Config()

database_url = f'mysql+pymysql://{settings.database_user}:{settings.database_password}@{settings.database_host}:{settings.database_port}/{settings.database_name}'
engine = create_engine(database_url, pool_recycle=120)

class DatabaseConnection:
    """
    DatabaseConnection class to manage the creation of database sessions.

    Attributes:
        _session_maker (sessionmaker): A SQLAlchemy sessionmaker instance for creating database sessions.

    Methods:
        __new__(cls):
            Creates a new sessionmaker instance if it doesn't exist and returns a new session.
    """
    _session_maker: Session = None

    def __new__(cls):
                
        if cls._session_maker is None:
            cls._session_maker = sessionmaker(engine, autoflush=False)
        return cls._session_maker()

def get_database_connection() -> Session:
    db = DatabaseConnection()
    try:
        yield db
    finally:
        db.close()
    