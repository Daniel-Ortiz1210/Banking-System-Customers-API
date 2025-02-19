from pydantic import BaseModel, Field, field_validator

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
    email: str = Field(..., example='user@example.com', description='Email address of a customer')
    password: str = Field(..., description='Customer password')

    @field_validator('email', mode='after')
    def validate_email(cls, value):
        if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", value):
            raise ValueError('Invalid email format, it should be like: test@example.com')
        return value
