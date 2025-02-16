from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from backend.models.local import Local
from backend.schemas.local import LocalCreate
from sqlalchemy import text

async def get_all_locais(db: AsyncSession):
    result = await db.execute(select(Local))  
    return result.scalars().all() 

async def create_local(db: AsyncSession, local: LocalCreate):
    try:
        query = text("""
            INSERT INTO locais (cidade, nome, estado, descricao)
            VALUES (:cidade, :nome, :estado, :descricao)
            RETURNING id, cidade, nome, estado, descricao
        """)
        params = {
            "cidade": local.cidade,
            "nome": local.nome,
            "estado": local.estado, 
            "descricao": local.descricao  
        }

        result = await db.execute(query, params)
        row = result.fetchone()
        await db.commit()
        
        return {
            "id": row.id,
            "cidade": row.cidade,
            "nome": row.nome,
            "estado": row.estado,  
            "descricao": row.descricao  
        }

    except Exception as e:
        await db.rollback()  
        raise e  


async def get_local(db: AsyncSession, local_id: int):
    result = await db.execute(
        select(Local).filter(Local.id == local_id)
    )
    local = result.scalars().first()
    return local 


async def update_local(db: AsyncSession, local_id: int, local: LocalCreate):
    result = await db.execute(
        select(Local).filter(Local.id == local_id)
    )
    db_local = result.scalars().first()
    if db_local is None:
        return None
    db_local.cidade = local.cidade
    db_local.nome = local.nome
    db_local.estado = local.estado
    db_local.descricao = local.descricao
    
    await db.commit()
    await db.refresh(db_local)
    return db_local

async def delete_local(db:AsyncSession, local_id: int):
    result = await db.execute(
        select(Local).filter(Local.id==local_id)
    )
    db_local = result.scalars().first()
    if db_local is None:
        return None
    await db.delete(db_local)
    await db.commit()
    return db_local

async def bulk_create_local(db: AsyncSession, locais: list[LocalCreate]):
    db_locais = [Local(**local.model_dump()) for local in locais]
    db.add_all(db_locais)
    await db.commit()
    for local in db_locais:
        await db.refresh(local)
    return db_locais

