import pytest
import requests

BASE_URL = "https://jsonplaceholder.typicode.com"


# создание нового ресурса-бар harat's
def test_create_post():
    payload = {"title": "harat's", "body": "bar", "userId": 1}
    response = requests.post(f"{BASE_URL}/posts", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 101
    assert data["title"] == "harat's"


# обновление ресурса
def test_update_post():
    payload = {
        "id": 1,
        "title": "new harat's",
        "body": "refreshed bar design",
        "userId": 1,
    }
    response = requests.put(f"{BASE_URL}/posts/1", json=payload)
    assert response.status_code == 200
    assert response.json()["title"] == "new harat's"


# удаление ресурса
def test_delete_post():
    response = requests.delete(f"{BASE_URL}/posts/1")
    assert response.status_code == 200


# получение постов конкретных пользователей
@pytest.mark.parametrize("user_id", [2, 7, 10])
def test_get_posts_by_user(user_id):
    response = requests.get(f"{BASE_URL}/posts", params={"userId": user_id})
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    for post in data:
        assert post["userId"] == user_id


# проверка комментариев к посту
@pytest.mark.parametrize("post_id", [1, 2])
def test_get_comments_for_post(post_id):
    response = requests.get(f"{BASE_URL}/posts/{post_id}/comments")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    for comment in data:
        assert comment["postId"] == post_id
        assert "email" in comment
