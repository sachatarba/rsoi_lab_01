from typing import Optional, Dict
from pydantic import BaseModel, ConfigDict


class ErrorResponse(BaseModel):
    message: str


class ValidationErrorResponse(BaseModel):
    message: str
    errors: Dict[str, str]


class PersonRequest(BaseModel):
    name: str
    age: Optional[int] = None
    address: Optional[str] = None
    work: Optional[str] = None

class PersonUpdateRequest(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    address: Optional[str] = None
    work: Optional[str] = None

class PersonResponse(BaseModel):
    id: int
    name: str
    age: Optional[int] = None
    address: Optional[str] = None
    work: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)