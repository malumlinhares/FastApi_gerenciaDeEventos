from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.certificado import Certificado
from schemas.certificado import CertificadoCreate

async def create_certificado(db: AsyncSession, certificado: CertificadoCreate):
    db_certificado = Certificado(
        evento_id=certificado.evento_id,
        participante_id=certificado.participante_id,
        autenticador_id=certificado.autenticador_id
    )
    db.add(db_certificado)
    await db.commit()
    await db.refresh(db_certificado)
    return db_certificado

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
