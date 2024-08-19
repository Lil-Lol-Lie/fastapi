from app import schemas
import pytest
from jose import jwt
from app.config import settings

@pytest.fixture
def test_user(client):
    user_data = {"email": "love@gmail.com", "password": "123"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user
    
    
def test_create_user(client):
    res = client.post("/users/", json={"email": "love@gmail.com", "password": "123"})
    new_user = schemas.UserOut(**res.json())
    print(res.json())
    assert res.status_code == 201
    assert new_user.email == "love@gmail.com"
    
def test_login_user(client, test_user):
    res = client.post("/login/", data={"username": test_user["email"], "password": test_user["password"]})
    login_token = schemas.Token(**res.json())
    payload = jwt.decode(login_token.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get("user_id")
    assert res.status_code == 200
    assert login_token.token_type == "bearer"
    assert id == test_user["id"]
    
@pytest.mark.parametrize("email, password, status_code", [
     ("love@gmail.com", "123", 200), 
     ("hate@gmail.com", "pass", 403)])   
def test_incorrect_login(test_user, client, email, password, status_code):
    res = client.post("/login", data={"username": email, "password": password})
    assert res.status_code == status_code
    #assert res.json().get("detail") == "Invalid Credentials"
    