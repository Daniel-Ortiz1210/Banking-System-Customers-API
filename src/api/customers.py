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
def get_all_customers(
    db: Session = Depends(get_database_connection),
    ) -> Page[CustomerBase]:
    
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
def create_customer(
    db: Session = Depends(get_database_connection),
    request: dict = Body(
        ...,
        json_schema_extra=CustomerBase.schema()
        )
    ):
    
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
def update_customer(
    db: Session = Depends(get_database_connection),
    decoded_token: dict = Depends(JWTBearerDependencie()),
    id: int = Path(
        ...,
        title='Customer ID',
        description='Unique identity value for a Customer'
        ),
    request: dict = Body(..., json_schema_extra=CustomerRequestBody.schema())
    ):
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
def delete_customer(
    decoded_token: dict = Depends(JWTBearerDependencie()),
    db: Session = Depends(get_database_connection),
    id: int = Path(
        ...,
        title='Customer ID',
        description='Unique identity value for a Customer'
        ),
    ):
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
