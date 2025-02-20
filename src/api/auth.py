from fastapi import APIRouter, Body, status, HTTPException, Depends
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from sqlalchemy.orm import Session

from src.schemas.requests import Login
from src.schemas.responses import ValidationErrorResponse, SuccessResponse
from src.utils.token import JWTManager
from src.utils.logger import Logger
from src.database.connection import get_database_connection
from src.database.repository.customers import CustomerRepository

router = APIRouter(prefix='/auth', tags=['Authentication'])

@router.post('/login')
def login(
    credentials: dict = Body(
        ...,
        title='Customers Credentiales for login',
        json_schema_extra=Login.schema()
        ),
    db: Session = Depends(get_database_connection)):
    """
    Authenticate a user with provided credentials.
    This endpoint accepts a dictionary of user credentials, validates them,
    and returns a JWT token if the credentials are valid.
    
    Args:
        credentials (dict): A dictionary containing user credentials.
    Returns:
        JSONResponse: A JSON response containing either a JWT token on success, or an error message on failure.
    Raises:
        ValidationError: If the provided credentials are invalid.
        Exception: If there is an error generating the JWT token.
    """
    
    logger = Logger()
    logger.log('INFO', f"[/api/v1/auth/login] [POST] Authenticating user with credentials {credentials}")

    try:
        credentials = Login(**credentials)
    except ValidationError as e:
        logger.log('ERROR', f"[/api/v1/auth/login] [POST] [400] Error validating request body")
        errors_details = e.errors()

        response = ValidationErrorResponse(details=errors_details)

        return JSONResponse(content=response.model_dump(), status_code=status.HTTP_400_BAD_REQUEST)

    customer_repository = CustomerRepository(db)
    customer = customer_repository.get_by_email(credentials.email)

    if not customer:
        logger.log('ERROR', f"[/api/v1/auth/login] [POST] [401] User not found")
        return JSONResponse(content={}, status_code=status.HTTP_404_NOT_FOUND)
    else:
        if not customer.password == credentials.password:
            logger.log('ERROR', f"[/api/v1/auth/login] [POST] [401] Invalid password")
            return JSONResponse(content={}, status_code=status.HTTP_401_UNAUTHORIZED)
        else:
            try:
                token_manager = JWTManager()
                token = token_manager.encode(credentials.model_dump())
            except Exception as e:
                logger.log('ERROR', f"[/api/v1/auth/login] [POST] [500] Error generating token: {str(e)}")
                return JSONResponse(content={'error': 'Internal Server Error'}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

            http_response = SuccessResponse(data={'token': token})

            logger.log('INFO', f"[/api/v1/auth/login] [POST] [200] User authenticated successfully")
            
            return JSONResponse(content=http_response.model_dump(), status_code=status.HTTP_200_OK) 
