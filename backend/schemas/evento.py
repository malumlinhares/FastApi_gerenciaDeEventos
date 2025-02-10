# from pydantic import BaseModel
# from datetime import date
# from typing import List

# class EventoBase(BaseModel):
#     nome: str
#     categoria: str 
#     data: date
#     numerohoras: int
#     local_id: int 
#     organizador_id: int 

#     class Config:
#         from_attributes = True

# class EventoBulkCreate(BaseModel):  # Para a criação em massa do Evento
#     eventos: List[EventoBase]  

# class EventoCreate(BaseModel):  # Para criação do Evento
#     nome: str
#     categoria: str 
#     data: date
#     numerohoras: int
#     local_id: int
#     organizador_id: int 

#     class Config:
#         from_attributes = True# 

# class EventoResponse(EventoCreate):  # Para a resposta com ID
#     id: int
#     nome: str
#     categoria: str
#     data: date
#     numerohoras: int
#     local_id: int
#     organizador_id: int

from pydantic import BaseModel
from datetime import date
from typing import List, Optional

class EventoBase(BaseModel):
    nome: str
    categoria: str 
    data: date
    numerohoras: int
    local_id: int 
    organizador_id: int 
    descricao: Optional[str] = None  # Campo opcional
    limite_participantes: Optional[int] = None  # Campo opcional

    class Config:
        from_attributes = True

class EventoBulkCreate(BaseModel):  # Para a criação em massa do Evento
    eventos: List[EventoBase]  

class EventoCreate(EventoBase):  # Para criação do Evento
    pass  # Herdando tudo de EventoBase, sem precisar repetir os campos

class EventoResponse(EventoBase):  # Para a resposta com ID
    id: int
