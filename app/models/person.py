from sqlalchemy import Column, Integer, String
from app.core.database import Base

class Person(Base):
    __tablename__ = "persons"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    age = Column(Integer)
    address = Column(String, nullable=True)
    work = Column(String, nullable=True)