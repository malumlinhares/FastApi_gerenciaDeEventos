from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from backend.models.certificado import Certificado
from backend.schemas.certificado import CertificadoCreate
from sqlalchemy import func
from sqlalchemy import text
from sqlalchemy import text
#usando bibliofeca
# async def create_certificado(db: AsyncSession, certificado: CertificadoCreate):
#     db_certificado = Certificado(
#         evento_id=certificado.evento_id,
#         participante_id=certificado.participante_id,
#         autenticador_id=certificado.autenticador_id
#     )
#     db.add(db_certificado)
#     await db.commit()
#     await db.refresh(db_certificado)
#     return db_certificado

# usando sql nativo
async def create_certificado(db: AsyncSession, certificado: CertificadoCreate):
    query = text("""
        INSERT INTO certificados (evento_id, participante_id, autenticador_id)
        VALUES (:evento_id, :participante_id, :autenticador_id)
        RETURNING id, evento_id, participante_id, autenticador_id
    """)
    params = {
        "evento_id": certificado.evento_id,
        "participante_id": certificado.participante_id,
        "autenticador_id": certificado.autenticador_id
    }
    result = await db.execute(query, params)
    row = result.fetchone()
    await db.commit()
    return {
        "id": row.id,
        "evento_id": row.evento_id,
        "participante_id": row.participante_id,
        "autenticador_id": row.autenticador_id
    }


async def get_certificado(db: AsyncSession, certificado_id: int):
    result = await db.execute(select(Certificado).filter(Certificado.id == certificado_id))
    certificado = result.scalars().first()
    return certificado

async def update_certificado(db: AsyncSession, certificado_id: int, certificado: CertificadoCreate):
    result = await db.execute(select(Certificado).filter(Certificado.id == certificado_id))
    db_certificado = result.scalars().first()
    if db_certificado is None:
        return None
    db_certificado.evento_id = certificado.evento_id
    db_certificado.participante_id = certificado.participante_id
    db_certificado.autenticador_id = certificado.autenticador_id
    await db.commit()
    await db.refresh(db_certificado)
    return db_certificado

async def delete_certificado(db: AsyncSession, certificado_id: int):
    result = await db.execute(select(Certificado).filter(Certificado.id == certificado_id))
    db_certificado = result.scalars().first()
    if db_certificado is None:
        return None
    await db.delete(db_certificado)
    await db.commit()
    return db_certificado


async def bulk_create_certificado(db: AsyncSession, certificados: list[CertificadoCreate]):
    db_certificados = [Certificado(**certificado.model_dump()) for certificado in certificados]
    db.add_all(db_certificados)
    await db.commit()
    # Atualiza os objetos para garantir dados consistentes
    for certificado in db_certificados:
        await db.refresh(certificado)
    return db_certificados



from sqlalchemy import func

async def count_certificados_por_participante(db: AsyncSession):
    """
    Conta o número de certificados emitidos por participante.
    Retorna uma lista de dicionários com o ID do participante e a contagem de certificados.
    """
    query = (
        select(
            Certificado.participante_id,
            func.count(Certificado.id).label("total_certificados")
        )
        .group_by(Certificado.participante_id)
    )
    result = await db.execute(query)
    return result.all()
