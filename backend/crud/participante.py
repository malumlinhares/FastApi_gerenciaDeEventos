from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from backend.models.participante import Participante
from backend.schemas.participante import ParticipanteCreate
from backend.models.participante import TipoParticipante
from sqlalchemy.orm import joinedload
from sqlalchemy.future import select
from backend.models.certificado import Certificado  
from sqlalchemy import text
# from sqlalchemy.orm import joinedload


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
    try:
        # Validações adicionais antes de criar o participante
        if participante.tipo == TipoParticipante.vip:
            if not participante.anuidade or participante.anuidade <= 0:
                raise ValueError("Anuidade deve ser maior que zero para participantes do tipo 'vip'.")
            if participante.elegivel_upgrade != 0:
                raise ValueError("Elegível para upgrade deve ser 0 para participantes do tipo 'vip'.")
        elif participante.tipo == TipoParticipante.padrao:
            if participante.anuidade != 0:
                raise ValueError("Anuidade deve ser zero para participantes do tipo 'padrao'.")
            if participante.elegivel_upgrade != 1:
                raise ValueError("Elegível para upgrade deve ser 1 para participantes do tipo 'padrao'.")

        query = text("""
            INSERT INTO participantes (nome, email, tipo, anuidade, elegivel_upgrade, endereco_id, telefone, responsavel)
            VALUES (:nome, :email, :tipo, :anuidade, :elegivel_upgrade, :endereco_id, :telefone, :responsavel)
            RETURNING id, nome, email, tipo, anuidade, elegivel_upgrade, telefone, responsavel
        """)
        params = {
            "nome": participante.nome,
            "email": participante.email,
            "tipo": participante.tipo,
            "anuidade": participante.anuidade,
            "elegivel_upgrade": participante.elegivel_upgrade,
            "endereco_id": participante.endereco_id,
            "telefone": participante.telefone,
            "responsavel": participante.responsavel
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
            "elegivel_upgrade": row.elegivel_upgrade,
            "endereco_id": row.endereco_id,
            "telefone": row.telefone,
            "responsavel": row.responsavel
        }

    except ValueError as e:
        raise e  # Levanta a exceção de validação se algo estiver errado

    except Exception as e:
        await db.rollback()  # Reverte a transação em caso de erro
        raise e  # Levanta a exceção para ser tratada em nível superior


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
    db_participante.endereco_id = participante.endereco_id
    db_participante.telefone = participante.telefone
    db_participante.responsavel = participante.responsavel
    
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


# async def get_participantes_com_certificados_inner_join(db: AsyncSession):
#     """
#     Retorna todos os participantes que possuem certificados (INNER JOIN).
#     """
#     query = (
#         select(Participante)
#         .join(Certificado, Participante.id == Certificado.participante_id)
#         .options(joinedload(Participante.certificado))
#     )
#     result = await db.execute(query)
#     return result.scalars().unique().all()

async def get_participantes_com_certificados_inner_join(db: AsyncSession):
    """
    Retorna todos os participantes que possuem certificados (INNER JOIN).
    """
    query = text("""
        SELECT p.*
        FROM participantes p
        INNER JOIN certificados c ON p.id = c.participante_id
    """)
    
    result = await db.execute(query)
    participantes = result.fetchall()  
    return participantes


async def get_participantes_com_certificados_left_join(db: AsyncSession):
    """
    Retorna todos os participantes, incluindo aqueles sem certificados (LEFT JOIN).
    """
    query = text("""
        SELECT p.*
        FROM participantes p
        LEFT JOIN certificados c ON p.id = c.participante_id
    """)
    
    result = await db.execute(query)
    participantes = result.fetchall()  
    return participantes

async def get_participantes_ordenados(db: AsyncSession, ordem: str):
    """
    Retorna todos os participantes ordenados pelo nome.
    A ordenação pode ser 'ASC' para ascendente ou 'DESC' para descendente.
    """
    if ordem.upper() not in {"ASC", "DESC"}:
        raise ValueError("A ordenação deve ser 'ASC' ou 'DESC'.")

    query = text("""
        SELECT p.id, p.nome, p.email, p.tipo, p.anuidade, p.elegivel_upgrade, p.endereco_id
        FROM participantes p
        ORDER BY p.nome """ + ordem.upper())

    result = await db.execute(query)
    participantes = result.fetchall()
    return participantes

from backend.schemas.endereco import EnderecoCreate
from backend.models.endereco import Endereco

async def create_participante_com_endereco(db: AsyncSession, participante: ParticipanteCreate, endereco: EnderecoCreate):
    endereco_db = Endereco(**endereco.dict())
    db.add(endereco_db)
    await db.commit() 
    await db.refresh(endereco_db)  

    participante_dict = participante.dict(exclude_unset=True)
    participante_dict['endereco_id'] = endereco_db.id  

    participante_db = Participante(**participante_dict)
    db.add(participante_db)
    await db.commit()
    await db.refresh(participante_db)

    return participante_db


