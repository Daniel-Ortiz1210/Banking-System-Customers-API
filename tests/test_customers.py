import pytest
from fastapi.testclient import TestClient
from faker import Faker

from main import app


def test_customer_endpoints():
    client = TestClient(app)
    faker = Faker()

    request_payload = {
        'first_name': 'John',
        'last_name': 'Doe',
        'email': faker.email(),
        'phone': '+1234567890',
        'password': 'Asdfghjk1'
    }   

    response = client.post('/api/v1/customers/', json={
        **request_payload,
        'phone': '1234567a91'
        }
    )

    assert response.status_code == 400

    response = client.post('/api/v1/customers/', json={
        **request_payload,
        'email': 'test_email@mail'
        }
    )

    assert response.status_code == 400

    response = client.post('/api/v1/customers/', json=request_payload)

    assert response.status_code == 201
    assert response.json()['success'] == True

    customer_id = response.json()['data']['customer']['id']
    customer_email = response.json()['data']['customer']['email']
    token = response.json()['data']['token']

    response = client.post('/api/v1/customers/', json=request_payload)
    
    assert response.status_code == 400

    # Test get customer by id
    response = client.get('/api/v1/customers/6456482840', headers={
        'Authorization': f"Bearer {token}"
    })

    assert response.status_code == 403
    assert response.json()['message'] == 'Customer logged in does not have access to this resource'

    response = client.get(f'/api/v1/customers/{customer_id}', headers={
        'Authorization': f"Bearer {token}"
    })

    assert response.status_code == 200
    assert response.json()['success'] == True
    assert response.json()['data']['id'] == customer_id

    # Test update customer

    updated_payload = {
        'first_name': 'Jane',
        'last_name': 'McGill',
        'email': faker.email(),
        'phone': '+1234567001',
        'password': 'Asdfghjk1'
        }
    response = client.put(f'/api/v1/customers/100', json=updated_payload,
        headers={
            'Authorization': f"Bearer {token}"
        })

    assert response.status_code == 403
    assert response.json()['message'] == 'Customer logged in does not have access to this resource'

    response = client.put(f'/api/v1/customers/{customer_id}', json={**updated_payload, 'email': 'vtrcavue'}, headers={
        'Authorization': f"Bearer {token}"
    })

    assert response.status_code == 400

    response = client.put(f'/api/v1/customers/{customer_id}', json=updated_payload, headers={
        'Authorization': f"Bearer {token}"
    })

    assert response.status_code == 201
    assert response.json()['success'] == True
    assert response.json()['data']['customer']['email'] == updated_payload['email']

    token = response.json()['data']['token']

    # Test delete customer
    response = client.delete('/api/v1/customers/7365448204', headers={
        'Authorization': f"Bearer {token}"
    })

    assert response.status_code == 403

    response = client.delete(f'/api/v1/customers/{customer_id}', headers={
        'Authorization': f"Bearer {token}"
    })

    assert response.status_code == 204
