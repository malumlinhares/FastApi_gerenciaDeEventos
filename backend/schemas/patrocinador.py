from pydantic import BaseModel, field_validator, ConfigDict
from typing import Optional, List
from enum import Enum

class TipoPatrocinador(str, Enum):
    publico = "publico"
    privado = "privado"

class PatrocinadorBase(BaseModel):
    nome: str
    email: str
    tipo: TipoPatrocinador  
    orgao_responsavel: Optional[str] = None
    responsavel_comercial: Optional[str] = None
    telefone: Optional[str] = None  
    nome_responsavel: Optional[str] = None  

    @field_validator('orgao_responsavel')
    @classmethod
    def validate_orgao_responsavel(cls, v, values):
        tipo = values.data.get('tipo')  
        if tipo == TipoPatrocinador.privado and v is not None:
            raise ValueError("orgao_responsavel não pode ser preenchido para patrocinadores do tipo 'privado'")
        return v

    @field_validator('responsavel_comercial')
    @classmethod
    def validate_responsavel_comercial(cls, v, values):
        tipo = values.data.get('tipo')  
        if tipo == TipoPatrocinador.publico and v is not None:
            raise ValueError("responsavel_comercial não pode ser preenchido para patrocinadores do tipo 'publico'")
        return v

    model_config = ConfigDict(from_attributes=True)

class PatrocinadorCreate(PatrocinadorBase):  
    model_config = ConfigDict(from_attributes=True)

class PatrocinadorResponse(PatrocinadorCreate):  
    id: int

class PatrocinadorBulkCreate(BaseModel):  
    patrocinadores: List[PatrocinadorBase]
