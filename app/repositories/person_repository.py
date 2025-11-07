from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.person import Person

class PersonRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, person_id: int) -> Optional[Person]:
        return self.db.query(Person).filter(Person.id == person_id).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Person]:
        return self.db.query(Person).offset(skip).limit(limit).all()

    def create(self, person_data: dict) -> Person:
        db_person = Person(**person_data)
        self.db.add(db_person)
        self.db.commit()
        self.db.refresh(db_person)
        return db_person

    def update(self, person_id: int, person_data: dict) -> Optional[Person]:
        db_person = self.get_by_id(person_id)
        if db_person:
            for key, value in person_data.items():
                setattr(db_person, key, value)
            self.db.commit()
            self.db.refresh(db_person)
        return db_person

    def delete(self, person_id: int) -> Optional[Person]:
        db_person = self.get_by_id(person_id)
        if db_person:
            self.db.delete(db_person)
            self.db.commit()
        return db_person