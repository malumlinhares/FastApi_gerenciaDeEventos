from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.organizador import Organizador
from schemas.organizador import OrganizadorCreate

async def create_organizador(db: AsyncSession, organizador: OrganizadorCreate):
    db_organizador = Organizador(
        nome=organizador.nome,  # Preencher com os dados recebidos
        email = organizador.email, 
        cnpj = organizador.cnpj

    )
    db.add(db_organizador)
    await db.commit()
    await db.refresh(db_organizador)
    return db_organizador  # Retorne o objeto organizador, FastAPI cuidará da conversão

async def get_organizador(db: AsyncSession, organizador_id: int):
    result = await db.execute(
        select(Organizador).filter(Organizador.id == organizador_id)
    )
    organizador = result.scalars().first()
    return organizador 


async def update_organizador(db: AsyncSession, organizador_id: int, organizador: OrganizadorCreate):
    result = await db.execute(
        select(Organizador).filter(Organizador.id == organizador_id)
    )
    db_organizador = result.scalars().first()
    if db_organizador is None:
        return None
    db_organizador.nome = organizador.nome
    db_organizador.email = organizador.email
    db_organizador.cnpj = organizador.cnpj

    
    await db.commit()
    await db.refresh(db_organizador)
    return db_organizador

async def delete_organizador(db:AsyncSession, organizador_id: int):
    result = await db.execute(
        select(Organizador).filter(Organizador.id==organizador_id)
    )
    db_organizador = result.scalars().first()
    if db_organizador is None:
        return None
    await db.delete(db_organizador)
    await db.commit()
    return db_organizador
