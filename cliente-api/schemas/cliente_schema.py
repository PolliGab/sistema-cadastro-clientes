"""
Schemas Pydantic para validacao e serializacao de dados
"""
from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
from datetime import datetime


class ClienteCreate(BaseModel):
    """Schema para criacao de cliente"""
    nome: str = Field(..., min_length=1, max_length=255, description="Nome do cliente")
    email: EmailStr = Field(..., description="Email valido do cliente")
    telefone: Optional[str] = Field(None, max_length=20, description="Telefone do cliente")

    @field_validator('nome')
    @classmethod
    def validar_nome(cls, v: str) -> str:
        """Valida se o nome nao e vazio apos remover espacos"""
        if not v or not v.strip():
            raise ValueError('Nome nao pode ser vazio')
        return v.strip()

    @field_validator('telefone')
    @classmethod
    def validar_telefone(cls, v: Optional[str]) -> Optional[str]:
        """Valida e formata o telefone"""
        if v:
            v = v.strip()
            if not v:
                return None
        return v


class ClienteResponse(BaseModel):
    """Schema para resposta de cliente"""
    id: int
    nome: str
    email: str
    telefone: Optional[str]
    criado_em: datetime
    atualizado_em: Optional[datetime]

    model_config = {"from_attributes": True}
