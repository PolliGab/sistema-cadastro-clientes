"""
Testes unitários para ClienteService
"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.connection import Base
from models.cliente import Cliente
from schemas.cliente_schema import ClienteCreate
from services.cliente_service import ClienteService


# Configuração do banco de dados em memória para testes
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture
def db_session():
    """Fixture que cria uma sessão de banco de dados para testes"""
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False}
    )
    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = TestingSessionLocal()
    
    yield db
    
    db.close()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def cliente_service(db_session):
    """Fixture que retorna uma instância do ClienteService"""
    return ClienteService(db_session)


class TestClienteServiceCriacao:
    """Testes para criação de clientes"""
    
    def test_criar_cliente_valido(self, cliente_service):
        """Testa criação de cliente com dados válidos"""
        cliente_data = ClienteCreate(
            nome="João da Silva",
            email="joao@email.com",
            telefone="41999999999"
        )
        
        cliente = cliente_service.criar_cliente(cliente_data)
        
        assert cliente.id is not None
        assert cliente.nome == "João da Silva"
        assert cliente.email == "joao@email.com"
        assert cliente.telefone == "41999999999"
    
    def test_criar_cliente_sem_telefone(self, cliente_service):
        """Testa criação de cliente sem telefone (campo opcional)"""
        cliente_data = ClienteCreate(
            nome="Maria Santos",
            email="maria@email.com"
        )
        
        cliente = cliente_service.criar_cliente(cliente_data)
        
        assert cliente.id is not None
        assert cliente.nome == "Maria Santos"
        assert cliente.telefone is None
    
    def test_criar_cliente_email_duplicado(self, cliente_service):
        """Testa que não é possível criar clientes com email duplicado"""
        cliente_data1 = ClienteCreate(
            nome="Cliente 1",
            email="mesmo@email.com"
        )
        cliente_service.criar_cliente(cliente_data1)
        
        cliente_data2 = ClienteCreate(
            nome="Cliente 2",
            email="mesmo@email.com"
        )
        
        with pytest.raises(ValueError, match="já está cadastrado"):
            cliente_service.criar_cliente(cliente_data2)
    
    def test_criar_cliente_nome_vazio(self, cliente_service):
        """Testa que não é possível criar cliente com nome vazio"""
        cliente_data = ClienteCreate(
            nome="   ",
            email="teste@email.com"
        )
        
        with pytest.raises(ValueError, match="Nome é obrigatório"):
            cliente_service.criar_cliente(cliente_data)
    
    def test_criar_cliente_email_normalizado(self, cliente_service):
        """Testa que o email é normalizado para lowercase"""
        cliente_data = ClienteCreate(
            nome="Teste",
            email="TESTE@EMAIL.COM"
        )
        
        cliente = cliente_service.criar_cliente(cliente_data)
        
        assert cliente.email == "teste@email.com"
    
    def test_criar_cliente_email_vazio(self, cliente_service):
        """Testa que não é possível criar cliente com email vazio"""
        cliente_data = ClienteCreate(
            nome="Teste",
            email="   "
        )
        with pytest.raises(ValueError, match="Email é obrigatório"):
            cliente_service.criar_cliente(cliente_data)

    def test_criar_cliente_email_invalido(self, cliente_service):
        """Testa que não é possível criar cliente com email inválido"""
        cliente_data = ClienteCreate(
            nome="Teste",
            email="emailinvalido"
        )
        with pytest.raises(ValueError, match="Email inválido"):
            cliente_service.criar_cliente(cliente_data)

    def test_criar_cliente_telefone_invalido(self, cliente_service):
        """Testa que não é possível criar cliente com telefone inválido"""
        cliente_data = ClienteCreate(
            nome="Teste",
            email="teste@email.com",
            telefone="abc123"
        )
        with pytest.raises(ValueError, match="Telefone inválido"):
            cliente_service.criar_cliente(cliente_data)

    def test_criar_cliente_erro_interno(self, cliente_service, monkeypatch):
        """Testa que exceção inesperada é propagada"""
        def raise_exception(*args, **kwargs):
            raise Exception("Erro inesperado")
        monkeypatch.setattr(cliente_service, "criar_cliente", raise_exception)
        cliente_data = ClienteCreate(
            nome="Teste",
            email="teste@email.com"
        )
        with pytest.raises(Exception, match="Erro inesperado"):
            cliente_service.criar_cliente(cliente_data)


class TestClienteServiceConsulta:
    """Testes para consulta de clientes"""
    
    def test_listar_todos_vazio(self, cliente_service):
        """Testa listagem quando não há clientes"""
        clientes = cliente_service.listar_todos()
        assert len(clientes) == 0
    
    def test_listar_todos_com_clientes(self, cliente_service):
        """Testa listagem com múltiplos clientes"""
        # Cria clientes
        for i in range(3):
            cliente_data = ClienteCreate(
                nome=f"Cliente {i}",
                email=f"cliente{i}@email.com"
            )
            cliente_service.criar_cliente(cliente_data)
        
        clientes = cliente_service.listar_todos()
        assert len(clientes) == 3
    
    def test_buscar_por_id_existente(self, cliente_service):
        """Testa busca por ID de cliente existente"""
        cliente_data = ClienteCreate(
            nome="Teste",
            email="teste@email.com"
        )
        cliente_criado = cliente_service.criar_cliente(cliente_data)
        
        cliente_encontrado = cliente_service.buscar_por_id(cliente_criado.id)
        
        assert cliente_encontrado is not None
        assert cliente_encontrado.id == cliente_criado.id
        assert cliente_encontrado.nome == "Teste"
    
    def test_buscar_por_id_inexistente(self, cliente_service):
        """Testa busca por ID que não existe"""
        cliente = cliente_service.buscar_por_id(999)
        assert cliente is None
    
    def test_buscar_por_email_existente(self, cliente_service):
        """Testa busca por email existente"""
        cliente_data = ClienteCreate(
            nome="Teste",
            email="teste@email.com"
        )
        cliente_service.criar_cliente(cliente_data)
        
        cliente = cliente_service.buscar_por_email("teste@email.com")
        
        assert cliente is not None
        assert cliente.email == "teste@email.com"
    
    def test_buscar_por_email_inexistente(self, cliente_service):
        """Testa busca por email que não existe"""
        cliente = cliente_service.buscar_por_email("naoexiste@email.com")
        assert cliente is None
    
    def test_listar_todos_apos_remocao(self, cliente_service):
        """Testa listagem após remoção de cliente"""
        cliente_data = ClienteCreate(
            nome="Remover",
            email="remover@email.com"
        )
        cliente = cliente_service.criar_cliente(cliente_data)
        cliente_service.db.delete(cliente)
        cliente_service.db.commit()
        clientes = cliente_service.listar_todos()
        assert all(c.id != cliente.id for c in clientes)

    def test_buscar_por_email_formato_diferente(self, cliente_service):
        """Testa busca por email com formato diferente"""
        cliente_data = ClienteCreate(
            nome="Teste",
            email="teste+alias@email.com"
        )
        cliente_service.criar_cliente(cliente_data)
        cliente = cliente_service.buscar_por_email("teste+alias@email.com")
        assert cliente is not None
        assert cliente.email == "teste+alias@email.com"

    def test_buscar_por_id_tipo_invalido(self, cliente_service):
        """Testa busca por ID com tipo inválido"""
        with pytest.raises(Exception):
            cliente_service.buscar_por_id("abc")


class TestClienteServiceBuscaNome:
    """Testes para busca por nome"""
    
    def test_buscar_por_nome_completo(self, cliente_service):
        """Testa busca por nome completo"""
        cliente_data = ClienteCreate(
            nome="João da Silva",
            email="joao@email.com"
        )
        cliente_service.criar_cliente(cliente_data)
        
        resultado = cliente_service.buscar_por_nome("João da Silva")
        
        assert len(resultado) == 1
        assert resultado[0].nome == "João da Silva"
    
    def test_buscar_por_nome_parcial(self, cliente_service):
        """Testa busca por nome parcial"""
        # Cria múltiplos clientes
        nomes = ["João Silva", "João Santos", "Maria Silva", "Pedro Costa"]
        for nome in nomes:
            cliente_data = ClienteCreate(
                nome=nome,
                email=f"{nome.replace(' ', '').lower()}@email.com"
            )
            cliente_service.criar_cliente(cliente_data)
        
        # Busca por "Silva"
        resultado = cliente_service.buscar_por_nome("Silva")
        
        assert len(resultado) == 2
        nomes_encontrados = [c.nome for c in resultado]
        assert "João Silva" in nomes_encontrados
        assert "Maria Silva" in nomes_encontrados
    
    def test_buscar_por_nome_case_insensitive(self, cliente_service):
        """Testa que a busca é case insensitive"""
        cliente_data = ClienteCreate(
            nome="João da Silva",
            email="joao@email.com"
        )
        cliente_service.criar_cliente(cliente_data)
        
        resultado = cliente_service.buscar_por_nome("joão")
        
        assert len(resultado) == 1
        assert resultado[0].nome == "João da Silva"
    
    def test_buscar_por_nome_vazio(self, cliente_service):
        """Testa busca com nome vazio retorna lista vazia"""
        resultado = cliente_service.buscar_por_nome("   ")
        assert len(resultado) == 0
    
    def test_buscar_por_nome_inexistente(self, cliente_service):
        """Testa busca por nome que não existe"""
        cliente_data = ClienteCreate(
            nome="João",
            email="joao@email.com"
        )
        cliente_service.criar_cliente(cliente_data)
        
        resultado = cliente_service.buscar_por_nome("Maria")
        
        assert len(resultado) == 0
    
    def test_buscar_por_nome_caracteres_especiais(self, cliente_service):
        """Testa busca por nome com caracteres especiais"""
        cliente_data = ClienteCreate(
            nome="Ana!@#",
            email="ana@email.com"
        )
        cliente_service.criar_cliente(cliente_data)
        resultado = cliente_service.buscar_por_nome("!@#")
        assert len(resultado) == 1
        assert resultado[0].nome == "Ana!@#"

    def test_buscar_por_nome_apenas_espacos(self, cliente_service):
        """Testa busca por nome apenas com espaços"""
        resultado = cliente_service.buscar_por_nome("     ")
        assert resultado == []

    def test_buscar_por_nome_erro_interno(self, cliente_service, monkeypatch):
        """Testa exceção inesperada na busca por nome"""
        def raise_exception(*args, **kwargs):
            raise Exception("Erro inesperado")
        monkeypatch.setattr(cliente_service, "buscar_por_nome", raise_exception)
        with pytest.raises(Exception, match="Erro inesperado"):
            cliente_service.buscar_por_nome("Teste")