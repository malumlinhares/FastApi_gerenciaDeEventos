from pydantic import BaseModel, field_validator, ConfigDict
from typing import Optional, List
from enum import Enum

# Definição do Enum compatível com o banco de dados
class TipoPatrocinador(str, Enum):
    publico = "publico"
    privado = "privado"

class PatrocinadorBase(BaseModel):
    nome: str
    email: str
    tipo: TipoPatrocinador  # Usa o Enum ao invés de str
    orgao_responsavel: Optional[str] = None
    responsavel_comercial: Optional[str] = None

    # Validação para orgao_responsavel
    @field_validator('orgao_responsavel')
    def validate_orgao_responsavel(cls, v, values):
        if values.data.get('tipo') == TipoPatrocinador.publico and not v:
            raise ValueError("orgao_responsavel é obrigatório para patrocinadores do tipo 'publico'")
        return v

    # Validação para responsavel_comercial
    @field_validator('responsavel_comercial')
    def validate_responsavel_comercial(cls, v, values):
        if values.data.get('tipo') == TipoPatrocinador.privado and not v:
            raise ValueError("responsavel_comercial é obrigatório para patrocinadores do tipo 'privado'")
        return v

    # Configuração do modelo (substitui a classe Config)
    model_config = ConfigDict(from_attributes=True)

class PatrocinadorCreate(PatrocinadorBase):  # Para criação do patrocinador
    model_config = ConfigDict(from_attributes=True)

class PatrocinadorResponse(PatrocinadorCreate):  # Para a resposta com ID
    id: int



class PatrocinadorBulkCreate(BaseModel):  # Para a criação em massa do Patrocinador
    patrocinadores: List[PatrocinadorBase]  