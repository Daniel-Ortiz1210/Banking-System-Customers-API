from fastapi import APIRouter, Body, Depends, Header, Path, status, Query
from fastapi.responses import JSONResponse, Response
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from pydantic import ValidationError
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from src.schemas.customers import CustomerBase
from src.schemas.requests import CustomerRequestBody
from src.schemas.responses import SuccessResponse, ValidationErrorResponse, BadResponse
from src.utils.dependencies import JWTBearerDependencie
from src.utils.logger import Logger
from src.utils.token import JWTManager
from src.database.connection import get_database_connection
from src.database.repository.customers import CustomerRepository
from src.database.models import CustomerModel


router = APIRouter(
    prefix='/customers',
    tags=['Customers']
)


@router.get('/')
def get_all_customers(db: Session = Depends(get_database_connection)) -> Page[CustomerBase]:
    """
    Retrieve all customers from the database. \n
    This endpoint retrieves all customers from the database and paginates the results 
    using the FastAPI pagination extension. \n

    **Arguments** \n
        - db (Session): Database session dependency, provided by FastAPI's Depends. \n
    **Responses** \n
        - 200: A paginated list of customers (Page[CustomerBase]). \n
    **Logs Levels** \n
        - INFO: Logs the start of the customer retrieval process. \n
        - INFO: Logs the successful completion of the customer retrieval process. \n
    """
    logger = Logger()
    
    logger.log('INFO', f"[/api/v1/customers/] [GET] Retreiving customers from database")

    customer_repository = CustomerRepository(db)

    result = paginate(db, customer_repository.get_all())

    logger.log('INFO', f"[/api/v1/customers/] [GET] [200] Customers retreived successfully")

    return result


@router.get('/{id}')
def get_customer_details(
    db: Session = Depends(get_database_connection),
    decoded_token: str = Depends(JWTBearerDependencie()),
    id: int = Path(
        ...,
        title='Customer ID',
        description='Unique identity value for a Customer'
        )
    ):
    """
    Retrieve customer details by ID.\n
    This endpoint retrieves the details of a customer from the database using the provided customer ID.\n
    It also verifies that the customer making the request has access to the requested customer ID.\n
    \n
    
    **Responses:** \n
        - 200: Customer details retrieved successfully.\n
        - 403: Forbidden access to customer with the provided ID.\n
        - 404: Customer with the provided ID not found.\n
    **Log Levels:**\n
        - INFO:\n
            - Retrieving customer with ID from database.\n
            - Customer with ID retrieved successfully.\n
        - ERROR:\n
            - Customer with ID not found.\n
            - Forbidden access to customer with ID.\n
    """
    logger = Logger()
    
    logger.log('INFO',f"[/api/v1/customers/{id}] [GET] Retreiving customer with ID {id} from database")

    customer_repository = CustomerRepository(db)
    
    customer = customer_repository.get_by_email(decoded_token['email'])

    if not customer:
        
        logger.log('ERROR', f"[/api/v1/customers/{id}] [GET] [404] Customer with ID {id} not found")
        
        response = BadResponse(message='Customer not found')
        
        return JSONResponse(content=response.model_dump(), status_code=status.HTTP_404_NOT_FOUND)
    else:
        if customer.id != id:
            
            logger.log('ERROR', f"[/api/v1/customers/{id}] [GET] [403] Forbidden access to customer with ID {id}")

            response = BadResponse(message='Customer logged in does not have access to this resource')
            
            return JSONResponse(content=response.model_dump(), status_code=status.HTTP_403_FORBIDDEN)
        else:
            http_response = SuccessResponse(data=
                {
                    'id': customer.id,
                    'first_name': customer.first_name,
                    'last_name': customer.last_name,
                    'email': customer.email,
                    'phone': customer.phone,
                }
            ).model_dump()

            logger.log('INFO', f"[/api/v1/customers/{id}] [GET] [200] Customer with ID {id} retreived successfully")
    
            return JSONResponse(content=http_response, status_code=status.HTTP_200_OK)


