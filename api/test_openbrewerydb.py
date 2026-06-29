import pytest
import requests

BASE_URL = "https://api.openbrewerydb.org/v1/breweries"


# получение списка пивоварен
def test_get_breweries_list():
    response = requests.get(BASE_URL)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


# получение пивоварни по ID
def test_get_single_brewery():
    list_response = requests.get(BASE_URL)
    assert list_response.status_code == 200
    breweries = list_response.json()
    assert len(breweries) > 0, "Список пивоварен пуст"
    first_brewery_id = breweries[0]["id"]
    response = requests.get(f"{BASE_URL}/{first_brewery_id}")
    assert response.status_code == 200
    assert response.json()["id"] == first_brewery_id


# получение случайной пивоварни
def test_get_random_brewery():
    response = requests.get(f"{BASE_URL}/random")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert "id" in data[0]


# фильтрация списка по типу пивоварни, выбрала самые популярные
@pytest.mark.parametrize("brewery_type", ["micro", "regional", "brewpub"])
def test_filter_breweries_by_type(brewery_type):
    params = {"by_type": brewery_type, "per_page": 2}
    response = requests.get(BASE_URL, params=params)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


# поиск пивоварен по ключевым словам
@pytest.mark.parametrize("query", ["Lonesome Pine", "Double Bluff", "Jester King"])
def test_search_breweries(query):
    params = {"query": query}
    response = requests.get(f"{BASE_URL}/search", params=params)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
