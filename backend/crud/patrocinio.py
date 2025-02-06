from sqlalchemy.ext.asyncio import AsyncSession
from backend.models.patrocinio import Patrocinio
from backend.schemas.patrocinio import PatrocinioCreate
from sqlalchemy.future import select
from sqlalchemy import text
from sqlalchemy import text

# async def create_patrocinio(db: AsyncSession, patrocinio: PatrocinioCreate):
#     db_patrocinio = Patrocinio(
#         valor=patrocinio.valor, descricao = patrocinio.descricao, 
#         patrocinador_id=patrocinio.patrocinador_id, 
#         evento_id=patrocinio.evento_id)
#     db.add(db_patrocinio)
#     await db.commit()
#     await db.refresh(db_patrocinio)
#     return db_patrocinio


async def create_patrocinio(db: AsyncSession, patrocinio: PatrocinioCreate):
    query = text("""
        INSERT INTO patrocinios (valor, descricao, evento_id, patrocinador_id)
        VALUES (:valor, :descricao, :evento_id, :patrocinador_id)
        RETURNING id, valor, descricao, evento_id, patrocinador_id
    """)
    params = {
        "valor": patrocinio.valor,
        "descricao": patrocinio.descricao,
        "evento_id": patrocinio.evento_id, 
        "patrocinador_id": patrocinio.patrocinador_id
    }
    result = await db.execute(query, params)
    row = result.fetchone()
    await db.commit()
    return {
        "id": row.id,
        "valor": row.valor,
        "descricao": row.descricao,
        "evento_id": row.evento_id, 
        "patrocinador_id": row.patrocinador_id
    }



async def get_patrocinio(db: AsyncSession, patrocinio_id: int):
    # Aqui você faz a consulta para buscar o patrocinio
    result = await db.execute(
        select(Patrocinio).filter(Patrocinio.id == patrocinio_id)
    )
    patrocinio = result.scalars().first()
    return patrocinio

async def update_patrocinio(db: AsyncSession, patrocinio_id: int, patrocinio: PatrocinioCreate):
    result = await db.execute(
        select(Patrocinio).filter(Patrocinio.id == patrocinio_id)
    )
    db_patrocinio = result.scalars().first()
    if db_patrocinio is None:
        return None
    
    db_patrocinio.valor = patrocinio.valor
    db_patrocinio.descricao = patrocinio.descricao
    db_patrocinio.evento_id = patrocinio.evento_id
    db_patrocinio.patrocinador_id = patrocinio.patrocinador_id

    await db.commit()
    await db.refresh(db_patrocinio)
    return db_patrocinio

async def delete_patrocinio(db:AsyncSession, patrocinio_id: int):
    result = await db.execute(
        select(Patrocinio).filter(Patrocinio.id==patrocinio_id)
    )
    db_patrocinio = result.scalars().first()
    if db_patrocinio is None:
        return None
    await db.delete(db_patrocinio)
    await db.commit()

    return db_patrocinio

#manipulação em massa
async def bulk_create_patrocinio(db: AsyncSession, patrocinios: list[PatrocinioCreate]):
    db_patrocinios = [Patrocinio(**patrocinio.model_dump()) for patrocinio in patrocinios]
    db.add_all(db_patrocinios)
    await db.commit()
    # Atualiza os objetos para garantir dados consistentes
    for patrocinio in db_patrocinios:
        await db.refresh(patrocinio)
    return db_patrocinios