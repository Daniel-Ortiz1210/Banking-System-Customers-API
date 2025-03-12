from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse, Response
from pymongo import MongoClient

from src.database.connection import get_database_client
from src.utils.dependencies import JWTBearerDependencie
from src.utils.logger import Logger
from src.database.repository.users import UsersRepository
from src.services.studio_ghibli import ServicesFactory
from src.schemas.responses import SuccessResponse, BadResponse


router = APIRouter(prefix='/ghibli', tags=['Studio Ghibli'])


@router.get('/vehicles')
def request_vehicles_studio_ghibli_services(
    db_client: MongoClient = Depends(get_database_client),
    decoded_token: dict = Depends(JWTBearerDependencie())
):
    """
    Endpoint to request Studio Ghibli vehicle services.

    This endpoint fetches vehicle data from Studio Ghibli services based on the user's role.
    Only users with roles 'admin' or 'vehicles' are authorized to access this endpoint.

    Args:
        - db_client (MongoClient): The database client dependency.
        - decoded_token (dict): The decoded JWT token dependency.

    Returns:
        - JSONResponse: A JSON response containing the vehicle data if the user is authorized,
                    or an error message if the user is not found or forbidden.

    Raises:
        - HTTP_401_UNAUTHORIZED: If the user is not found.
        - HTTP_403_FORBIDDEN: If the user does not have the required role.
    """
    
    logger = Logger()
    logger.log('INFO', f"[/api/v1/ghibli/vehicles] [GET] Requesting Studio Ghibli services")


    users_repository = UsersRepository(db_client)
    user = users_repository.get_by_email(decoded_token['email'])

    if user is None:
        logger.log('ERROR', f"[/api/v1/ghibli/vehicles] [GET] [401] User not found")
        return JSONResponse(content={"detail": "User not found"}, status_code=status.HTTP_401_UNAUTHORIZED)
    
    user_role = user['role']

    if user_role in ('admin', 'vehicles'):
        logger.log('INFO', f"[/api/v1/ghibli/vehicles] [GET] Fetching vehicles")
        services = ServicesFactory.get_service('vehicles')
        response = services.fetch_all()
        response = SuccessResponse(data=response).model_dump()
        return JSONResponse(content=response)
    else:
        logger.log('ERROR', f"[/api/v1/ghibli/vehicles] [GET] [403] Forbidden")
        response = BadResponse(detail={"detail": "Forbidden"}).model_dump()
        return JSONResponse(content=response, status_code=status.HTTP_403_FORBIDDEN)


@router.get('/vehicles/{id}')
def request_vehicles_studio_ghibli_services_by_id(
    id: str,
    db_client: MongoClient = Depends(get_database_client),
    decoded_token: dict = Depends(JWTBearerDependencie())
):
    """
    Handles the request to fetch Studio Ghibli vehicle services by ID.
    Logs:
        - INFO: Request initiation with endpoint and method.
        - ERROR: User not found.
        - INFO: Fetching vehicles by ID.
        - ERROR: Forbidden access.
    Args:
        id (str): The ID of the vehicle to fetch.
        db_client (MongoClient, optional): The database client dependency.
        decoded_token (dict, optional): The decoded JWT token dependency.
    Returns:
        JSONResponse: The HTTP response with the appropriate status code and message.
    HTTP Responses:
        - 200 OK: Successfully fetched vehicle data.
        - 401 Unauthorized: User not found.
        - 403 Forbidden: User does not have the required role.
    """
    
    logger = Logger()
    logger.log('INFO', f"[/api/v1/ghibli/vehicles/{id}] [GET] Requesting Studio Ghibli services by id")


    users_repository = UsersRepository(db_client)
    user = users_repository.get_by_email(decoded_token['email'])

    if user is None:
        logger.log('ERROR', f"[/api/v1/ghibli/vehicles/{id}] [GET] [401] User not found")
        return JSONResponse(content={"detail": "User not found"}, status_code=status.HTTP_401_UNAUTHORIZED)
    
    user_role = user['role']

    if user_role in ('admin', 'vehicles'):
        logger.log('INFO', f"[/api/v1/ghibli/vehicles/{id}] [GET] Fetching vehicles by id")
        services = ServicesFactory.get_service('vehicles')
        data = services.fetch_by_id(id)
        response = SuccessResponse(data=data).model_dump()
        return JSONResponse(content=response, status_code=status.HTTP_200_OK)
    else:
        logger.log('ERROR', f"[/api/v1/ghibli/vehicles/{id}] [GET] [403] Forbidden")
        response = BadResponse(detail={"detail": "Forbidden"}).model_dump()
        return JSONResponse(content=response, status_code=status.HTTP_403_FORBIDDEN)
    

