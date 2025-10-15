"""
Service Layer - Logica de negocio para operacoes com Cliente
"""
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List, Optional

from models.cliente import Cliente
from schemas.cliente_schema import ClienteCreate


class ClienteService:
    """
    Classe responsavel pela logica de negocio relacionada a clientes
    """
    
    def __init__(self, db: Session):
        self.db = db

    def criar_cliente(self, cliente_data: ClienteCreate) -> Cliente:
        """
        Cria um novo cliente no banco de dados
        """
        if not cliente_data.nome or not cliente_data.nome.strip():
            raise ValueError("Nome e obrigatorio e nao pode ser vazio")
        
        if not cliente_data.email or not cliente_data.email.strip():
            raise ValueError("Email e obrigatorio e nao pode ser vazio")
        
        cliente_existente = self.db.query(Cliente).filter(
            Cliente.email == cliente_data.email
        ).first()
        
        if cliente_existente:
            raise ValueError(f"Email {cliente_data.email} ja esta cadastrado")
        
        novo_cliente = Cliente(
            nome=cliente_data.nome.strip(),
            email=cliente_data.email.strip().lower(),
            telefone=cliente_data.telefone.strip() if cliente_data.telefone else None
        )
        
        try:
            self.db.add(novo_cliente)
            self.db.commit()
            self.db.refresh(novo_cliente)
            return novo_cliente
        except IntegrityError as e:
            self.db.rollback()
            raise ValueError(f"Erro ao criar cliente: {str(e)}")

    def listar_todos(self) -> List[Cliente]:
        """Lista todos os clientes cadastrados"""
        return self.db.query(Cliente).order_by(Cliente.nome).all()

    def buscar_por_id(self, cliente_id: int) -> Optional[Cliente]:
        """Busca um cliente especifico pelo ID"""
        return self.db.query(Cliente).filter(Cliente.id == cliente_id).first()

    def buscar_por_nome(self, nome: str) -> List[Cliente]:
        """Busca clientes cujo nome contenha o valor informado"""
        if not nome or not nome.strip():
            return []
        filtro = f"%{nome.strip()}%"
        return self.db.query(Cliente).filter(
            Cliente.nome.ilike(filtro)
        ).order_by(Cliente.nome).all()
