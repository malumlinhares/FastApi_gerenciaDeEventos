from pydantic import BaseModel
from typing import List, Optional
from datetime import date

class InscricaoBase(BaseModel):
    status: str = 'Pendente'  
    forma_pagamento: str
    valor: int
    participante_id: int
    data_pagamento: Optional[date] = None  
    observacao: Optional[str] = None  

    class Config:
        from_attributes = True

class InscricaoCreate(InscricaoBase): 
    status: str
    forma_pagamento: str
    valor: int
    participante_id: int
    data_pagamento: Optional[date] = None  
    observacao: Optional[str] = None  

    class Config:
        from_attributes = True

class InscricaoResponse(InscricaoBase):  
    numero_inscricao: int
    status: str
    forma_pagamento: str
    valor: int
    participante_id: int
    data_pagamento: Optional[date] = None 
    observacao: Optional[str] = None  

class InscricaoBulkCreate(BaseModel):  
    inscricoes: List[InscricaoBase]  
