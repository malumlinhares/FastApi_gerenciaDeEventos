from pydantic import BaseModel
from typing import List

class LocalBase(BaseModel):
    cidade: str
    capacidade: int 
    nome: str 


    class Config:
        from_attributes = True

class LocalCreate(BaseModel):  # Para criação do Local
    cidade: str
    capacidade: int 
    nome: str 

    class Config:
        from_attributes = True# 

class LocalResponse(LocalCreate):  # Para a resposta com ID
    id: int
    cidade: str
    capacidade: int 
    nome: str 

class LocalBulkCreate(BaseModel):  # Para a criação em massa do Local
    locais: List[LocalBase]  