from pydantic import BaseModel

class LocalBase(BaseModel):
    cidade: str
    capacidade: int 
    nome: str 
    evento_id: int 


    class Config:
        from_attributes = True

class LocalCreate(BaseModel):  # Para criação do Local
    cidade: str
    capacidade: int 
    nome: str 
    evento_id: int 

    class Config:
        from_attributes = True# 

class LocalResponse(LocalCreate):  # Para a resposta com ID
    id: int
