from pydantic import BaseModel, Field, validator, AfterValidator, field_validator, ConfigDict
from typing import List, Optional, Annotated
from datetime import datetime
import re
from src.schemas.types import AlphaStr, EmailStr, PhoneNumberStr

class CustomerBase(BaseModel):
    """
    CustomerBase schema for customer data validation.

    Attributes:
        first_name (AlphaStr): The first name of the customer. Example: "John".
        last_name (AlphaStr): The last name of the customer. Example: "Doe".
        email (str): The email address of the customer. Example: "email@example.com".
        phone (str): The phone number of the customer. Example: "+1234567890".
        created_at (Optional[str]): The timestamp when the customer was created. Example: "2021-01-01T00:00:00".
        updated_at (Optional[str]): The timestamp when the customer was last updated. Example: "2021-01-01T00:00:00".

    Methods:
        validate_email(cls, value): Validates the email format.
        validate_phone_number(cls, value): Validates the phone number format and length.
    """
    id: int = Field(..., example=1)
    first_name: AlphaStr = Field(..., example="John")
    last_name: AlphaStr = Field(..., example="Doe") 
    email: EmailStr = Field(..., example="email@example.com")
    password: str = Field(..., example="password")
    phone: PhoneNumberStr = Field(..., example="+1234567890")
    created_at: Optional[datetime] = Field(example="2021-01-01T00:00:00", default=datetime.now().isoformat())
    updated_at: Optional[datetime] = Field(example="2021-01-01T00:00:00", default=datetime.now().isoformat())

    model_config = ConfigDict(from_attributes=True)

