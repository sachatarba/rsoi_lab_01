from typing import List
from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.person import PersonRequest, PersonResponse, PersonUpdateRequest
from app.services.person_service import PersonService

router = APIRouter(
    prefix="/persons",
    tags=["Persons"]
)

def get_person_service(db: Session = Depends(get_db)):
    return PersonService(db)

@router.post("/",
             status_code=status.HTTP_201_CREATED,
             summary="Create new Person")
def create_person(
    person: PersonRequest,
    response: Response,
    service: PersonService = Depends(get_person_service)
):
    created_person = service.create_person(person)
    response.headers["Location"] = f"/api/v1/persons/{created_person.id}"
    return

@router.get("/",
            response_model=List[PersonResponse],
            summary="Get all Persons")
def read_persons(
    skip: int = 0, limit: int = 100, service: PersonService = Depends(get_person_service)
):
    return service.get_all_persons(skip=skip, limit=limit)

@router.get("/{person_id}",
            response_model=PersonResponse,
            summary="Get Person by ID")
def read_person(
    person_id: int, service: PersonService = Depends(get_person_service)
):
    return service.get_person(person_id)

@router.patch("/{person_id}",
              response_model=PersonResponse,
              summary="Update Person by ID")
def update_person(
    person_id: int,
    person: PersonUpdateRequest,
    service: PersonService = Depends(get_person_service)
):
    return service.update_person(person_id, person)


@router.delete("/{person_id}",
               status_code=status.HTTP_204_NO_CONTENT,
               summary="Remove Person by ID")
def delete_person(
    person_id: int, service: PersonService = Depends(get_person_service)
):
    service.delete_person(person_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)