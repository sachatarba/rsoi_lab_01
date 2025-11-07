from fastapi import FastAPI
from app.api.v1 import persons  # Импортируем наш роутер

app = FastAPI(
    title="Persons API",
    description="Lab 1 API for managing persons",
    version="1.0.0"
)

app.include_router(persons.router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Persons API"}