@router.get('/species')
def request_species_studio_ghibli_services(
    db_client: MongoClient = Depends(get_database_client),
    decoded_token: dict = Depends(JWTBearerDependencie())
):
    """
    Handles the request to fetch Studio Ghibli species data.
    Logs:
        - INFO: When the request is initiated.
        - ERROR: If the user is not found or if the user does not have the required role.
        - INFO: When fetching species data.
    Args:
        db_client (MongoClient): The database client dependency.
        decoded_token (dict): The decoded JWT token containing user information.
    Description:
        This function checks the user's role and fetches species data if the user has the appropriate permissions.
        It logs the process and returns the appropriate HTTP response based on the user's role and existence.
    HTTP Responses:
        - 200 OK: If the species data is successfully fetched.
        - 401 Unauthorized: If the user is not found.
        - 403 Forbidden: If the user does not have the required role.
    """
    
    logger = Logger()
    logger.log('INFO', f"[/api/v1/ghibli/species] [GET] Requesting Studio Ghibli services")


    users_repository = UsersRepository(db_client)
    user = users_repository.get_by_email(decoded_token['email'])

    if user is None:
        logger.log('ERROR', f"[/api/v1/ghibli/species] [GET] [401] User not found")
        return JSONResponse(content={"detail": "User not found"}, status_code=status.HTTP_401_UNAUTHORIZED)
    
    user_role = user['role']

    if user_role in ('admin', 'species'):
        logger.log('INFO', f"[/api/v1/ghibli/species] [GET] Fetching species")
        services = ServicesFactory.get_service('species')
        data = services.fetch_all()
        response = SuccessResponse(data=data).model_dump()
        return JSONResponse(content=response, status_code=status.HTTP_200_OK)
    else:
        logger.log('ERROR', f"[/api/v1/ghibli/species] [GET] [403] Forbidden")

        response = BadResponse(detail={"detail": "Forbidden"}).model_dump()
        return JSONResponse(content=response, status_code=status.HTTP_403_FORBIDDEN)


@router.get('/species/{id}')
def request_species_studio_ghibli_services_by_id(
    id: str,
    db_client: MongoClient = Depends(get_database_client),
    decoded_token: dict = Depends(JWTBearerDependencie())
):
    """
    Handles the request to fetch Studio Ghibli species by ID.
    Logs:
        - INFO: Request initiation and fetching species by ID.
        - ERROR: User not found or forbidden access.
    Args:
        id (str): The ID of the species to fetch.
        db_client (MongoClient, optional): The database client dependency. Defaults to Depends(get_database_client).
        decoded_token (dict, optional): The decoded JWT token dependency. Defaults to Depends(JWTBearerDependencie).
    Returns:
        JSONResponse: The HTTP response containing the species data or an error message.
    HTTP Responses:
        - 200 OK: Successfully fetched species data.
        - 401 Unauthorized: User not found.
        - 403 Forbidden: User does not have the required role.
    """
    
    logger = Logger()
    logger.log('INFO', f"[/api/v1/ghibli/species/{id}] [GET] Requesting Studio Ghibli services by id")


    users_repository = UsersRepository(db_client)
    user = users_repository.get_by_email(decoded_token['email'])

    if user is None:
        logger.log('ERROR', f"[/api/v1/species/{id}] [GET] [401] User not found")
        return JSONResponse(content={"detail": "User not found"}, status_code=status.HTTP_401_UNAUTHORIZED)
    
    user_role = user['role']

    if user_role in ('admin', 'species'):
        logger.log('INFO', f"[/api/v1/ghibli/species/{id}] [GET] Fetching species by id")
        services = ServicesFactory.get_service('species')
        data = services.fetch_by_id(id)
        response = SuccessResponse(data=data).model_dump()
        return JSONResponse(content=response, status_code=status.HTTP_200_OK)
    else:
        logger.log('ERROR', f"[/api/v1/ghibli/species/{id}] [GET] [403] Forbidden")
        response = BadResponse(detail={"detail": "Forbidden"}).model_dump()
        return JSONResponse(content=response, status_code=status.HTTP_403_FORBIDDEN)


