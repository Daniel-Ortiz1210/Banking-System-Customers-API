import pytest
from fastapi.testclient import TestClient
from faker import Faker

from main import app

def test_login():
    client = TestClient(app)
    faker = Faker()

    request_payload = {
        'first_name': 'John',
        'last_name': 'Doe',
        'email': faker.email(),
        'phone': '+123456789900',
        'password': 'mockpassword'
    }   

    response = client.post('/api/v1/auth/login', json={
        'email': request_payload['email'],
        'password': request_payload['password']
    })
    
    assert response.status_code == 404
    assert response.json()['message'] == 'Customer not found'

    response = client.post('/api/v1/customers/', json=request_payload)
    
    assert response.status_code == 201
    assert response.json()['success'] == True

    customer_id = response.json()['data']['customer']['id']

    response = client.post('/api/v1/auth/login', json={
        'email': request_payload['email'],
        'password': 'wrongpassword'
    })

    assert response.status_code == 401
    assert response.json()['message'] == 'Invalid password'

    response = client.post('/api/v1/auth/login', json={
        'email': request_payload['email'],
        'password': request_payload['password']
    })

    assert response.status_code == 200
    assert response.json()['success'] == True
    assert 'token' in response.json()['data']

    response = client.delete(f'/api/v1/customers/{customer_id}', headers={
        'Authorization': f'Bearer {response.json()["data"]["token"]}'
    })

    assert response.status_code == 204

