from fastapi.testclient import TestClient
from main import app
import unittest

client = TestClient(app)

@unittest.skip("Teste de criação de caminhão")
def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World Autocampos!"}