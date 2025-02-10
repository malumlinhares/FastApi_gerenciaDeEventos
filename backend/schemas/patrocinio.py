from pydantic import BaseModel
from typing import List, Optional

class PatrocinioBase(BaseModel):
    valor: float
    descricao: str 
    evento_id: int 
    patrocinador_id: int 
    status: Optional[str] = None  
    observacao: Optional[str] = None  

    class Config:
        from_attributes = True

class PatrocinioCreate(PatrocinioBase):  
    pass

class PatrocinioResponse(PatrocinioCreate): 
    id: int

class PatrocinioBulkCreate(BaseModel): 
    patrocinios: List[PatrocinioBase]
