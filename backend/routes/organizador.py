from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from backend.config.database import get_db
from backend.schemas.organizador import OrganizadorCreate, OrganizadorResponse
from backend.crud.organizador import create_organizador, get_organizador, update_organizador, delete_organizador, bulk_create_organizador
from typing import List

router = APIRouter()

@router.post("/", response_model=OrganizadorResponse)
async def create_organizador_api(organizador: OrganizadorCreate, db: AsyncSession = Depends(get_db)):
    return await create_organizador(db=db, organizador=organizador)

@router.get("/{organizador_id}", response_model=OrganizadorResponse)
async def read_organizador_api(organizador_id: int, db: AsyncSession = Depends(get_db)):
    db_organizador = await get_organizador(db=db, organizador_id=organizador_id)
    if db_organizador is None:
        raise HTTPException(status_code=404, detail="Público não encontrado")
    return db_organizador


@router.put("/{organizador_id}", response_model=OrganizadorResponse)
async def update_organizador_api(
    organizador_id: int, 
    organizador: OrganizadorCreate, 
    db: AsyncSession = Depends(get_db)
):
    db_organizador = await update_organizador(db=db, organizador_id=organizador_id, organizador=organizador)
    if db_organizador is None:
        raise HTTPException (status_code=404, detail = "organizador nao encontrado")
    return db_organizador

@router.delete("/{organizador_id}", response_model=OrganizadorResponse)
async def delete_organizador_api(
    organizador_id: int, 
    db: AsyncSession = Depends(get_db)
):
    db_organizador = await delete_organizador(db=db, organizador_id=organizador_id)
    
    if db_organizador is None:
        raise HTTPException(status_code=404, detail="organizador não encontrado")
    
    return db_organizador


@router.post("/bulk", response_model=List[OrganizadorResponse])
async def bulk_create_organizadores(
    organizadores: List[OrganizadorCreate], 
    db: AsyncSession = Depends(get_db)
):
    try:
        return await bulk_create_organizador(db, organizadores)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))