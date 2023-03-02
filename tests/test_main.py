import requests

BASE_URL = "http://localhost:8080"


def test_create_document():
    payload = {"title": "Test document", "content": "This is a test document."}
    response = requests.post(f"{BASE_URL}/documents/", json=payload)
    assert response.status_code == 200
    assert response.json() == {"id": 1, "title": "Test document", "content": "This is a test document."}


def test_get_document():
    response = requests.get(f"{BASE_URL}/documents/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "title": "Test document", "content": "This is a test document."}


def test_list_documents():
    response = requests.get(f"{BASE_URL}/documents/")
    assert response.status_code == 200
    assert response.json() == [{"id": 1, "title": "Test document", "content": "This is a test document."}]


def test_healthcheck():
    response = requests.get(f"{BASE_URL}/__health")
    assert response.status_code == 200
