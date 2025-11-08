from unittest.mock import MagicMock
import pytest
from fastapi import HTTPException

from app.schemas.person import PersonRequest, PersonUpdateRequest
from app.services.person_service import PersonService
from app.models.person import Person

def test_get_person_success():
    """
    Unit-тест для PersonService.get_person, случай успешного нахождения.
    """
    # 1. Arrange (Подготовка)
    mock_repo = MagicMock()
    mock_repo.get_by_id.return_value = Person(id=1, name="Test User", age=30)


    service = PersonService(db=None)
    service.repository = mock_repo

    result = service.get_person(person_id=1)

    # 3. Assert (Проверка)
    assert result.id == 1
    assert result.name == "Test User"
    mock_repo.get_by_id.assert_called_once_with(1)


def test_get_person_not_found():
    """
    Unit-тест для PersonService.get_person, случай когда запись не найдена.
    """
    # 1. Arrange
    mock_repo = MagicMock()
    mock_repo.get_by_id.return_value = None

    service = PersonService(db=None)
    service.repository = mock_repo

    # 2. Act & 3. Assert
    with pytest.raises(HTTPException) as exc_info:
        service.get_person(person_id=999)

    assert exc_info.value.status_code == 404
    mock_repo.get_by_id.assert_called_once_with(999)


def test_create_person():
    """Unit-тест для создания нового пользователя."""
    # 1. Arrange
    mock_repo = MagicMock()
    person_to_create = PersonRequest(name="New Person", age=22)

    created_person_model = Person(id=1, name=person_to_create.name, age=person_to_create.age)
    mock_repo.create.return_value = created_person_model

    service = PersonService(db=None)
    service.repository = mock_repo

    # 2. Act
    result = service.create_person(person_data=person_to_create)

    # 3. Assert
    assert result.id is not None
    assert result.name == person_to_create.name
    mock_repo.create.assert_called_once_with(person_to_create.model_dump())


def test_update_person_success():
    """Unit-тест для успешного обновления пользователя."""
    # 1. Arrange
    mock_repo = MagicMock()
    person_id = 1
    update_data = PersonUpdateRequest(name="Updated Name")

    updated_person_model = Person(id=person_id, name=update_data.name)
    mock_repo.update.return_value = updated_person_model

    service = PersonService(db=None)
    service.repository = mock_repo

    # 2. Act
    result = service.update_person(person_id=person_id, person_data=update_data)

    # 3. Assert
    assert result.name == "Updated Name"
    mock_repo.update.assert_called_once_with(person_id, update_data.model_dump(exclude_unset=True))


def test_delete_person_success():
    """Unit-тест для успешного удаления пользователя."""
    # 1. Arrange
    mock_repo = MagicMock()
    person_id = 1

    deleted_person_model = Person(id=person_id, name="UserToDelete")
    mock_repo.delete.return_value = deleted_person_model

    service = PersonService(db=None)
    service.repository = mock_repo

    # 2. Act
    service.delete_person(person_id=person_id)

    # 3. Assert
    mock_repo.delete.assert_called_once_with(person_id)