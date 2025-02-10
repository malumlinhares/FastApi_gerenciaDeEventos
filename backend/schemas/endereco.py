from pydantic import BaseModel
from typing import List, Optional

class EnderecoBase(BaseModel):
    rua: str
    cep: str
    numero: int
    complemento: Optional[str] = None  
    ponto_de_referencia: Optional[str] = None  

    class Config:
        from_attributes = True

class EnderecoCreate(EnderecoBase):  
    pass  

class EnderecoResponse(EnderecoBase):  
    id: int

class EnderecoBulkCreate(BaseModel):  
    enderecos: List[EnderecoBase]  
