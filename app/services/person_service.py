from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.repositories.person_repository import PersonRepository
from app.schemas.person import PersonRequest, PersonUpdateRequest
from app.models.person import Person


class PersonService:
    def __init__(self, db: Session):
        self.repository = PersonRepository(db)

    def get_person(self, person_id: int):
        person = self.repository.get_by_id(person_id)
        if not person:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Person with id {person_id} not found"
            )
        return person

    def get_all_persons(self, skip: int = 0, limit: int = 100):
        return self.repository.get_all(skip=skip, limit=limit)

    def create_person(self, person_data: PersonRequest) -> Person:
        return self.repository.create(person_data.model_dump())

    def update_person(self, person_id: int, person_data: PersonUpdateRequest):
        update_data = person_data.model_dump(exclude_unset=True)
        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No fields to update provided"
            )

        updated_person = self.repository.update(person_id, update_data)

        if not updated_person:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Person with id {person_id} not found"
            )
        return updated_person

    def delete_person(self, person_id: int):
        deleted_person = self.repository.delete(person_id)
        if not deleted_person:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Person with id {person_id} not found"
            )
        return