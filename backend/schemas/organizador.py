from pydantic import BaseModel
from typing import List, Optional

class OrganizadorBase(BaseModel):
    nome: str
    email: str 
    cnpj: str 
    telefone: Optional[str] = None  
    nome_contato: Optional[str] = None  

    class Config:
        from_attributes = True

class OrganizadorCreate(BaseModel):  
    nome: str
    email: str 
    cnpj: str 
    telefone: Optional[str] = None  
    nome_contato: Optional[str] = None  

    class Config:
        from_attributes = True

class OrganizadorResponse(OrganizadorCreate): 
    id: int
    nome: str
    email: str 
    cnpj: str 
    telefone: Optional[str] = None  
    nome_contato: Optional[str] = None  

class OrganizadorBulkCreate(BaseModel):  
    organizadores: List[OrganizadorBase] 
