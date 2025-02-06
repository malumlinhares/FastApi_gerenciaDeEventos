from sqlalchemy.ext.asyncio import AsyncSession
from backend.models.patrocinador import Patrocinador, TipoPatrocinador
from backend.schemas.patrocinador import PatrocinadorCreate
from sqlalchemy.future import select
from sqlalchemy import text

# Função para criar patrocinador
# async def create_patrocinador(db: AsyncSession, patrocinador: PatrocinadorCreate):
#     db_patrocinador = Patrocinador(
#         nome=patrocinador.nome,
#         email=patrocinador.email,
#         tipo=TipoPatrocinador(patrocinador.tipo),  # Convertendo para o tipo Enum
#         orgao_responsavel=patrocinador.orgao_responsavel,
#         responsavel_comercial=patrocinador.responsavel_comercial,
#     )
#     db.add(db_patrocinador)
#     await db.commit()
#     await db.refresh(db_patrocinador)
#     return db_patrocinador

async def create_patrocinador(db: AsyncSession, patrocinador: PatrocinadorCreate):
    query = text("""
        INSERT INTO patrocinadores (nome, email, tipo, orgao_responsavel, responsavel_comercial)
        VALUES (:nome, :email, :tipo, :orgao_responsavel, :responsavel_comercial)
        RETURNING id, nome, email, tipo, orgao_responsavel, responsavel_comercial
    """)
    params = {
        "nome": patrocinador.nome,
        "email": patrocinador.email,
        "tipo": patrocinador.tipo, 
        "orgao_responsavel": patrocinador.orgao_responsavel,  # Corrigido para remover a vírgula extra
        "responsavel_comercial": patrocinador.responsavel_comercial
    }
    result = await db.execute(query, params)
    row = result.fetchone()
    await db.commit()
    return {
        "id": row.id,
        "nome": row.nome,
        "email": row.email,
        "tipo": row.tipo, 
        "orgao_responsavel": row.orgao_responsavel, 
        "responsavel_comercial": row.responsavel_comercial
    }

# Função para buscar patrocinador
async def get_patrocinador(db: AsyncSession, patrocinador_id: int):
    result = await db.execute(
        select(Patrocinador).filter(Patrocinador.id == patrocinador_id)
    )
    patrocinador = result.scalars().first()
    return patrocinador

# Função para atualizar patrocinador
async def update_patrocinador(db: AsyncSession, patrocinador_id: int, patrocinador: PatrocinadorCreate):
    result = await db.execute(
        select(Patrocinador).filter(Patrocinador.id == patrocinador_id)
    )
    db_patrocinador = result.scalars().first()
    if db_patrocinador is None:
        return None

    db_patrocinador.nome = patrocinador.nome
    db_patrocinador.email = patrocinador.email
    db_patrocinador.tipo = TipoPatrocinador(patrocinador.tipo)  # Atualizando tipo (Enum)
    db_patrocinador.orgao_responsavel = patrocinador.orgao_responsavel
    db_patrocinador.responsavel_comercial = patrocinador.responsavel_comercial

    await db.commit()
    await db.refresh(db_patrocinador)
    return db_patrocinador

# Função para deletar patrocinador
async def delete_patrocinador(db: AsyncSession, patrocinador_id: int):
    result = await db.execute(
        select(Patrocinador).filter(Patrocinador.id == patrocinador_id)
    )
    db_patrocinador = result.scalars().first()
    if db_patrocinador is None:
        return None
    await db.delete(db_patrocinador)
    await db.commit()

    return db_patrocinador

async def bulk_create_patrocinador(db: AsyncSession, patrocinadores: list[PatrocinadorCreate]):
    db_patrocinadores = [Patrocinador(**patrocinador.model_dump()) for patrocinador in patrocinadores]
    db.add_all(db_patrocinadores)
    await db.commit()
    # Atualiza os objetos para garantir dados consistentes
    for patrocinador in db_patrocinadores:
        await db.refresh(patrocinador)
    return db_patrocinadores



# Função para buscar patrocinadores com uma substring no nome
# Função para buscar patrocinadores por substring no nome
async def search_patrocinador_by_name(db: AsyncSession, nome_substring: str):
    result = await db.execute(
        select(Patrocinador).filter(Patrocinador.nome.ilike(f"%{nome_substring}%"))
    )
    patrocinadores = result.scalars().all()
    return patrocinadores