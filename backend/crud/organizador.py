from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from backend.models.organizador import Organizador
from backend.schemas.organizador import OrganizadorCreate
from sqlalchemy import text

# async def create_organizador(db: AsyncSession, organizador: OrganizadorCreate):
#     db_organizador = Organizador(
#         nome=organizador.nome,  # Preencher com os dados recebidos
#         email = organizador.email, 
#         cnpj = organizador.cnpj

#     )
#     db.add(db_organizador)
#     await db.commit()
#     await db.refresh(db_organizador)
#     return db_organizador  

async def create_organizador(db: AsyncSession, organizador: OrganizadorCreate):
    query = text("""
        INSERT INTO organizadores (nome, email, cnpj)
        VALUES (:nome, :email, :cnpj)
        RETURNING id, nome, email, cnpj
    """)
    params = {
        "nome": organizador.nome,
        "email": organizador.email,
        "cnpj": organizador.cnpj
    }
    result = await db.execute(query, params)
    row = result.fetchone()
    await db.commit()
    return {
        "id": row.id,
        "nome": row.nome,
        "email": row.email,
        "cnpj": row.cnpj
    }

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


async def bulk_create_organizador(db: AsyncSession, organizadores: list[OrganizadorCreate]):
    db_organizadores = [Organizador(**organizador.model_dump()) for organizador in organizadores]
    db.add_all(db_organizadores)
    await db.commit()
    # Atualiza os objetos para garantir dados consistentes
    for organizador in db_organizadores:
        await db.refresh(organizador)
    return db_organizadores