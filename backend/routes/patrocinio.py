from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from backend.config.database import get_db
from backend.schemas.patrocinio import PatrocinioCreate, PatrocinioResponse
from backend.crud.patrocinio import create_patrocinio, get_patrocinio, delete_patrocinio, update_patrocinio, bulk_create_patrocinio, get_all_patrocinios
from typing import List

router = APIRouter()

@router.get("/", response_model=List[PatrocinioResponse])
async def list_autenticadores(db: AsyncSession = Depends(get_db)):
    autenticadores = await get_all_patrocinios(db=db)  # Função que retorna todos os autenticadores
    return autenticadores


@router.post("/", response_model=PatrocinioResponse)
async def create_patrocinio_api(patrocinio: PatrocinioCreate, db: AsyncSession = Depends(get_db)):
    return await create_patrocinio(db=db, patrocinio=patrocinio)

@router.get("/{patrocinio_id}", response_model=PatrocinioResponse)
async def read_patrocinio_api(patrocinio_id: int, db: AsyncSession = Depends(get_db)):
    db_patrocinio = await get_patrocinio(db=db, patrocinio_id=patrocinio_id)
    if db_patrocinio is None:
        raise HTTPException(status_code=404, detail="Patrocinio não encontrado")
    return db_patrocinio

@router.put("/{patrocinio_id}", response_model=PatrocinioResponse)
async def update_patrocinio_api(
    patrocinio_id: int, 
    patrocinio: PatrocinioCreate, 
    db: AsyncSession = Depends(get_db)
):
    db_patrocinio = await update_patrocinio(db=db, patrocinio_id=patrocinio_id, patrocinio=patrocinio)
    if db_patrocinio is None:
        raise HTTPException (status_code=404, detail = "Patrocinio nao encontrado")
    return db_patrocinio

@router.delete("/{patrocinio_id}", response_model=PatrocinioResponse)
async def delete_patrocinio_api(
    patrocinio_id: int, 
    db: AsyncSession = Depends(get_db)
):
    db_patrocinio = await delete_patrocinio(db=db, patrocinio_id=patrocinio_id)
    
    if db_patrocinio is None:
        raise HTTPException(status_code=404, detail="Patrocinio não encontrado")
    
    return db_patrocinio

@router.post("/bulk", response_model=List[PatrocinioResponse])
async def bulk_create_patrocinios(
    patrocinios: List[PatrocinioCreate], 
    db: AsyncSession = Depends(get_db)
):
    try:
        return await bulk_create_patrocinio(db, patrocinios)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))