from pydantic import BaseModel

class OrganizadorBase(BaseModel):
    nome: str
    email: str 
    cnpj: str 

    class Config:
        from_attributes = True

class OrganizadorCreate(BaseModel):  # Para criação do Organizador
    nome: str
    email: str 
    cnpj: str 

    class Config:
        from_attributes = True

class OrganizadorResponse(OrganizadorCreate):  # Para a resposta com ID
    id: int
