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


class SuccessResponse(BaseModel):
    status: Optional[str] = Field('success', example='success')
    message: Optional[str] = Field('Operation successful', example='Operation successful')
    data: Optional[Union[list, dict]]= Field({}, example={})
    timestamp: Optional[str] = Field(datetime.now().isoformat(), example="2021-01-01T00:00:00")
