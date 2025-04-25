from http.client import responses

from fastapi.testclient import TestClient
from starlette.responses import Response

from src.main import app

client = TestClient(app)

users = [
    {
        'id': 1,
        'name': 'Ivan Ivanov',
        'email': 'i.i.ivanov@mail.com',
    },
    {
        'id': 2,
        'name': 'Petr Petrov',
        'email': 'p.p.petrov@mail.com',
    }
]

def test_get_existed_user():
    '''Получение существующего пользователя'''

    response = client.get("/api/v1/user", params={'email': users[0]['email']})
    assert response.status_code == 200
    assert response.json() == users[0]

def test_get_unexisted_user():
    '''Получение несуществующего пользователя'''
    response =  client.get("/api/v1/user", params={'email': "ABOBA"})
    assert response.status_code == 404


def test_create_user_with_valid_email():
    '''Создание пользователя с уникальной почтой'''
    new_user = {
        'id': 3,
        'name': 'New User',
        'email': 'new.user@mail.com'
    }
    response = client.post("/api/v1/user", json=new_user)
    assert response.status_code == 201
    assert response.json() == new_user['id']

    # Проверяем, что пользователь действительно создан
    response = client.get("/api/v1/user", params={'email': new_user['email']})
    assert response.status_code == 200
    assert response.json() == new_user

def test_create_user_with_invalid_email():
    '''Создание пользователя с почтой, которую использует другой пользователь'''
    existing_email = users[0]['email']
    new_user = {
        'id': 3,
        'name': 'New User',
        'email': existing_email
    }
    response = client.post("/api/v1/user", json=new_user)
    assert response.status_code == 409
    assert "email already exists" in response.json().get("detail", "").lower()


def test_delete_user():
    #Удаление пользователя
    test_user = {
        'id': 999,
        'name': 'Test User',
        'email': 'test.user@mail.com'
    }
    client.post("/api/v1/user", json=test_user)

    response = client.delete("/api/v1/user/", params={"email": test_user['email']})
    assert response.status_code == 204

    response = client.get("/api/v1/user", params={'email': test_user['email']})
    assert response.status_code == 404