@router.get('/locations')
def request_locations_studio_ghibli_services(
    db_client: MongoClient = Depends(get_database_client),
    decoded_token: dict = Depends(JWTBearerDependencie())
):
    """
    Handles the request to fetch Studio Ghibli locations.
    This function logs the request, verifies the user's role, and fetches the locations
    if the user has the appropriate permissions.
    Args:
        db_client (MongoClient): The database client dependency.
        decoded_token (dict): The decoded JWT token containing user information.
    Logs:
        INFO: When the request is initiated.
        ERROR: If the user is not found or does not have the required permissions.
        INFO: When fetching locations for authorized users.
    Returns:
        JSONResponse: A JSON response with the appropriate status code and message.
    HTTP Responses:
        200 OK: If the locations are successfully fetched.
        401 Unauthorized: If the user is not found.
        403 Forbidden: If the user does not have the required permissions.
    """
    logger = Logger()
    logger.log('INFO', f"[/api/v1/ghibli/locations] [GET] Requesting Studio Ghibli services")


    users_repository = UsersRepository(db_client)
    user = users_repository.get_by_email(decoded_token['email'])

    if user is None:
        logger.log('ERROR', f"[/api/v1/ghibli/locations] [GET] [401] User not found")
        return JSONResponse(content={"detail": "User not found"}, status_code=status.HTTP_401_UNAUTHORIZED)
    
    user_role = user['role']

    if user_role in ('admin', 'locations'):
        logger.log('INFO', f"[/api/v1/ghibli/locations] [GET] Fetching locations")
        services = ServicesFactory.get_service('locations')
        data = services.fetch_all()
        response = SuccessResponse(data=data).model_dump()
        return JSONResponse(content=response, status_code=status.HTTP_200_OK)
    else:
        logger.log('ERROR', f"[/api/v1/ghibli/locations] [GET] [403] Forbidden")
        response = BadResponse(detail={"detail": "Forbidden"}).model_dump()
        return JSONResponse(content=response, status_code=status.HTTP_403_FORBIDDEN)


