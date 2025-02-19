from pydantic import BaseModel, Field, validator, AfterValidator, field_validator
from typing import List, Optional, Annotated
from datetime import datetime
import re

def validate_only_letters(value: str):
    """
    Validate that the input string contains only letters.

    Args:
        value (str): The string to be validated.

    Returns:
        str: The validated string if it contains only letters.

    Raises:
        ValueError: If the string contains non-letter characters.
    """
    if not value.isalpha():
        raise ValueError('Only letters are allowed')
    return value

AlphaStr = Annotated[str, AfterValidator(validate_only_letters)]

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
    first_name: AlphaStr = Field(..., example="John")
    last_name: AlphaStr = Field(..., example="Doe") 
    email: str = Field(..., example="email@example.com")
    phone: str = Field(..., example="+1234567890")
    created_at: Optional[str] = Field(example="2021-01-01T00:00:00", default=datetime.now().isoformat())
    updated_at: Optional[str] = Field(example="2021-01-01T00:00:00", default=datetime.now().isoformat())

    @field_validator('email', mode='after')
    def validate_email(cls, value):
        """
        Validates the email field after it has been set.

        This method uses a regular expression to check if the provided email
        address matches the standard email format. If the email does not match
        the expected format, a ValueError is raised.

        Args:
            cls: The class the method is attached to.
            value (str): The email address to validate.

        Returns:
            str: The validated email address.

        Raises:
            ValueError: If the email address does not match the expected format.
        """
        if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", value):
            raise ValueError('Invalid email format, it should be like: test@example.com')
        return value

    @field_validator('phone', mode='after')
    def validate_phone_number(cls, value):
        """
        Validates a phone number to ensure it meets specific criteria.

        Args:
            value (str): The phone number to validate.

        Returns:
            str: The validated phone number.

        Raises:
            ValueError: If the phone number is not between 10 and 15 digits long,
                        or if it does not start with a '+' character.
        """
        if len(value) < 10 or len(value) > 15:
            raise ValueError('Phone number should be 10-15 digits long')
        elif not str(value).startswith('+'):
            raise ValueError('Phone number should start with +')
        return value

