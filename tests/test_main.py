import requests

BASE_URL = "http://localhost:8080"


def test_create_document():
    # Send a POST request to create a new document
    payload = {"title": "Test document", "content": "This is a test document."}
    response = requests.post(f"{BASE_URL}/documents/", json=payload)

    # Check that the response status code is 200 OK
    assert response.status_code == 200

    # Check that the response JSON matches the expected document data
    assert response.json() == {"id": 1, "title": "Test document", "content": "This is a test document."}


def test_get_document():
    # Send a GET request to retrieve a document
    response = requests.get(f"{BASE_URL}/documents/1")

    # Check that the response status code is 200 OK
    assert response.status_code == 200

    # Check that the response JSON matches the expected document data
    assert response.json() == {"id": 1, "title": "Test document", "content": "This is a test document."}


def test_list_documents():
    # Send a GET request to retrieve a list of documents
    response = requests.get(f"{BASE_URL}/documents/")

    # Check that the response status code is 200 OK
    assert response.status_code == 200

    # Check that the response JSON matches the expected list of documents
    assert response.json() == [{"id": 1, "title": "Test document", "content": "This is a test document."}]


def test_healthcheck():
    response = requests.get(f"{BASE_URL}/__health")
    assert response.status_code == 200
