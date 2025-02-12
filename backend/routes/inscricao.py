from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from backend.config.database import get_db
from backend.schemas.inscricao import InscricaoCreate, InscricaoResponse
from backend.crud.inscricao import create_inscricao, get_inscricao, update_inscricao, delete_inscricao, bulk_create_inscricao, get_all_inscricoes
from typing import List

router = APIRouter()

@router.get("/", response_model=List[InscricaoResponse])
async def list_autenticadores(db: AsyncSession = Depends(get_db)):
    autenticadores = await get_all_inscricoes(db=db)  # Função que retorna todos os autenticadores
    return autenticadores

@router.post("/", response_model=InscricaoResponse)
async def create_inscricao_api(inscricao: InscricaoCreate, db: AsyncSession = Depends(get_db)):
    return await create_inscricao(db=db, inscricao=inscricao)

@router.get("/{inscricao_id}", response_model=InscricaoResponse)
async def read_inscricao_api(inscricao_id: int, db: AsyncSession = Depends(get_db)):
    db_inscricao = await get_inscricao(db=db, inscricao_id=inscricao_id)
    if db_inscricao is None:
        raise HTTPException(status_code=404, detail="Inscrição não encontrada")
    return db_inscricao

@router.put("/{inscricao_id}", response_model=InscricaoResponse)
async def update_inscricao_api(
    inscricao_id: int,
    inscricao: InscricaoCreate,
    db: AsyncSession = Depends(get_db)
):
    db_inscricao = await update_inscricao(db=db, inscricao_id=inscricao_id, inscricao=inscricao)
    if db_inscricao is None:
        raise HTTPException(status_code=404, detail="Inscrição não encontrada")
    return db_inscricao

@router.delete("/{inscricao_id}", response_model=InscricaoResponse)
async def delete_inscricao_api(
    inscricao_id: int,
    db: AsyncSession = Depends(get_db)
):
    db_inscricao = await delete_inscricao(db=db, inscricao_id=inscricao_id)
    if db_inscricao is None:
        raise HTTPException(status_code=404, detail="Inscrição não encontrada")
    return db_inscricao

@router.post("/bulk", response_model=List[InscricaoResponse])
async def bulk_create_inscricoes(
    inscricoes: List[InscricaoCreate], 
    db: AsyncSession = Depends(get_db)
):
    try:
        return await bulk_create_inscricao(db, inscricoes)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))