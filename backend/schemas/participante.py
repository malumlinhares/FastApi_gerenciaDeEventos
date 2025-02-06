from pydantic import BaseModel, field_validator, ConfigDict, ValidationInfo
from typing import Optional
from enum import Enum
from typing import List

# Definição do Enum compatível com o banco de dados
class TipoParticipante(str, Enum):
    vip = "vip"
    padrao = "padrao"

class ParticipanteBase(BaseModel):
    nome: str
    email: str
    tipo: TipoParticipante  # Usa o Enum ao invés de str
    elegivel_upgrade: Optional[int] = None
    anuidade: Optional[int] = None

    # Validação para anuidade
    @field_validator('anuidade')
    def validate_anuidade(cls, v, values: ValidationInfo):
        if values.data.get('tipo') == TipoParticipante.vip and not v:
            raise ValueError("Anuidade é obrigatória para Participantes do tipo 'vip'")
        return v

    # Validação para elegivel_upgrade
    @field_validator('elegivel_upgrade')
    def validate_elegivel_upgrade(cls, v, values: ValidationInfo):
        if values.data.get('tipo') == TipoParticipante.padrao and not v:
            raise ValueError("Elegível para upgrade é obrigatório para Participantes do tipo 'padrao'")
        return v

    # Configuração do modelo (substitui a classe Config)
    model_config = ConfigDict(from_attributes=True)

class ParticipanteCreate(ParticipanteBase):  # Para criação do participante
    model_config = ConfigDict(from_attributes=True)

class ParticipanteResponse(ParticipanteCreate):  # Para a resposta com ID
    id: int
    nome: str
    email: str
    tipo: TipoParticipante  # Usa o Enum ao invés de str
    anuidade: int
    elegivel_upgrade: int




class ParticipanteBulkCreate(BaseModel):  # Para a criação em massa do Participante
    particpantes: List[ParticipanteBase]  


# Esquema para capturar o participante_id como um parâmetro de consulta
class ParticipanteQueryParams(BaseModel):
    participante_id: int

# Resolve a referência circular entre ParticipanteResponse e CertificadoResponse
from .certificado import CertificadoResponse
ParticipanteResponse.model_rebuild()