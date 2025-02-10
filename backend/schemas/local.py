# from pydantic import BaseModel
# from typing import List

# class LocalBase(BaseModel):
#     cidade: str
#     capacidade: int 
#     nome: str 


#     class Config:
#         from_attributes = True

# class LocalCreate(BaseModel):  # Para criação do Local
#     cidade: str
#     capacidade: int 
#     nome: str 

#     class Config:
#         from_attributes = True# 

# class LocalResponse(LocalCreate):  # Para a resposta com ID
#     id: int
#     cidade: str
#     capacidade: int 
#     nome: str 

# class LocalBulkCreate(BaseModel):  # Para a criação em massa do Local
#     locais: List[LocalBase]  

from pydantic import BaseModel
from typing import List, Optional

class LocalBase(BaseModel):
    cidade: str
    nome: str
    estado: Optional[str] = None  # Campo opcional
    descricao: Optional[str] = None  # Campo opcional

    class Config:
        from_attributes = True

class LocalCreate(LocalBase):  # Para criação do Local
    cidade: str
    nome: str
    estado: Optional[str] = None  # Campo opcional
    descricao: Optional[str] = None  # Campo opcional

    class Config:
        from_attributes = True

class LocalResponse(LocalCreate):  # Para a resposta com ID
    id: int
    cidade: str
    nome: str
    estado: Optional[str] = None  # Campo opcional
    descricao: Optional[str] = None  # Campo opcional

class LocalBulkCreate(BaseModel):  # Para a criação em massa do Local
    locais: List[LocalBase]
