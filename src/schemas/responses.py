from pydantic import BaseModel, field_validator, Field
from datetime import datetime
from typing import List, Optional, Dict, Union

class ValidationErrorResponse(BaseModel):
    status: Optional[str] = Field('error', example='error')
    details: List[Dict[str, str]] = Field(..., example=[])
    error_type: Optional[str] = Field('ValidationError', example="ValidationError")
    timestamp: Optional[str] = Field(datetime.now().isoformat(), example="2021-01-01T00:00:00")

    @field_validator('details', mode='before')
    def construct_details(cls, value):
        details = []
        for error in value:
            details.append(
                {
                    'field': error['loc'][0],
                    'message': error['msg']
                }
            )
        return details

class HttpResponse(BaseModel):
    success: Optional[bool] = Field(True, example=True)
    message: Optional[str] = Field('Operation successful', example='Operation successful')
    timestamp: Optional[str] = Field(datetime.now().isoformat(), example="2021-01-01T00:00:00")

class SuccessResponse(HttpResponse):
    data: Optional[Union[list, dict]]= Field({}, example={})

class BadResponse(HttpResponse):
    success: Optional[bool] = Field(False, example=False)
    detail: Optional[Union[list, dict]]= Field({}, example={})
