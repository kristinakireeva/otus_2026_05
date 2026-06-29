import pytest
import requests


BASE_URL = "https://dog.ceo/api"


# получение списка пород всех собак
def test_get_all_breeds():
    response = requests.get(f"{BASE_URL}/breeds/list/all")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "message" in data
    assert isinstance(data["message"], dict)


# получение случайного изображения собаки
def test_get_random_images():
    response = requests.get(f"{BASE_URL}/breeds/image/random")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "dog.ceo" in data["message"]


# запрос несуществующей породы
def test_get_sub_breeds_not_found():
    response = requests.get(f"{BASE_URL}/breed/nonexistentbreed/list")
    assert response.status_code == 404
    data = response.json()
    assert data["status"] == "error"
    assert "Breed not found" in data["message"]


# получение изображений конкретных пород
@pytest.mark.parametrize("breed", ["collie", "hound", "retriever"])
def test_get_breed_images(breed):
    response = requests.get(f"{BASE_URL}/breed/{breed}/images")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert len(data["message"]) > 0


# запрос определенного количества рандомных фото
@pytest.mark.parametrize("count", [1, 4, 9])
def test_get_multiple_random_images(count):
    response = requests.get(f"{BASE_URL}/breeds/image/random/{count}")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert len(data["message"]) == count
