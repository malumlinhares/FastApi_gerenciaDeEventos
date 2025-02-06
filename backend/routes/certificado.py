from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from backend.config.database import get_db
from backend.schemas.certificado import CertificadoCreate, CertificadoResponse
from backend.crud.certificado import create_certificado, get_certificado, update_certificado, delete_certificado, bulk_create_certificado, count_certificados_por_participante
from typing import List, Dict

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

@router.post("/bulk", response_model=List[CertificadoResponse])
async def bulk_create_certificados(
    certificados: List[CertificadoCreate], 
    db: AsyncSession = Depends(get_db)
):
    try:
        return await bulk_create_certificado(db, certificados)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@router.get("/certificados/contagem-por-participante", response_model=List[Dict[str, int]])
async def read_certificados_contagem_por_participante(db: AsyncSession = Depends(get_db)):
    """
    Retorna a contagem de certificados por participante.
    """
    result = await count_certificados_por_participante(db)
    return [{"participante_id": row.participante_id, "total_certificados": row.total_certificados} for row in result]
