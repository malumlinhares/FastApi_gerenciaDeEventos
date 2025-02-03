from pydantic import BaseModel

class PrivilegioVipBase(BaseModel):
    privilegio_id: int
    participante_id: int

    class Config:
        from_attributes = True

class PrivilegioVipCreate(PrivilegioVipBase):  # Para criação do privilégio VIP
    privilegio_id: int
    participante_id: int

    class Config:
        from_attributes = True

class PrivilegioVipResponse(PrivilegioVipBase):  # Para a resposta com ID
    id: int
