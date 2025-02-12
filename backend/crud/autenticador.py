from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from backend.models.autenticador import Autenticador
from backend.schemas.autenticador import AutenticadorCreate
from sqlalchemy import text

async def get_all_autenticadores(db: AsyncSession):
    result = await db.execute(select(Autenticador))  # Executa a consulta para buscar todos os autenticadores
    return result.scalars().all() 

#usando a biblioteca
# async def create_autenticador(db: AsyncSession, autenticador: AutenticadorCreate):
#     db_autenticador = Autenticador(orgao=autenticador.orgao)
#     db.add(db_autenticador)
#     await db.commit()
#     await db.refresh(db_autenticador)
#     return db_autenticador

#usando sqlnativo:

async def create_autenticador(db: AsyncSession, autenticador: AutenticadorCreate):
    try:
        query = text("""
            INSERT INTO autenticadores (chave_autenticacao, orgao, status, data_expiracao)
            VALUES (:chave_autenticacao, :orgao, :status, :data_expiracao)
            RETURNING id, chave_autenticacao, orgao, status, data_expiracao
        """)

        result = await db.execute(
            query,
            {
                "chave_autenticacao": autenticador.chave_autenticacao,
                "orgao": autenticador.orgao,
                "status": autenticador.status,
                "data_expiracao": autenticador.data_expiracao,
            }
        )

        row = result.fetchone()  
        await db.commit()  
        return {
            "id": row.id,
            "chave_autenticacao": row.chave_autenticacao,
            "orgao": row.orgao,
            "status": row.status,
            "data_expiracao": row.data_expiracao
        }

    except Exception as e:
        await db.rollback()  
        raise e  


async def get_autenticador(db: AsyncSession, autenticador_id: int):
    result = await db.execute(select(Autenticador).filter(Autenticador.id == autenticador_id))
    return result.scalars().first()

async def update_autenticador(db: AsyncSession, autenticador_id: int, autenticador: AutenticadorCreate):
    result = await db.execute(select(Autenticador).filter(Autenticador.id == autenticador_id))
    db_autenticador = result.scalars().first()
    if db_autenticador is None:
        return None
    db_autenticador.chave_autenticacao = autenticador.chave_autenticacao
    db_autenticador.orgao = autenticador.orgao
    db_autenticador.status = autenticador.status
    db_autenticador.data_expiracao = autenticador.data_expiracao
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
    for autenticador in db_autenticadores:
        await db.refresh(autenticador)
    return db_autenticadores
