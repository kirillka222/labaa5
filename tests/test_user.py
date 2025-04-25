from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)

# Существующие пользователи
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
    response = client.get("/api/v1/user", params={'email': 'asdqwe'})
    assert response.status_code == 404
    assert response.json() == users[0]

def test_create_user_with_valid_email():
    '''Создание пользователя с уникальной почтой'''
    new_user = {
        'id': 3,
        'name': 'Kirill Kirill',
        'email': 'k.k.kivanov@mail.com',
    }
    response = client.get("/api/v1/user", json=new_user)
    assert response.status_code == 201
    assert response.json() == new_user['id']

    # проверяем что пользователь действительно создан:
    response = client.get("/api/v1/user", params={'email': new_user['email']})
    assert response.status_code == 200
    assert response.json() == new_user

def test_create_user_with_invalid_email():
    '''Создание пользователя с почтой, которую использует другой пользователь'''
    email = users[0]['email']
    new_user = {
        'id': 3,
        'name': 'Kirill Kirill',
        'email': email
    }
    response = client.post("/api/v1/user", json=new_user)
    assert response.status_code == 409
    assert "адрес электронной почты уже существует" in response.json().get("detail", "").lower()
def test_delete_user():
    '''Удаление пользователя'''
    test_user = {
        'id': 999,
        'name': 'Test User',
        'email': 'test.user@gmail.com'
    }

    client.post("/api/v1/user", json=test_user)

    response = client.delete("/api/v1/user/", params={"email": test_user['email']})
    assert response.status_code == 204

    response = client.get("/api/v1/user", params={'email': test_user['email']})
    assert response.status_code == 404