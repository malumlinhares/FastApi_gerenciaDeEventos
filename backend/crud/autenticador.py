from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from backend.models.autenticador import Autenticador
from backend.schemas.autenticador import AutenticadorCreate
from sqlalchemy import text

#usando a biblioteca
# async def create_autenticador(db: AsyncSession, autenticador: AutenticadorCreate):
#     db_autenticador = Autenticador(orgao=autenticador.orgao)
#     db.add(db_autenticador)
#     await db.commit()
#     await db.refresh(db_autenticador)
#     return db_autenticador

#usando sqlnativo:
async def create_autenticador(db: AsyncSession, autenticador: AutenticadorCreate):
    query = text("""
        INSERT INTO autenticadores (orgao)
        VALUES (:orgao)
        RETURNING id, orgao
    """)
    result = await db.execute(query, {"orgao": autenticador.orgao})
    row = result.fetchone()
    await db.commit()  
    return {"id": row.id, "orgao": row.orgao}


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


async def bulk_create_autenticador(db: AsyncSession, autenticadores: list[AutenticadorCreate]):
    db_autenticadores = [Autenticador(**autenticador.model_dump()) for autenticador in autenticadores]
    db.add_all(db_autenticadores)
    await db.commit()
    # Atualiza os objetos para garantir dados consistentes
    for autenticador in db_autenticadores:
        await db.refresh(autenticador)
    return db_autenticadores
