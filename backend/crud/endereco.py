from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.endereco import Endereco
from schemas.endereco import EnderecoCreate

async def create_endereco(db: AsyncSession, endereco: EnderecoCreate):
    db_endereco = Endereco(
        rua=endereco.rua,
        cep=endereco.cep,
        numero=endereco.numero,
        participante_id=endereco.participante_id
    )
    db.add(db_endereco)
    await db.commit()
    await db.refresh(db_endereco)
    return db_endereco

async def get_endereco(db: AsyncSession, endereco_id: int):
    result = await db.execute(select(Endereco).filter(Endereco.id == endereco_id))
    endereco = result.scalars().first()
    return endereco

async def update_endereco(db: AsyncSession, endereco_id: int, endereco: EnderecoCreate):
    result = await db.execute(select(Endereco).filter(Endereco.id == endereco_id))
    db_endereco = result.scalars().first()
    if db_endereco is None:
        return None
    db_endereco.rua = endereco.rua
    db_endereco.cep = endereco.cep
    db_endereco.numero = endereco.numero
    db_endereco.participante_id = endereco.participante_id
    await db.commit()
    await db.refresh(db_endereco)
    return db_endereco

async def delete_endereco(db: AsyncSession, endereco_id: int):
    result = await db.execute(select(Endereco).filter(Endereco.id == endereco_id))
    db_endereco = result.scalars().first()
    if db_endereco is None:
        return None
    await db.delete(db_endereco)
    await db.commit()
    return db_endereco
