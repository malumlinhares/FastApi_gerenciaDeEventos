from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from backend.config.database import get_db
from backend.schemas.patrocinio import PatrocinioCreate, PatrocinioResponse
from backend.crud.patrocinio import create_patrocinio, get_patrocinio, delete_patrocinio, update_patrocinio 

router = APIRouter()

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