@router.post('/')
def create_customer(db: Session = Depends(get_database_connection), request: dict = Body(...,json_schema_extra=CustomerBase.schema())):
    """
    Create a new customer in the database. \n
    This function handles the creation of a new customer by validating the request body \n
    persisting the customer data to the database, and generating a JWT token for the customer. \n
    
    **Args:** \n
        - db (Session): Database session dependency. \n
        - request (dict): Request body containing customer data.\n
    **Returns:** \n
        - JSONResponse: A JSON response with the status of the operation and relevant data or error messages. \n
    **Raises:** \n
        - ValidationError: If the request body validation fails. \n
        - IntegrityError: If there is a database integrity error (e.g., customer already exists). \n
        - Exception: If there is an error generating the JWT token.
    """
    
    logger = Logger()
    
    logger.log('INFO', f"[/api/v1/customers/] [POST] Persisting customer to database")

    try: 
        body = CustomerRequestBody(**request)
    except ValidationError as e:
        logger.log('ERROR', f"[/api/v1/customers/] [POST] [400] Error validating request body")

        errors_details = e.errors()
        
        error_response = ValidationErrorResponse(details=errors_details)
        
        return JSONResponse(content=error_response.model_dump(), status_code=status.HTTP_400_BAD_REQUEST)
    
    try:
        body_to_dict = body.model_dump()

        customer_repository = CustomerRepository(db)
    
        new_customer = customer_repository.create(body_to_dict)
    except IntegrityError as e:
        
        logger.log('ERROR', f"[/api/v1/customers/] [POST] [400] Error creating customer: {str(e)}")
        
        response = BadResponse(message='Customer already exists')
        
        return JSONResponse(content=response.model_dump(), status_code=status.HTTP_400_BAD_REQUEST)
    
    try:
        jwt_manager = JWTManager()
        
        token = jwt_manager.encode(body_to_dict)
    except Exception as e:
        
        logger.log('ERROR', f"[/api/v1/customers/] [POST] [500] Error generating token: {str(e)}")
        
        response = BadResponse(message='Possible error generating token')
        
        return JSONResponse(content=response.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    http_response = SuccessResponse(data={
        'customer': {'id': new_customer.id, 'email': new_customer.email},
        'token': token
    })

    logger.log('INFO', "[/api/v1/customers/] [POST] [201] Customer created successfully")
    
    return JSONResponse(content=http_response.model_dump(), status_code=status.HTTP_201_CREATED)


@router.put('/{id}')
def update_customer(db: Session = Depends(get_database_connection), decoded_token: dict = Depends(JWTBearerDependencie()), id: int = Path(..., title='Customer ID', description='Unique identity value for a Customer'), request: dict = Body(..., json_schema_extra=CustomerRequestBody.schema())):
    """
    Update a customer in the database.\n
    This endpoint replaces the customer data with the provided request body for the customer with the specified ID.\n
    It also generates a new JWT token for the updated customer. \n

    **Args:**\n
        - db (Session): Database session dependency.\n
        - decoded_token (dict): Decoded JWT token dependency.\n
        - id (int): Unique identity value for a Customer.\n
        - request (dict): Request body containing the customer data to update.\n
    **Returns:**\n
        - JSONResponse: JSON response with the status of the operation and any relevant data or error messages.\n
    **Raises:**\n
        - ValidationError: If the request body validation fails.\n
        - Exception: If there is an error generating the JWT token.\n
    **Logs:**\n
        - INFO: Logs the start and successful completion of the update operation.\n
        - ERROR: Logs any errors encountered during the process.\n
    **Responses:**\n
        - 400: Bad request if the request body validation fails.\n
        - 404: Not found if the customer with the specified ID does not exist.\n
        - 403: Forbidden if the logged-in customer does not have access to the specified resource.\n
        - 500: Internal server error if there is an error generating the JWT token.\n
        - 201: Created if the customer is updated successfully.\n
    """
    
    logger = Logger()
    
    logger.log('INFO', f"[/api/v1/customers/{id}] [PUT] Replacing customer with ID {id} from database")

    try:  
        body = CustomerRequestBody(**request)
    except ValidationError as e:
        
        logger.log('ERRO', f"[/api/v1/customers/{id}] [PUT] [400] Error validating request body")

        errors_details = e.errors()
        
        error_response = ValidationErrorResponse(details=errors_details)
        
        return JSONResponse(content=error_response.model_dump(), status_code=status.HTTP_400_BAD_REQUEST)

    customer_repository = CustomerRepository(db)

    customer = customer_repository.get_by_email(decoded_token['email'])

    body_to_dict = body.model_dump()

    if not customer:
        
        logger.log('ERROR', f"[/api/v1/customers/{id}] [PUT] [404] Customer with ID {id} not found")
        
        response = BadResponse(message='Customer not found')
        
        return JSONResponse(content=response.model_dump(), status_code=status.HTTP_404_NOT_FOUND)
    else:
        if customer.id != id:
            
            logger.log('ERROR', f"[/api/v1/customers/{id}] [PUT] [403] Forbidden access to customer with ID {id}")

            response = BadResponse(message='Customer logged in does not have access to this resource')

            return JSONResponse(content=response.model_dump(), status_code=status.HTTP_403_FORBIDDEN)
        else:
    
            updated_customer = customer_repository.update(id, body_to_dict)

            logger.log('INFO', f"[/api/v1/customers/{id}] [PUT] [201] Customer with ID {id} updated successfully")

            try:
                jwt_manager = JWTManager()
                
                token = jwt_manager.encode(body_to_dict)
            except Exception as e:
                
                logger.log('ERROR', f"[/api/v1/customers/{id}] [PUT] [500] Error generating token: {str(e)}")
                
                response = BadResponse(message='Possible error generating token')
                
                return JSONResponse(content=response.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            response = SuccessResponse(data={
                'token': token,
                'customer': {
                    'id': updated_customer.id,
                    'email': updated_customer.email
                    }
                }
            )
            return JSONResponse(content=response.model_dump(), status_code=status.HTTP_201_CREATED)


@router.delete('/{id}')
def delete_customer(decoded_token: dict = Depends(JWTBearerDependencie()),db: Session = Depends(get_database_connection), id: int = Path(...,title='Customer ID',description='Unique identity value for a Customer')):
    """
    Deletes a customer from the database.\n

    This endpoint deletes a customer from the database using the provided customer ID.\n
    It also verifies that the customer making the request has access to the specified customer ID.\n


    **Args:**\n
        - decoded_token (dict): The decoded JWT token containing user information.\n
        - db (Session): The database session dependency.\n
        - id (int): The unique identity value for a customer.\n
    **Returns:**\n
        - 404 Not Found: If the customer with the given ID does not exist.\n
        - 403 Forbidden: If the logged-in customer does not have access to delete the specified customer.\n
        - 204 No Content: If the customer is successfully deleted.\n
    **Logs:**\n
        - INFO: When attempting to delete a customer.\n
        - ERROR: If the customer with the given ID does not exist.\n
        - ERROR: If the logged-in customer does not have access to delete the specified customer.\n
        - INFO: If the customer is successfully deleted.\n
    """
    
    logger = Logger()
    
    logger.log('INFO', f"[/api/v1/customers/{id}] [DELETE] Deleting customer with ID {id} from database")

    customer_repository = CustomerRepository(db)

    customer = customer_repository.get_by_email(decoded_token['email'])

    if not customer:
        
        logger.log('ERROR', f"[/api/v1/customers/{id}] [DELETE] [404] Customer with ID {id} not found")
        
        response = BadResponse(message='Customer not found')
        
        return JSONResponse(content=response.model_dump(), status_code=status.HTTP_404_NOT_FOUND)
    else:
        if customer.id != id:
            
            logger.log('ERROR', f"[/api/v1/customers/{id}] [DELETE] [403] Forbidden access to customer with ID {id}")

            response = BadResponse(message='Customer logged in does not have access to this resource')

            return JSONResponse(content=response.model_dump(), status_code=status.HTTP_403_FORBIDDEN)
        else:
            logger.log('INFO', f"[/api/v1/customers/{id}] [DELETE] [204] Customer with ID {id} deleted successfully")

            customer_repository.delete(id)

            response = SuccessResponse()

            return Response(status_code=status.HTTP_204_NO_CONTENT)
