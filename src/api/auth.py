from fastapi import APIRouter, Body, status, HTTPException, Depends
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from pymongo import MongoClient

from src.schemas.requests import Login
from src.schemas.responses import ValidationErrorResponse, SuccessResponse, BadResponse
from src.utils.token import JWTManager
from src.utils.logger import Logger
from src.database.connection import get_database_client
from src.database.repository.users import UsersRepository

router = APIRouter(prefix='/auth', tags=['Authentication'])

@router.post('/login')
def login(
    credentials: dict = Body(
        ...,
        title='Users Credentiales for login',
        json_schema_extra=Login.model_json_schema()
        ),
    db_client: MongoClient = Depends(get_database_client)):
    """
    Authenticates a user based on provided credentials.\n
    **URL:** /api/v1/auth/login\n
    **Method:** POST\n
    **Auth required:** NO\n
    **Permissions required:** None\n
    **Args:** \n
        credentials (dict): A dictionary containing the user's login credentials.\n
        db (MongoClient): Database session dependency.\n
    **Responses:**\n
        - 200 OK: If the user is authenticated successfully, returns a token.\n
        - 400 Bad Request: If there is a validation error in the request body.\n
        - 401 Unauthorized: If the user is not found or the password is invalid.\n
        - 404 Not Found: If the user is not found.\n
        - 500 Internal Server Error: If there is an error generating the token.\n
    Raises:\n
        - ValidationError: If there is a validation error in the request body.\n
    **Log Levels:**\n
        - INFO: When the user is authenticated successfully.\n
        - ERROR: When there is a validation error in the request body, the user is not found, the password is invalid, or there is an error generating the token.\n
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

    users_repository = UsersRepository(db_client)
    user = users_repository.get_by_email(credentials.email)

    if not user:
        logger.log('ERROR', f"[/api/v1/auth/login] [POST] [401] User not found")
        
        response = BadResponse(message='user not found')
        return JSONResponse(content=response.model_dump(), status_code=status.HTTP_404_NOT_FOUND)
    else:
        if not user['password'] == credentials.password:
            logger.log('ERROR', f"[/api/v1/auth/login] [POST] [401] Invalid password")
            
            response = BadResponse(message='Invalid password')
            return JSONResponse(content=response.model_dump(), status_code=status.HTTP_401_UNAUTHORIZED)
        else:
            try:
                token_manager = JWTManager()
                token = token_manager.encode(credentials.model_dump())
            except Exception as e:
                logger.log('ERROR', f"[/api/v1/auth/login] [POST] [500] Error generating token: {str(e)}")
                
                response = BadResponse(message='Possible error generating token')
                return JSONResponse(content=response.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

            http_response = SuccessResponse(data={'token': token})

            logger.log('INFO', f"[/api/v1/auth/login] [POST] [200] User authenticated successfully")
            
            return JSONResponse(content=http_response.model_dump(), status_code=status.HTTP_200_OK) 
