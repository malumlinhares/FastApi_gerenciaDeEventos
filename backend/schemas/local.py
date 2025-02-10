from pydantic import BaseModel
from typing import List, Optional

class LocalBase(BaseModel):
    cidade: str
    nome: str
    estado: Optional[str] = None  
    descricao: Optional[str] = None  

    class Config:
        from_attributes = True

class LocalCreate(LocalBase):  
    cidade: str
    nome: str
    estado: Optional[str] = None  
    descricao: Optional[str] = None  

    class Config:
        from_attributes = True

class LocalResponse(LocalCreate):  
    id: int
    cidade: str
    nome: str
    estado: Optional[str] = None  
    descricao: Optional[str] = None  

class LocalBulkCreate(BaseModel):  
    locais: List[LocalBase]
