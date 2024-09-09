from httpx import AsyncClient
import pytest


@pytest.mark.parametrize("username,password,status_code", [
    ("Dima", "Malikov", 200),
    ("test", "test", 409),
    ("Transformer", "desept2012", 200),
])
async def test_register_user(username, password, status_code, ac: AsyncClient):
    response = await ac.post("/auth/register", json={
        "username": username,
        "password": password
    })

    assert response.status_code == status_code


@pytest.mark.parametrize("username,password,status_code", [
    ("test", "test", 200),
    ("test1", "test1", 200),
    ("test2", "test1", 401),
    ("test5", "test5", 401),
])
async def test_login_user(username, password, status_code, ac: AsyncClient):
    response = await ac.post("/auth/login", json={
        "username": username,
        "password": password
    })

    assert response.status_code == status_code
