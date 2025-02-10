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
    descricao: Optional[str] = None 
    limite_participantes: Optional[int] = None  

    class Config:
        from_attributes = True

class EventoBulkCreate(BaseModel): 
    eventos: List[EventoBase]  

class EventoCreate(EventoBase): 
    pass  

class EventoResponse(EventoBase):  
    pass
