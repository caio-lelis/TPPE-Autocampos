import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.core.session import Base
from main import app

# Configuração do banco de dados de teste (SQLite em memória)
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Sobrescreve a dependência get_db para usar o banco de teste
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides = {}
from src.admin.admin_endpoint import get_db
app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_and_teardown():
    # Cria as tabelas antes de cada teste
    Base.metadata.create_all(bind=engine)
    yield
    # Limpa as tabelas após cada teste
    Base.metadata.drop_all(bind=engine)

def test_create_admin_success():
    payload = {"usuario_id": 1, "is_admin": True}
    response = client.post("/admins/create", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["usuario_id"] == 1
    assert data["is_admin"] is True
    assert "id" in data

def test_create_admin_fail_duplicate():
    payload = {"usuario_id": 1, "is_admin": True}
    client.post("/admins/create", json=payload)
    # Tenta criar o mesmo admin novamente (ajuste conforme sua lógica de unicidade)
    response = client.post("/admins/create", json=payload)
    assert response.status_code == 400

def test_get_all_admins_empty():
    response = client.get("/admins/get")
    assert response.status_code == 200
    assert response.json() == []

def test_get_all_admins_with_data():
    payload = {"usuario_id": 1, "is_admin": True}
    client.post("/admins/create", json=payload)
    response = client.get("/admins/get")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["usuario_id"] == 1

def test_get_admin_by_id_success():
    payload = {"usuario_id": 1, "is_admin": True}
    create_resp = client.post("/admins/create", json=payload)
    admin_id = create_resp.json()["id"]
    response = client.get(f"/admins/get/{admin_id}")
    assert response.status_code == 200
    assert response.json()["id"] == admin_id

def test_get_admin_by_id_not_found():
    response = client.get("/admins/get/999")
    assert response.status_code == 404

def test_update_admin_success():
    payload = {"usuario_id": 1, "is_admin": True}
    create_resp = client.post("/admins/create", json=payload)
    admin_id = create_resp.json()["id"]
    update_payload = {"usuario_id": 2, "is_admin": False}
    response = client.put(f"/admins/update/{admin_id}", json=update_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["usuario_id"] == 2
    assert data["is_admin"] is False

def test_update_admin_not_found():
    update_payload = {"usuario_id": 2, "is_admin": False}
    response = client.put("/admins/update/999", json=update_payload)
    assert response.status_code == 404

def test_delete_admin_success():
    payload = {"usuario_id": 1, "is_admin": True}
    create_resp = client.post("/admins/create", json=payload)
    admin_id = create_resp.json()["id"]
    response = client.delete(f"/admins/delete/{admin_id}")
    assert response.status_code == 200
    # Verifica que foi removido
    get_resp = client.get(f"/admins/get/{admin_id}")
    assert get_resp.status_code == 404

def test_delete_admin_not_found():
    response = client.delete("/admins/delete/999")
    assert response.status_code == 404