@router.get('/locations/{id}')
def request_locations_studio_ghibli_services_by_id(
    id: str,
    db_client: MongoClient = Depends(get_database_client),
    decoded_token: dict = Depends(JWTBearerDependencie())
):
    """
    Handles GET requests for Studio Ghibli locations by ID.
    Logs:
        - INFO: Requesting Studio Ghibli services by id
        - ERROR: User not found
        - INFO: Fetching locations by id
        - ERROR: Forbidden
    Args:
        id (str): The ID of the location to fetch.
        db_client (MongoClient): The database client dependency.
        decoded_token (dict): The decoded JWT token dependency.
    Returns:
        JSONResponse: 
            - 200 OK: If the user is authorized and the location is fetched successfully.
            - 401 Unauthorized: If the user is not found.
            - 403 Forbidden: If the user does not have the required role.
    Description:
        This function handles GET requests to fetch Studio Ghibli location details by ID. It first logs the request, 
        then checks if the user exists and has the appropriate role. If the user is authorized, it fetches the location 
        details and returns them in a successful response. If the user is not found or does not have the required role, 
        it returns an appropriate error response.
    """
    
    logger = Logger()
    logger.log('INFO', f"[/api/v1/ghibli/locations/{id}] [GET] Requesting Studio Ghibli services by id")


    users_repository = UsersRepository(db_client)
    user = users_repository.get_by_email(decoded_token['email'])

    if user is None:
        logger.log('ERROR', f"[/api/v1/ghibli/locations/{id}] [GET] [401] User not found")
        return JSONResponse(content={"detail": "User not found"}, status_code=status.HTTP_401_UNAUTHORIZED)
    
    user_role = user['role']

    if user_role in ('admin', 'locations'):
        logger.log('INFO', f"[/api/v1/ghibli/locations/{id}] [GET] Fetching locations by id")
        services = ServicesFactory.get_service('locations')
        data = services.fetch_by_id(id)
        response = SuccessResponse(data=data).model_dump()
        return JSONResponse(content=response, status_code=status.HTTP_200_OK)
    else:
        logger.log('ERROR', f"[/api/v1/ghibli/locations/{id}] [GET] [403] Forbidden")
        response = BadResponse(detail={"detail": "Forbidden"}).model_dump()
        return JSONResponse(content=response, status_code=status.HTTP_403_FORBIDDEN)
    

@router.get('/people')
def request_people_studio_ghibli_services(
    db_client: MongoClient = Depends(get_database_client),
    decoded_token: dict = Depends(JWTBearerDependencie())
):
    """
    Handles the request to fetch people data from Studio Ghibli services.
    Logs:
        - INFO: When the request is initiated.
        - ERROR: If the user is not found or if the user does not have the required role.
        - INFO: When fetching people data.
    Args:
        db_client (MongoClient): The database client dependency.
        decoded_token (dict): The decoded JWT token dependency.
    Returns:
        JSONResponse: 
            - 200 OK: If the user is authorized and data is fetched successfully.
            - 401 Unauthorized: If the user is not found.
            - 403 Forbidden: If the user does not have the required role.
    """

    logger = Logger()
    logger.log('INFO', f"[/api/v1/ghibli/people] [GET] Requesting Studio Ghibli services")


    users_repository = UsersRepository(db_client)
    user = users_repository.get_by_email(decoded_token['email'])

    if user is None:
        logger.log('ERROR', f"[/api/v1/ghibli/people] [GET] [401] User not found")
        return JSONResponse(content={"detail": "User not found"}, status_code=status.HTTP_401_UNAUTHORIZED)
    
    user_role = user['role']

    if user_role in ('admin', 'people'):
        logger.log('INFO', f"[/api/v1/ghibli/people] [GET] Fetching people")
        services = ServicesFactory.get_service('people')
        data = services.fetch_all()

        response = SuccessResponse(data=data).model_dump()

        return JSONResponse(content=response, status_code=status.HTTP_200_OK)
    else:
        logger.log('ERROR', f"[/api/v1/ghibli/people] [GET] [403] Forbidden")

        response = BadResponse(detail={"detail": "Forbidden"}).model_dump()
        return JSONResponse(content=response, status_code=status.HTTP_403_FORBIDDEN)


