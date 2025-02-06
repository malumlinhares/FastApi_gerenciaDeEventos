from pydantic import BaseModel
from datetime import date
from typing import List

class EventoBase(BaseModel):
    nome: str
    categoria: str 
    data: date
    numerohoras: int
    local_id: int 
    organizador_id: int 

    class Config:
        from_attributes = True

class EventoBulkCreate(BaseModel):  # Para a criação em massa do Evento
    eventos: List[EventoBase]  

class EventoCreate(BaseModel):  # Para criação do Evento
    nome: str
    categoria: str 
    data: date
    numerohoras: int
    local_id: int
    organizador_id: int 

    class Config:
        from_attributes = True# 

class EventoResponse(EventoCreate):  # Para a resposta com ID
    id: int
    nome: str
    categoria: str
    data: date
    numerohoras: int
    local_id: int
    organizador_id: int
