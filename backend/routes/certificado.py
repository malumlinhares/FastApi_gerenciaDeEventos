from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from backend.config.database import get_db
from backend.schemas.certificado import CertificadoCreate, CertificadoResponse
from backend.crud.certificado import create_certificado, get_certificado, update_certificado, delete_certificado

router = APIRouter()

@router.post("/", response_model=CertificadoResponse)
async def create_certificado_api(certificado: CertificadoCreate, db: AsyncSession = Depends(get_db)):
    return await create_certificado(db=db, certificado=certificado)

@router.get("/{certificado_id}", response_model=CertificadoResponse)
async def read_certificado_api(certificado_id: int, db: AsyncSession = Depends(get_db)):
    db_certificado = await get_certificado(db=db, certificado_id=certificado_id)
    if db_certificado is None:
        raise HTTPException(status_code=404, detail="Certificado não encontrado")
    return db_certificado

@router.put("/{certificado_id}", response_model=CertificadoResponse)
async def update_certificado_api(
    certificado_id: int,
    certificado: CertificadoCreate,
    db: AsyncSession = Depends(get_db)
):
    db_certificado = await update_certificado(db=db, certificado_id=certificado_id, certificado=certificado)
    if db_certificado is None:
        raise HTTPException(status_code=404, detail="Certificado não encontrado")
    return db_certificado

@router.delete("/{certificado_id}", response_model=CertificadoResponse)
async def delete_certificado_api(
    certificado_id: int,
    db: AsyncSession = Depends(get_db)
):
    db_certificado = await delete_certificado(db=db, certificado_id=certificado_id)
    if db_certificado is None:
        raise HTTPException(status_code=404, detail="Certificado não encontrado")
    return db_certificado
