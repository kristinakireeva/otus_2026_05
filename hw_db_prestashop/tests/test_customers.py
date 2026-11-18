import uuid
import pytest
from db_helpers.db import  (
    create_customer,
    delete_customer,
    get_customer_by_id,
    update_customer,
)


@pytest.fixture
def created_customer(connection):
    """Фикстура создает тестового клиента и удаляет его после завершения теста."""
    unique_suffix = uuid.uuid4().hex[:8]
    customer_data = {
        "firstname": "Ivan",
        "lastname": "Petrov",
        "email": f"ivan_{unique_suffix}@test.com",
    }
    customer_id = create_customer(connection, customer_data)
    yield customer_id, customer_data
    delete_customer(connection, customer_id)


def test_create_customer(connection):
    """Позитивный тест создания нового клиента."""
    unique_suffix = uuid.uuid4().hex[:8]
    customer_data = {
        "firstname": "Anna",
        "lastname": "Smirnova",
        "email": f"anna_{unique_suffix}@test.com",
    }

    customer_id = create_customer(connection, customer_data)
    try:
        assert isinstance(customer_id, int)
        assert customer_id > 0

        db_customer = get_customer_by_id(connection, customer_id)
        assert db_customer is not None
        assert db_customer["firstname"] == customer_data["firstname"]
        assert db_customer["lastname"] == customer_data["lastname"]
        assert db_customer["email"] == customer_data["email"]
    finally:
        delete_customer(connection, customer_id)


def test_update_existing_customer(connection, created_customer):
    """Позитивный тест обновления полей firstname, lastname и email."""
    customer_id, _ = created_customer
    unique_suffix = uuid.uuid4().hex[:8]
    new_data = {
        "firstname": "UpdatedName",
        "lastname": "UpdatedSurname",
        "email": f"updated_{unique_suffix}@test.com",
    }

    affected_rows = update_customer(connection, customer_id, new_data)
    assert affected_rows == 1

    updated_customer = get_customer_by_id(connection, customer_id)
    assert updated_customer is not None
    assert updated_customer["firstname"] == new_data["firstname"]
    assert updated_customer["lastname"] == new_data["lastname"]
    assert updated_customer["email"] == new_data["email"]


def test_update_non_existent_customer(connection):
    """Негативный тест обновления несуществующего клиента."""
    non_existent_id = 999_999_999
    assert get_customer_by_id(connection, non_existent_id) is None

    affected_rows = update_customer(
        connection,
        non_existent_id,
        {
            "firstname": "Ghost",
            "lastname": "User",
            "email": "ghost@test.com",
        },
    )
    assert affected_rows == 0


def test_delete_existing_customer(connection):
    """Позитивный тест удаления существующего клиента."""
    unique_suffix = uuid.uuid4().hex[:8]
    customer_id = create_customer(
        connection,
        {
            "firstname": "DeleteMe",
            "lastname": "User",
            "email": f"delete_{unique_suffix}@test.com",
        },
    )
    assert get_customer_by_id(connection, customer_id) is not None

    affected_rows = delete_customer(connection, customer_id)
    assert affected_rows == 1
    assert get_customer_by_id(connection, customer_id) is None


def test_delete_non_existent_customer(connection):
    """Негативный тест удаления несуществующего клиента."""
    non_existent_id = 999_999_999
    assert get_customer_by_id(connection, non_existent_id) is None

    affected_rows = delete_customer(connection, non_existent_id)
    assert affected_rows == 0
