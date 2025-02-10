from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from backend.models.local import Local
from backend.schemas.local import LocalCreate
from sqlalchemy import text

# async def create_local(db: AsyncSession, local: LocalCreate):
#     db_local = Local(
#         cidade=local.cidade, 
#         capacidade = local.capacidade, 
#         nome = local.nome, 
#     )
#     db.add(db_local)
#     await db.commit()
#     await db.refresh(db_local)
#     return db_local  

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
            "estado": local.estado,  # Novo campo opcional
            "descricao": local.descricao  # Novo campo opcional
        }

        result = await db.execute(query, params)
        row = result.fetchone()
        await db.commit()
        
        return {
            "id": row.id,
            "cidade": row.cidade,
            "nome": row.nome,
            "estado": row.estado,  # Retorna o valor do novo campo
            "descricao": row.descricao  # Retorna o valor do novo campo
        }

    except Exception as e:
        await db.rollback()  # Reverte a transação em caso de erro
        raise e  # Levanta a exceção para depuração ou mensagens de erro apropriadas




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
    # Atualiza os objetos para garantir dados consistentes
    for local in db_locais:
        await db.refresh(local)
    return db_locais

