from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.autenticador import Autenticador
from schemas.autenticador import AutenticadorCreate

async def create_autenticador(db: AsyncSession, autenticador: AutenticadorCreate):
    db_autenticador = Autenticador(orgao=autenticador.orgao)
    db.add(db_autenticador)
    await db.commit()
    await db.refresh(db_autenticador)
    return db_autenticador

async def get_autenticador(db: AsyncSession, autenticador_id: int):
    result = await db.execute(select(Autenticador).filter(Autenticador.id == autenticador_id))
    return result.scalars().first()

async def update_autenticador(db: AsyncSession, autenticador_id: int, autenticador: AutenticadorCreate):
    result = await db.execute(select(Autenticador).filter(Autenticador.id == autenticador_id))
    db_autenticador = result.scalars().first()
    if db_autenticador is None:
        return None
    db_autenticador.orgao = autenticador.orgao
    await db.commit()
    await db.refresh(db_autenticador)
    return db_autenticador

async def delete_autenticador(db: AsyncSession, autenticador_id: int):
    result = await db.execute(select(Autenticador).filter(Autenticador.id == autenticador_id))
    db_autenticador = result.scalars().first()
    if db_autenticador is None:
        return None
    await db.delete(db_autenticador)
    await db.commit()
    return db_autenticador
