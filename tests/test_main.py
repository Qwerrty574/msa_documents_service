import requests as req

api_url = 'http://localhost:8080'


def test_healthcheck():
    response = req.get(f'{api_url}/__health')
    assert response.status_code == 200
  