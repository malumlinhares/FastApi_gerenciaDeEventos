from pydantic import BaseModel
from typing import List, Optional
from datetime import date

class AutenticadorBase(BaseModel):
    orgao: str
    status: str

    class Config:
        from_attributes = True

class AutenticadorCreate(AutenticadorBase):  
    chave_autenticacao: str
    data_expiracao: Optional[date] = None  

class AutenticadorResponse(AutenticadorBase):  
    id: int
    chave_autenticacao: str
    data_expiracao: Optional[date] = None  

class AutenticadorBulkCreate(BaseModel):  
    autenticadores: List[AutenticadorCreate]
