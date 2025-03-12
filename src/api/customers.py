from fastapi import APIRouter, Body, Depends, Header, Path, status, Query
from fastapi.responses import JSONResponse, Response
from pydantic import ValidationError
from pymongo import MongoClient
from pymongo.errors import PyMongoError

from src.schemas.customers import CustomerBase
from src.schemas.requests import CustomerRequestBody
from src.schemas.responses import SuccessResponse, ValidationErrorResponse, BadResponse
from src.utils.dependencies import JWTBearerDependencie
from src.utils.logger import Logger
from src.utils.token import JWTManager
from src.database.connection import get_database_client
from src.database.repository.users import UsersRepository


router = APIRouter(
    prefix='/users',
    tags=['users']
)


@router.get('/')
def get_all_users(
    db_client: MongoClient = Depends(get_database_client),
    decoded_token: str = Depends(JWTBearerDependencie())
    ):
    """
    Retrieve all users from the database.\n
    This endpoint retrieves all users from the database.\n

    **URL:** /api/v1/users/\n
    **Method:** GET\n
    **Auth required:** NO\n
    **Permissions required:** None\n

    **Args** \n
        - db (MongoClient): Database session dependency, provided by FastAPI's Depends. \n
    **Responses** \n
        - 200: List of all users). \n
    **Logs Levels** \n
        - INFO: Logs the start of the user retrieval process. \n
        - INFO: Logs the successful completion of the user retrieval process. \n
    """
    logger = Logger()
    
    logger.log('INFO', f"[/api/v1/users/] [GET] Retreiving users from database")

    users_repository = UsersRepository(db_client)

    user = users_repository.get_by_email(decoded_token['email'])

    if not user:
        
        logger.log('ERROR', f"[/api/v1/users/] [GET] [404] User not found")
        
        response = BadResponse(message='User not found')
        
        return JSONResponse(content=response.model_dump(), status_code=status.HTTP_404_NOT_FOUND)

    users = users_repository.get_all()

    logger.log('INFO', f"[/api/v1/users/] [GET] [200] Users retreived successfully")

    return JSONResponse(content=users, status_code=status.HTTP_200_OK)


@router.get('/{email}')
def get_user_detail_by_email(
    db_client: MongoClient = Depends(get_database_client),
    decoded_token: str = Depends(JWTBearerDependencie()),
    email: str = Path(..., title="String value ID of the user to retrieve", description="The ID of the user to retrieve"),
    ):
    """
    Retrieve user details by email.\n
    This endpoint retrieves the details of a user from the database using the provided email.\n
    
    **URL:** /api/v1/users/{email}\n
    **Method:** GET\n
    **Auth required:** YES\n
    **Permissions required:** None\n

    **Args:**\n
        - db_client (MongoClient): Database session dependency.\n
        - decoded_token (str): Decoded JWT token dependency.\n
        - email (str): The email of the user to retrieve.\n
    **Responses:** \n
        - 200: user details retrieved successfully.\n
        - 403: Forbidden access to user with the provided email.\n
        - 404: user with the provided email not found.\n
    **Log Levels:**\n
        - INFO:\n
            - Retrieving user with email from database.\n
            - user with email retrieved successfully.\n
        - ERROR:\n
            - user not found.\n
    """
    logger = Logger()
    
    logger.log('INFO',f"[/api/v1/users/] [GET] Retreiving user from database")

    users_repository = UsersRepository(db_client)
    
    user = users_repository.get_by_email(decoded_token['email'])

    if not user:
        
        logger.log('ERROR', f"[/api/v1/users/{id}] [GET] [404] user not found")
        
        response = BadResponse(message='User not found')
        
        return JSONResponse(content=response.model_dump(), status_code=status.HTTP_404_NOT_FOUND)
    else:

        if email != decoded_token['email']:
            
            logger.log('ERROR', f"[/api/v1/users/{id}] [GET] [403] Forbidden access to user")
            
            response = BadResponse(message='Forbidden access to user')
            
            return JSONResponse(content=response.model_dump(), status_code=status.HTTP_403_FORBIDDEN)
        else:

            http_response = SuccessResponse(data=user).model_dump()

            logger.log('INFO', f"[/api/v1/users/] [GET] [200] User retreived successfully")
        
            return JSONResponse(content=http_response, status_code=status.HTTP_200_OK)


