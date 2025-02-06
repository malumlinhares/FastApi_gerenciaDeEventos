from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from backend.models.privilegio import Privilegio
from backend.schemas.privilegio import PrivilegioCreate
from sqlalchemy import text

# async def create_privilegio(db: AsyncSession, privilegio: PrivilegioCreate):
#     db_privilegio = Privilegio(
#         nome=privilegio.nome,
#         descricao=privilegio.descricao
#     )
#     db.add(db_privilegio)
#     await db.commit()
#     await db.refresh(db_privilegio)
#     return db_privilegio


async def create_privilegio(db: AsyncSession, privilegio: PrivilegioCreate):
    query = text("""
        INSERT INTO privilegios ( nome, descricao)
        VALUES (:nome, :descricao)
        RETURNING id,  nome, descricao
    """)
    params = {
        "nome": privilegio.nome, 
        "descricao": privilegio.descricao
    }
    result = await db.execute(query, params)
    row = result.fetchone()
    await db.commit()
    return {
        "id":row.id,
        "nome": row.nome, 
        "descricao": row.descricao
    }

async def get_privilegio(db: AsyncSession, privilegio_id: int):
    result = await db.execute(select(Privilegio).filter(Privilegio.id == privilegio_id))
    privilegio = result.scalars().first()
    return privilegio

async def update_privilegio(db: AsyncSession, privilegio_id: int, privilegio: PrivilegioCreate):
    result = await db.execute(select(Privilegio).filter(Privilegio.id == privilegio_id))
    db_privilegio = result.scalars().first()
    if db_privilegio is None:
        return None
    db_privilegio.nome = privilegio.nome
    db_privilegio.descricao = privilegio.descricao
    await db.commit()
    await db.refresh(db_privilegio)
    return db_privilegio

async def delete_privilegio(db: AsyncSession, privilegio_id: int):
    result = await db.execute(select(Privilegio).filter(Privilegio.id == privilegio_id))
    db_privilegio = result.scalars().first()
    if db_privilegio is None:
        return None
    await db.delete(db_privilegio)
    await db.commit()
    return db_privilegio


async def bulk_create_privilegio(db: AsyncSession, privilegios: list[PrivilegioCreate]):
    db_privilegios = [Privilegio(**privilegio.model_dump()) for privilegio in privilegios]
    db.add_all(db_privilegios)
    await db.commit()
    # Atualiza os objetos para garantir dados consistentes
    for privilegio in db_privilegios:
        await db.refresh(privilegio)
    return db_privilegios



