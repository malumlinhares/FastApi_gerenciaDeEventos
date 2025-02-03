from pydantic import BaseModel
from datetime import date
from typing import List

class EventoBase(BaseModel):
    nome: str
    categoria: str 
    data: date
    numerohoras: int
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
    organizador_id: int 

    class Config:
        from_attributes = True# 

class EventoResponse(EventoCreate):  # Para a resposta com ID
    id: int

# from pydantic import BaseModel
# from datetime import date
# from typing import List, Optional

# class EventoBase(BaseModel):
#     nome: str
#     categoria: str 
#     data: date
#     numerohoras: int
#     organizador_id: int 

# class EventoCreate(EventoBase):
#     class Config:
#         from_attributes = True

# class EventoUpdate(BaseModel):
#     nome: Optional[str] = None
#     categoria: Optional[str] = None
#     data: Optional[date] = None
#     numerohoras: Optional[int] = None
#     organizador_id: Optional[int] = None

# # Schema específico para bulk update (todos campos obrigatórios + id)
# class EventoBulkUpdate(EventoBase):  # Herda diretamente de EventoBase
#     id: int  # Campo adicional obrigatório

# class EventoResponse(EventoBase):
#     id: int

# class BulkDeleteRequest(BaseModel):
#     ids: List[int]