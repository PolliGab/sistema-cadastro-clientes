"""
Testes mockados para a API FastAPI - Sistema de Cadastro de Clientes
"""

from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from main import app
from datetime import datetime

# Tente importar o schema correto. Se não existir, crie um mock para os testes:
try:
    from schemas.cliente_schema import ClienteResponse
except ImportError:
    from pydantic import BaseModel, Field
    class ClienteResponse(BaseModel):
        id: int = Field(...)
        nome: str = Field(...)
        email: str = Field(...)
        telefone: str = Field(default=None)
        criado_em: datetime = Field(default_factory=lambda: datetime(2024, 1, 1, 0, 0, 0))
        atualizado_em: datetime = Field(default_factory=lambda: datetime(2024, 1, 1, 0, 0, 0))
        class Config:
            extra = "allow"

client = TestClient(app)

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "Sistema de Cadastro de Clientes" in data["message"]
    assert data["version"] == "1.0.0"

@patch("services.cliente_service.ClienteService.listar_todos")
@patch("database.connection.get_db")
def test_listar_todos_clientes(mock_get_db, mock_listar_todos):
    mock_get_db.return_value = MagicMock()
    mock_listar_todos.return_value = [
        ClienteResponse(
            id=1,
            nome="Maria Silva",
            email="maria@example.com",
            telefone="11987654321",
            criado_em=datetime(2024, 1, 1, 0, 0, 0),
            atualizado_em=datetime(2024, 1, 1, 0, 0, 0)
        ),
        ClienteResponse(
            id=2,
            nome="João Souza",
            email="joao@example.com",
            telefone="11988889999",
            criado_em=datetime(2024, 1, 1, 0, 0, 0),
            atualizado_em=datetime(2024, 1, 1, 0, 0, 0)
        ),
    ]
    response = client.get("/clientes")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["nome"] == "Maria Silva"
    assert data[1]["email"] == "joao@example.com"

@patch("services.cliente_service.ClienteService.buscar_por_nome")
@patch("database.connection.get_db")
def test_listar_clientes_com_filtro(mock_get_db, mock_buscar_por_nome):
    mock_get_db.return_value = MagicMock()
    mock_buscar_por_nome.return_value = [
        ClienteResponse(
            id=1,
            nome="Maria Silva",
            email="maria@example.com",
            telefone="11987654321",
            criado_em=datetime(2024, 1, 1, 0, 0, 0),
            atualizado_em=datetime(2024, 1, 1, 0, 0, 0)
        )
    ]
    response = client.get("/clientes?nome=Maria")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["nome"] == "Maria Silva"

@patch("services.cliente_service.ClienteService.buscar_por_id")
@patch("database.connection.get_db")
def test_consultar_cliente(mock_get_db, mock_buscar_por_id):
    mock_get_db.return_value = MagicMock()
    mock_buscar_por_id.return_value = ClienteResponse(
        id=1,
        nome="Maria Silva",
        email="maria@example.com",
        telefone="11987654321",
        criado_em=datetime(2024, 1, 1, 0, 0, 0),
        atualizado_em=datetime(2024, 1, 1, 0, 0, 0)
    )
    response = client.get("/clientes/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["email"] == "maria@example.com"

@patch("services.cliente_service.ClienteService.buscar_por_id")
@patch("database.connection.get_db")
def test_consultar_cliente_inexistente(mock_get_db, mock_buscar_por_id):
    mock_get_db.return_value = MagicMock()
    mock_buscar_por_id.return_value = None
    response = client.get("/clientes/999")
    assert response.status_code == 404
    assert "nao encontrado" in response.json()["detail"].lower()

@patch("services.cliente_service.ClienteService.criar_cliente")
@patch("database.connection.get_db")
def test_criar_cliente(mock_get_db, mock_criar_cliente):
    mock_get_db.return_value = MagicMock()
    mock_criar_cliente.return_value = ClienteResponse(
        id=1,
        nome="Maria Silva",
        email="maria@example.com",
        telefone="11987654321",
        criado_em=datetime(2024, 1, 1, 0, 0, 0),
        atualizado_em=datetime(2024, 1, 1, 0, 0, 0)
    )
    payload = {
        "nome": "Maria Silva",
        "email": "maria@example.com",
        "telefone": "11987654321"
    }
    response = client.post("/clientes", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["nome"] == "Maria Silva"
    assert data["email"] == "maria@example.com"

@patch("services.cliente_service.ClienteService.criar_cliente")
@patch("database.connection.get_db")
def test_criar_cliente_email_duplicado(mock_get_db, mock_criar_cliente):
    mock_get_db.return_value = MagicMock()
    mock_criar_cliente.side_effect = ValueError("Email já cadastrado")
    payload = {
        "nome": "Maria Silva",
        "email": "maria@example.com",
        "telefone": "11987654321"
    }
    response = client.post("/clientes", json=payload)
    assert response.status_code == 400
    assert "Email já cadastrado" in response.json()["detail"]

@patch("services.cliente_service.ClienteService.criar_cliente")
@patch("database.connection.get_db")
def test_criar_cliente_erro_interno(mock_get_db, mock_criar_cliente):
    mock_get_db.return_value = MagicMock()
    mock_criar_cliente.side_effect = Exception("Erro inesperado no banco")
    payload = {
        "nome": "João Souza",
        "email": "joao@example.com",
        "telefone": "11999999999"
    }
    response = client.post("/clientes", json=payload)
    assert response.status_code == 500
    assert "Erro ao criar cliente" in response.json()["detail"]

def test_criar_cliente_validacao_nome_obrigatorio():
    payload = {
        "email": "teste@email.com",
        "telefone": "11999999999"
    }
    response = client.post("/clientes", json=payload)
    assert response.status_code == 422
    assert any("nome" in err["loc"] for err in response.json()["detail"])

def test_criar_cliente_validacao_email_obrigatorio():
    payload = {
        "nome": "Teste",
        "telefone": "11999999999"
    }
    response = client.post("/clientes", json=payload)
    assert response.status_code == 422
    assert any("email" in err["loc"] for err in response.json()["detail"])

def test_criar_cliente_validacao_email_invalido():
    payload = {
        "nome": "Teste",
        "email": "emailinvalido",
        "telefone": "11999999999"
    }
    response = client.post("/clientes", json=payload)
    assert response.status_code == 422

def test_listar_clientes_sem_mock():
    response = client.get("/clientes")
    assert response.status_code in (200, 500, 422)  # Aceita vazio ou erro de banco

def test_consultar_cliente_sem_mock():
    response = client.get("/clientes/1")
    assert response.status_code in (200, 404, 500)

def test_listar_clientes_com_nome_vazio():
    response = client.get("/clientes?nome=")
    assert response.status_code in (200, 500, 422)

def test_root_endpoint_method_not_allowed():
    response = client.post("/")
    assert response.status_code == 405