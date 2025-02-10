from pydantic import BaseModel, field_validator, ConfigDict, ValidationInfo
from typing import Optional, List
from enum import Enum

class TipoParticipante(str, Enum):
    vip = "vip"
    padrao = "padrao"

class ParticipanteBase(BaseModel):
    nome: str
    email: str
    tipo: TipoParticipante 
    elegivel_upgrade: Optional[int] = None
    endereco_id: int
    anuidade: Optional[int] = None
    telefone: Optional[str] = None  
    responsavel: Optional[str] = None  

 
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

    model_config = ConfigDict(from_attributes=True)

class ParticipanteCreate(ParticipanteBase):  
    model_config = ConfigDict(from_attributes=True)

class ParticipanteResponse(ParticipanteCreate):  
    id: int
    nome: str
    email: str
    tipo: TipoParticipante  
    anuidade: Optional[int]  
    elegivel_upgrade: Optional[int]  
    endereco_id: int

class ParticipanteBulkCreate(BaseModel): 
    participantes: List[ParticipanteBase]  


class ParticipanteQueryParams(BaseModel):
    participante_id: int