@router.get('/people/{id}')
def request_people_studio_ghibli_services_by_id(
    id: str,
    db_client: MongoClient = Depends(get_database_client),
    decoded_token: dict = Depends(JWTBearerDependencie())
):
    """
    Handles the request to fetch Studio Ghibli people services by ID.
    This function performs the following steps:
    1. Logs the incoming request.
    2. Retrieves the user from the database using the email from the decoded JWT token.
    3. Checks if the user exists and logs an error if not.
    4. Checks the user's role and fetches the requested data if the user has the appropriate role.
    5. Returns the fetched data or an error response based on the user's role.
    Args:
        id (str): The ID of the Studio Ghibli person to fetch.
        db_client (MongoClient, optional): The database client dependency. Defaults to Depends(get_database_client).
        decoded_token (dict, optional): The decoded JWT token dependency. Defaults to Depends(JWTBearerDependencie()).
    Logs:
        - INFO: When a request is received.
        - ERROR: If the user is not found or if the user does not have the appropriate role.
        - INFO: When fetching the data by ID.
    HTTP Responses:
        - 200 OK: If the data is successfully fetched.
        - 401 Unauthorized: If the user is not found.
        - 403 Forbidden: If the user does not have the appropriate role.
    Returns:
        JSONResponse: The response containing the fetched data or an error message.
    """
    logger = Logger()
    logger.log('INFO', f"[/api/v1/ghibli/people/{id}] [GET] Requesting Studio Ghibli services by id")


    users_repository = UsersRepository(db_client)
    user = users_repository.get_by_email(decoded_token['email'])

    if user is None:
        logger.log('ERROR', f"[/api/v1/ghibli/people/{id}] [GET] [401] User not found")
        return JSONResponse(content={"detail": "User not found"}, status_code=status.HTTP_401_UNAUTHORIZED)
    
    user_role = user['role']

    if user_role in ('admin', 'people'):
        logger.log('INFO', f"[/api/v1/ghibli/people/{id}] [GET] Fetching people by id")
        services = ServicesFactory.get_service('people')
        data = services.fetch_by_id(id)
        response = SuccessResponse(data=data).model_dump()
        return JSONResponse(content=response, status_code=status.HTTP_200_OK)
    else:
        logger.log('ERROR', f"[/api/v1/ghibli/people/{id}] [GET] [403] Forbidden")
        response = BadResponse(detail={"detail": "Forbidden"}).model_dump()
        return JSONResponse(content=response, status_code=status.HTTP_403_FORBIDDEN)    

@router.get('/films')
def request_films_studio_ghibli_services(
    db_client: MongoClient = Depends(get_database_client),
    decoded_token: dict = Depends(JWTBearerDependencie())
):
    """
    Handles the request to fetch Studio Ghibli films.
    This function logs the request, verifies the user's role, and fetches the films
    if the user has the appropriate permissions.
    Args:
        db_client (MongoClient): The database client dependency.
        decoded_token (dict): The decoded JWT token containing user information.
    Logs:
        INFO: When the request is initiated.
        ERROR: If the user is not found or does not have the required permissions.
        INFO: When fetching films for authorized users.
    Returns:
        JSONResponse: A JSON response with the appropriate status code and message.
    HTTP Responses:
        200 OK: If the films are successfully fetched.
        401 Unauthorized: If the user is not found.
        403 Forbidden: If the user does not have the required role.
    """
    
    logger = Logger()
    logger.log('INFO', f"[/api/v1/ghibli/films] [GET] Requesting Studio Ghibli services")


    users_repository = UsersRepository(db_client)
    user = users_repository.get_by_email(decoded_token['email'])

    if user is None:
        logger.log('ERROR', f"[/api/v1/ghibli/films] [GET] [401] User not found")
        return JSONResponse(content={"detail": "User not found"}, status_code=status.HTTP_401_UNAUTHORIZED)
    
    user_role = user['role']

    if user_role in ('admin', 'films'):
        logger.log('INFO', f"[/api/v1/ghibli/films] [GET] Fetching films")
        services = ServicesFactory.get_service('films')
        data = services.fetch_all()
        response = SuccessResponse(data=data).model_dump()
        return JSONResponse(content=response, status_code=status.HTTP_200_OK)
    else:
        logger.log('ERROR', f"[/api/v1/ghibli/films] [GET] [403] Forbidden")
        response = BadResponse(detail={"detail": "Forbidden"}).model_dump()
        return JSONResponse(content=response, status_code=status.HTTP_403_FORBIDDEN)
