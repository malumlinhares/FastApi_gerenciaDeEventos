from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from backend.models.participante import Participante
from backend.schemas.participante import ParticipanteCreate
from backend.models.participante import TipoParticipante
from sqlalchemy.orm import joinedload
from sqlalchemy.future import select
from backend.models.certificado import Certificado  
from sqlalchemy import text


# async def create_participante(db: AsyncSession, participante: ParticipanteCreate):
#     db_participante = Participante(
#         nome=participante.nome,
#         email=participante.email,
#         tipo=TipoParticipante(participante.tipo),
#         anuidade = participante.anuidade,
#         elegivel_upgrade = participante.elegivel_upgrade

#     )
#     db.add(db_participante)
#     await db.commit()
#     await db.refresh(db_participante)
#     return db_participante

async def create_participante(db: AsyncSession, participante: ParticipanteCreate):
    query = text("""
        INSERT INTO participantes (nome, email, tipo, anuidade, elegivel_upgrade)
        VALUES (:nome, :email, :tipo, :anuidade, :elegivel_upgrade)
        RETURNING id, nome, email, tipo, anuidade, elegivel_upgrade
    """)
    params = {
        "nome": participante.nome,
        "email": participante.email,
        "tipo": participante.tipo, 
        "anuidade": participante.anuidade,  # Corrigido para remover a vírgula extra
        "elegivel_upgrade": participante.elegivel_upgrade
    }
    result = await db.execute(query, params)
    row = result.fetchone()
    await db.commit()
    return {
        "id": row.id,
        "nome": row.nome,
        "email": row.email,
        "tipo": row.tipo, 
        "anuidade": row.anuidade, 
        "elegivel_upgrade": row.elegivel_upgrade
    }


async def get_participante(db: AsyncSession, participante_id: int):
    result = await db.execute(select(Participante).filter(Participante.id == participante_id))
    participante = result.scalars().first()
    return participante

async def update_participante(db: AsyncSession, participante_id: int, participante: ParticipanteCreate):
    result = await db.execute(select(Participante).filter(Participante.id == participante_id))
    db_participante = result.scalars().first()
    if db_participante is None:
        return None
    db_participante.nome = participante.nome
    db_participante.email = participante.email
    db_participante.tipo = TipoParticipante(participante.tipo)
    db_participante.anuidade = participante.anuidade
    db_participante.elegivel_upgrade = participante.elegivel_upgrade
    
    await db.commit()
    await db.refresh(db_participante)
    return db_participante

async def delete_participante(db: AsyncSession, participante_id: int):
    result = await db.execute(select(Participante).filter(Participante.id == participante_id))
    db_participante = result.scalars().first()
    if db_participante is None:
        return None
    await db.delete(db_participante)
    await db.commit()
    return db_participante


async def bulk_create_participante(db: AsyncSession, participantes: list[ParticipanteCreate]):
    db_participantes = [Participante(**participante.model_dump()) for participante in participantes]
    db.add_all(db_participantes)
    await db.commit()
    # Atualiza os objetos para garantir dados consistentes
    for participante in db_participantes:
        await db.refresh(participante)
    return db_participantes


from sqlalchemy.orm import joinedload

async def get_participantes_com_certificados_inner_join(db: AsyncSession):
    """
    Retorna todos os participantes que possuem certificados (INNER JOIN).
    """
    query = (
        select(Participante)
        .join(Certificado, Participante.id == Certificado.participante_id)
        .options(joinedload(Participante.certificado))
    )
    result = await db.execute(query)
    return result.scalars().unique().all()

async def get_participantes_com_certificados_left_join(db: AsyncSession):
    """
    Retorna todos os participantes, incluindo aqueles sem certificados (LEFT JOIN).
    """
    query = (
        select(Participante)
        .outerjoin(Certificado, Participante.id == Certificado.participante_id)
        .options(joinedload(Participante.certificado))
    )
    result = await db.execute(query)
    return result.scalars().unique().all()