@router.post('/')
def create_user(
    db_client: MongoClient = Depends(get_database_client),
    request: dict = Body(..., json_schema_extra=CustomerRequestBody.model_json_schema())
    ):
    """
    Create a new user in the database. \n
    This function handles the creation of a new user by validating the request body \n
    persisting the user data to the database, and generating a JWT token for the user. \n
    **Args:** \n
        - db (Session): Database session dependency. \n
        - request (dict): Request body containing user data.\n
    **Responses:** \n
        - 201: user created successfully. \n
        - 400: Bad request if the request body validation fails. \n
        - 500: Internal server error if there is an error generating the JWT token. \n
    **Logs:** \n
        - INFO: Logs the start of the user creation process. \n
        - INFO: Logs the successful completion of the user creation process. \n
        - ERROR: Logs any errors encountered during the process. \n
    **Raises:** \n
        - ValidationError: If the request body validation fails. \n
        - IntegrityError: If there is a database integrity error (e.g., user already exists). \n
        - Exception: If there is an error generating the JWT token.
    """
    
    logger = Logger()
    
    logger.log('INFO', f"[/api/v1/users/] [POST] Persisting user to database")

    try: 
        body = CustomerRequestBody(**request)
    except ValidationError as e:
        logger.log('ERROR', f"[/api/v1/users/] [POST] [400] Error validating request body")

        errors_details = e.errors()
        
        error_response = ValidationErrorResponse(details=errors_details)
        
        return JSONResponse(content=error_response.model_dump(), status_code=status.HTTP_400_BAD_REQUEST)

    user_repository = UsersRepository(db_client)

    if user_repository.get_by_email(body.email):
        logger.log('ERROR', f"[/api/v1/users/] [POST] [400] User already exists")
        
        response = BadResponse(message='user already exists')
        
        return JSONResponse(content=response.model_dump(), status_code=status.HTTP_400_BAD_REQUEST)

    user_repository.create(body.model_dump())

    try:
        jwt_manager = JWTManager()
        
        token = jwt_manager.encode(body.model_dump())
    except Exception:
        
        logger.log('ERROR', f"[/api/v1/users/] [POST] [500] Error generating token")
        
        response = BadResponse(message='Possible error generating token')
        
        return JSONResponse(content=response.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    http_response = SuccessResponse(data={
        'user': body.model_dump(),
        'token': token
    })

    logger.log('INFO', "[/api/v1/users/] [POST] [201] user created successfully")
    
    return JSONResponse(content=http_response.model_dump(), status_code=status.HTTP_201_CREATED)


@router.put('/')
def update_user_by_id(
    db_client: MongoClient = Depends(get_database_client),
    decoded_token: dict = Depends(JWTBearerDependencie()),
    request: dict = Body(..., json_schema_extra=CustomerRequestBody.model_json_schema())
    ):
    """
    Update a user in the database.\n
    This endpoint replaces the user data with the provided request body for the user logged in.\n
    It also generates a new JWT token for the updated user.\n
    
    **URL:** /api/v1/users/\n
    **Method:** PUT\n
    **Auth required:** YES\n
    **Permissions required:** None\n

    **Args:**\n
        - db (Session): Database session dependency.\n
        - decoded_token (dict): Decoded JWT token dependency.\n
        - request (dict): Request body containing the user data to update.\n
    **Raises:**\n
        - ValidationError: If the request body validation fails.\n
        - Exception: If there is an error generating the JWT token.\n
    **Logs:**\n
        - INFO: Logs the start and successful completion of the update operation.\n
        - ERROR: Logs any errors encountered during the process.\n
    **Responses:**\n
        - 400: Bad request if the request body validation fails.\n
        - 404: Not found if the user with the specified ID does not exist.\n
        - 403: Forbidden if the logged-in user does not have access to the specified resource.\n
        - 500: Internal server error if there is an error generating the JWT token.\n
        - 201: Created if the user is updated successfully.\n
    """
    
    logger = Logger()
    
    logger.log('INFO', f"[/api/v1/users/] [PUT] Replacing user from database")

    try:  
        body = CustomerRequestBody(**request)
    except ValidationError as e:
        
        logger.log('ERROR', f"[/api/v1/users/] [PUT] [400] Error validating request body")

        errors_details = e.errors()
        
        error_response = ValidationErrorResponse(details=errors_details)
        
        return JSONResponse(content=error_response.model_dump(), status_code=status.HTTP_400_BAD_REQUEST)

    users_repository = UsersRepository(db_client)

    user = users_repository.get_by_email(decoded_token['email'])

    body_to_dict = body.model_dump()

    if not user:
        
        logger.log('ERROR', f"[/api/v1/users/] [PUT] [404] User not found")
        
        response = BadResponse(message='User not found')
        
        return JSONResponse(content=response.model_dump(), status_code=status.HTTP_404_NOT_FOUND)
    else:
        
        users_repository.update(decoded_token['email'], body_to_dict)

        logger.log('INFO', f"[/api/v1/users/] [PUT] [201] User updated successfully")

        try:
            jwt_manager = JWTManager()
            
            token = jwt_manager.encode(body.model_dump())
        except Exception as e:
            
            logger.log('ERROR', f"[/api/v1/users] [PUT] [500] Error generating token: {str(e)}")
            
            response = BadResponse(message='Possible error generating token')
            
            return JSONResponse(content=response.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        response = SuccessResponse(data={
            'token': token,
            'user': body_to_dict
            }
        )
        return JSONResponse(content=response.model_dump(), status_code=status.HTTP_201_CREATED)


@router.delete('/')
def delete_user_by_id(
    decoded_token: dict = Depends(JWTBearerDependencie()),
    db_client: MongoClient = Depends(get_database_client),
    ):
    """
    Deletes a user from the database.\n
    This endpoint deletes the user logged in.\n

    **URL:** /api/v1/users/\n
    **Method:** DELETE\n
    **Auth required:** YES\n
    **Permissions required:** None\n

    **Args:**\n
        - decoded_token (dict): The decoded JWT token containing user information.\n
        - db (Session): The database session dependency.\n
        - id (int): The unique identity value for a user.\n
    **Returns:**\n
        - 404 Not Found: If the user with the given ID does not exist.\n
        - 403 Forbidden: If the logged-in user does not have access to delete the specified user.\n
        - 204 No Content: If the user is successfully deleted.\n
    **Logs:**\n
        - INFO: When attempting to delete a user.\n
        - ERROR: If the user with the given ID does not exist.\n
        - ERROR: If the logged-in user does not have access to delete the specified user.\n
        - INFO: If the user is successfully deleted.\n
    """
    
    logger = Logger()
    
    logger.log('INFO', f"[/api/v1/users/] [DELETE] Deleting user from database")

    users_repository = UsersRepository(db_client)

    user = users_repository.get_by_email(decoded_token['email'])

    if not user:
        
        logger.log('ERROR', f"[/api/v1/user/{id}] [DELETE] [404] user with ID {id} not found")
        
        response = BadResponse(message='user not found')
        
        return JSONResponse(content=response.model_dump(), status_code=status.HTTP_404_NOT_FOUND)
    else:
    
        logger.log('INFO', f"[/api/v1/user/{id}] [DELETE] [204] User deleted successfully")

        users_repository.delete(decoded_token['email'])

        response = SuccessResponse()

        return Response(status_code=status.HTTP_204_NO_CONTENT)
