from pydantic import BaseModel, Field, field_validator
from src.schemas.types import EmailStr, AlphaStr, PhoneNumberStr, PasswordStr

import re

class Login(BaseModel):
    """
    Login schema for user authentication.

    Attributes:
        email (str): Email address of a customer. Example: 'user@example.com'.
        password (str): Customer password.

    Methods:
        validate_email(cls, value): Validates the format of the email address.
            Args:
                value (str): The email address to validate.
            Returns:
                str: The validated email address.
            Raises:
                ValueError: If the email address format is invalid.
    """
    email: EmailStr = Field(..., example='user@example.com', description='Email address of a customer')
    password: PasswordStr = Field(..., description='Customer password')


class CustomerRequestBody(BaseModel):
    first_name: AlphaStr = Field(..., example="John")
    last_name: AlphaStr = Field(..., example="Doe") 
    email: EmailStr = Field(..., example="email@example.com")
    password: PasswordStr = Field(..., example="password")
    phone: PhoneNumberStr = Field(..., example="+1234567890")
