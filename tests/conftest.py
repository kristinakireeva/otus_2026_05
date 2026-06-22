import pytest
from src.rectangle import Rectangle


@pytest.fixture
def default_rectangle():
    # Setup
    rectangle = Rectangle(3, 5)

    yield rectangle

    # Teardown
    del rectangle