from pydantic import BaseModel
from datetime import date

class EventoBase(BaseModel):
    nome: str
    categoria: str 
    data: date
    numerohoras: int
    organizador_id: int 

    class Config:
        from_attributes = True

class EventoCreate(BaseModel):  # Para criação do Evento
    nome: str
    categoria: str 
    data: date
    numerohoras: int
    organizador_id: int 

    class Config:
        from_attributes = True# 

class EventoResponse(EventoCreate):  # Para a resposta com ID
    id: int
