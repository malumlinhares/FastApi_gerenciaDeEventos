# from pydantic import BaseModel
# from typing import List

# class OrganizadorBase(BaseModel):
#     nome: str
#     email: str 
#     cnpj: str 

#     class Config:
#         from_attributes = True

# class OrganizadorCreate(BaseModel):  # Para criação do Organizador
#     nome: str
#     email: str 
#     cnpj: str 

#     class Config:
#         from_attributes = True

# class OrganizadorResponse(OrganizadorCreate):  # Para a resposta com ID
#     id: int
#     nome: str
#     email: str 
#     cnpj: str 

# class OrganizadorBulkCreate(BaseModel):  # Para a criação em massa do Organizador
#     organizadores: List[OrganizadorBase]  

from pydantic import BaseModel
from typing import List, Optional

class OrganizadorBase(BaseModel):
    nome: str
    email: str 
    cnpj: str 
    telefone: Optional[str] = None  # Campo opcional
    nome_contato: Optional[str] = None  # Campo opcional

    class Config:
        from_attributes = True

class OrganizadorCreate(BaseModel):  # Para criação do Organizador
    nome: str
    email: str 
    cnpj: str 
    telefone: Optional[str] = None  # Campo opcional
    nome_contato: Optional[str] = None  # Campo opcional

    class Config:
        from_attributes = True

class OrganizadorResponse(OrganizadorCreate):  # Para a resposta com ID
    id: int
    nome: str
    email: str 
    cnpj: str 
    telefone: Optional[str] = None  # Campo opcional
    nome_contato: Optional[str] = None  # Campo opcional

class OrganizadorBulkCreate(BaseModel):  # Para a criação em massa do Organizador
    organizadores: List[OrganizadorBase] 
