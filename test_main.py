import requests


def test_post_access_token():
    headers = {
        "accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    request_data = {
        "client_id": "",
        "client_secret": "",
        "scope": "",
        "grant_type": "",
        "refresh_token": "",
        "username": "test@test.com",
        "password": "test"
    }

    response = requests.post("http://127.0.0.1:8000/token", data=request_data, headers=headers)

    assert response.status_code == 200
    token = response.json()['access_token']
    return token


def test_read_users():
    token = test_post_access_token()

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {token}"
    }

    response = requests.get('http://127.0.0.1:8000/users/', headers=headers)
    assert response.status_code == 200

def test_read_users_me():
    token = test_post_access_token()

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {token}"
    }

    response = requests.get('http://127.0.0.1:8000/users/me', headers=headers)
    assert response.status_code == 200

def test_list_movies():
    response = requests.get('http://127.0.0.1:8000/movies/')
    assert response.status_code == 200

def test_get_movie_ratings():
    response = requests.get('http://127.0.0.1:8000/movies/1/ratings/')
    assert response.status_code == 200

def test_get_movie():
    response = requests.get('http://127.0.0.1:8000/movies/1/')
    assert response.status_code == 200
