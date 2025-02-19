import jwt
from abc import ABC, abstractmethod
from datetime import datetime, timezone, timedelta

class TokenBaseManager(ABC):
    """
    TokenBaseManager is an abstract base class that serves as an interface for token generation and decoding.

    Methods
    -------
    encode(body: dict) -> str
        Abstract method to encode a dictionary into a token string.
    decode(token: str) -> dict
        Abstract method to decode a token string back into a dictionary.
    """
    """Interface for token generation"""

    @abstractmethod
    def encode(self, body: dict) -> str:
        pass

    @abstractmethod
    def decode(self, token: str) -> dict:
        pass

