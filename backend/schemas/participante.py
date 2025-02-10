# from pydantic import BaseModel, field_validator, ConfigDict, ValidationInfo
# from typing import Optional
# from enum import Enum
# from typing import List

# # Definição do Enum compatível com o banco de dados
# class TipoParticipante(str, Enum):
#     vip = "vip"
#     padrao = "padrao"

# class ParticipanteBase(BaseModel):
#     nome: str
#     email: str
#     tipo: TipoParticipante  # Usa o Enum ao invés de str
#     elegivel_upgrade: Optional[int] = None
#     anuidade: Optional[int] = None

#     # Validação para anuidade
#     @field_validator('anuidade')
#     def validate_anuidade(cls, v, values: ValidationInfo):
#         if values.data.get('tipo') == TipoParticipante.vip and not v:
#             raise ValueError("Anuidade é obrigatória para Participantes do tipo 'vip'")
#         return v

#     # Validação para elegivel_upgrade
#     @field_validator('elegivel_upgrade')
#     def validate_elegivel_upgrade(cls, v, values: ValidationInfo):
#         if values.data.get('tipo') == TipoParticipante.padrao and not v:
#             raise ValueError("Elegível para upgrade é obrigatório para Participantes do tipo 'padrao'")
#         return v

#     # Configuração do modelo (substitui a classe Config)
#     model_config = ConfigDict(from_attributes=True)

# class ParticipanteCreate(ParticipanteBase):  # Para criação do participante
#     model_config = ConfigDict(from_attributes=True)

# class ParticipanteResponse(ParticipanteCreate):  # Para a resposta com ID
#     id: int
#     nome: str
#     email: str
#     tipo: TipoParticipante  # Usa o Enum ao invés de str
#     anuidade: int
#     elegivel_upgrade: int




# class ParticipanteBulkCreate(BaseModel):  # Para a criação em massa do Participante
#     particpantes: List[ParticipanteBase]  


# # Esquema para capturar o participante_id como um parâmetro de consulta
# class ParticipanteQueryParams(BaseModel):
#     participante_id: int

# # Resolve a referência circular entre ParticipanteResponse e CertificadoResponse
# from .certificado import CertificadoResponse
# ParticipanteResponse.model_rebuild()

from pydantic import BaseModel, field_validator, ConfigDict, ValidationInfo
from typing import Optional, List
from enum import Enum

# Definição do Enum compatível com o banco de dados
class TipoParticipante(str, Enum):
    vip = "vip"
    padrao = "padrao"

class ParticipanteBase(BaseModel):
    nome: str
    email: str
    tipo: TipoParticipante  # Usa o Enum ao invés de str
    elegivel_upgrade: Optional[int] = None
    endereco_id: int
    anuidade: Optional[int] = None
    telefone: Optional[str] = None  # Novo campo opcional
    responsavel: Optional[str] = None  # Novo campo opcional

    # Validação para anuidade
    @field_validator('anuidade')
    def validate_anuidade(cls, v, values: ValidationInfo):
        tipo = values.data.get('tipo')
        if tipo == TipoParticipante.vip:
            if not v or v <= 0:
                raise ValueError("Anuidade deve ser maior que zero para participantes 'vip'")
        elif tipo == TipoParticipante.padrao:
            if v != 0:
                raise ValueError("Anuidade deve ser zero para participantes 'padrao'")
        return v

    # Validação para elegivel_upgrade
    @field_validator('elegivel_upgrade')
    def validate_elegivel_upgrade(cls, v, values: ValidationInfo):
        tipo = values.data.get('tipo')
        if tipo == TipoParticipante.padrao:
            if v != 1:
                raise ValueError("Elegível para upgrade deve ser 1 para participantes 'padrao'")
        elif tipo == TipoParticipante.vip:
            if v != 0:
                raise ValueError("Elegível para upgrade deve ser 0 para participantes 'vip'")
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
    anuidade: Optional[int]  # Pode ser nulo para participantes que não são 'vip'
    elegivel_upgrade: Optional[int]  # Pode ser nulo para participantes que não são 'padrao'
    endereco_id: int

class ParticipanteBulkCreate(BaseModel):  # Para a criação em massa do Participante
    particpantes: List[ParticipanteBase]  

# Esquema para capturar o participante_id como um parâmetro de consulta
class ParticipanteQueryParams(BaseModel):
    participante_id: int

# Resolve a referência circular entre ParticipanteResponse e CertificadoResponse
from .certificado import CertificadoResponse
ParticipanteResponse.model_rebuild()
