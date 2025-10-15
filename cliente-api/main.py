"""
Sistema de Cadastro de Clientes - API REST
Desenvolvido com FastAPI e PostgreSQL
"""
from fastapi import FastAPI, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import uvicorn

from models.cliente import Cliente
from schemas.cliente_schema import ClienteCreate, ClienteResponse
from database.connection import get_db, init_db
from services.cliente_service import ClienteService

app = FastAPI(
    title="Sistema de Cadastro de Clientes",
    description="API para gerenciamento de clientes",
    version="1.0.0"
)


@app.on_event("startup")
def startup_event():
    """Inicializa o banco de dados ao iniciar a aplicacao"""
    init_db()


@app.get("/")
def root():
    """Endpoint raiz - health check"""
    return {
        "message": "Sistema de Cadastro de Clientes - API Online",
        "version": "1.0.0"
    }


@app.post("/clientes", response_model=ClienteResponse, status_code=201)
def criar_cliente(
    cliente: ClienteCreate,
    db: Session = Depends(get_db)
):
    """
    Cadastra um novo cliente no sistema
    
    - **nome**: Nome completo do cliente (obrigatorio)
    - **email**: Email valido (obrigatorio)
    - **telefone**: Telefone de contato (opcional)
    """
    service = ClienteService(db)
    
    try:
        novo_cliente = service.criar_cliente(cliente)
        return novo_cliente
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar cliente: {str(e)}")


@app.get("/clientes", response_model=List[ClienteResponse])
def listar_clientes(
    nome: Optional[str] = Query(None, description="Filtrar clientes por nome"),
    db: Session = Depends(get_db)
):
    """
    Lista todos os clientes cadastrados
    
    - **nome**: Parametro opcional para buscar clientes por nome (busca parcial)
    """
    service = ClienteService(db)
    
    if nome:
        clientes = service.buscar_por_nome(nome)
    else:
        clientes = service.listar_todos()
    
    return clientes


@app.get("/clientes/{id}", response_model=ClienteResponse)
def consultar_cliente(
    id: int,
    db: Session = Depends(get_db)
):
    """
    Consulta um cliente especifico pelo ID
    
    - **id**: ID do cliente a ser consultado
    """
    service = ClienteService(db)
    cliente = service.buscar_por_id(id)
    
    if not cliente:
        raise HTTPException(status_code=404, detail=f"Cliente com ID {id} nao encontrado")
    
    return cliente


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
