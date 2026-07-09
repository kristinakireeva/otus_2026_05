import requests


def test_url_status(target_url, expected_status):
    response = requests.get(target_url, timeout=10)
    assert response.status_code == expected_status, \
        f"Ожидали {expected_status}, получили {response.status_code}"
