from pydantic import BaseModel

class PatrocinioBase(BaseModel):
    valor: float
    descricao: str 
    evento_id: int 
    patrocinador_id: int 

    class Config:
        from_attributes = True

class PatrocinioCreate(BaseModel):  # Para criação do Patrocinio
    valor: float
    descricao: str 
    evento_id: int 
    patrocinador_id: int 

    class Config:
        from_attributes = True

class PatrocinioResponse(PatrocinioCreate):  # Para a resposta com ID
    id: int
