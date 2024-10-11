from tests.client import client 
import json

def test_registering_with_bad_email():
    data = {"email": "testtest.com", "password": "qwerqwer", "fullname": "Test User"}
    response = client.post(url="/user/signup",json=json.dumps(data))
    assert response.status_code == 422
    assert response.json() == {'detail': [{'input': '{"email": "testtest.com", "password": "qwerqwer", "fullname": "Test User"}', 'loc': ['body'], 'msg': 'Input should be a valid dictionary or object to extract fields from', 'type': 'model_attributes_type'}]}

def test_bad_nopassword_signup():
    response = client.post("/user/signup", json={"email": "test@test.com", "fullname": "Test User"})
    assert response.status_code == 422
    assert response.json() == {'detail': [{'input': {'email': 'test@test.com', 'fullname': 'Test User'}, 'loc': ['body', 'password'], 'msg': 'Field required', 'type': 'missing'}]} 

def test_signup():
    response = client.post("/user/signup", json={"email": "test@test.com", "password": "qwerqwer", "fullname": "Test User"})
    assert response.status_code == 200
    token = response.json()["access_token"]
    assert token is not None
# 
# def test_duplicate_signup():
    response = client.post("/user/signup", json={"email": "test@test.com", "password": "qwerqwer", "fullname": "Test User"})
    assert response.status_code == 409
    assert response.json() == { "detail": "User with this email already exists."}
