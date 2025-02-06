from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from backend.config.database import get_db
from backend.schemas.privilegio import PrivilegioCreate, PrivilegioResponse
from backend.crud.privilegio import create_privilegio, get_privilegio, update_privilegio, delete_privilegio, bulk_create_privilegio
from typing import List

router = APIRouter()

@router.post("/", response_model=PrivilegioResponse)
async def create_privilegio_api(privilegio: PrivilegioCreate, db: AsyncSession = Depends(get_db)):
    return await create_privilegio(db=db, privilegio=privilegio)

@router.get("/{privilegio_id}", response_model=PrivilegioResponse)
async def read_privilegio_api(privilegio_id: int, db: AsyncSession = Depends(get_db)):
    db_privilegio = await get_privilegio(db=db, privilegio_id=privilegio_id)
    if db_privilegio is None:
        raise HTTPException(status_code=404, detail="Privilégio não encontrado")
    return db_privilegio

@router.put("/{privilegio_id}", response_model=PrivilegioResponse)
async def update_privilegio_api(
    privilegio_id: int,
    privilegio: PrivilegioCreate,
    db: AsyncSession = Depends(get_db)
):
    db_privilegio = await update_privilegio(db=db, privilegio_id=privilegio_id, privilegio=privilegio)
    if db_privilegio is None:
        raise HTTPException(status_code=404, detail="Privilégio não encontrado")
    return db_privilegio

@router.delete("/{privilegio_id}", response_model=PrivilegioResponse)
async def delete_privilegio_api(
    privilegio_id: int,
    db: AsyncSession = Depends(get_db)
):
    db_privilegio = await delete_privilegio(db=db, privilegio_id=privilegio_id)
    if db_privilegio is None:
        raise HTTPException(status_code=404, detail="Privilégio não encontrado")
    return db_privilegio


@router.post("/bulk", response_model=List[PrivilegioResponse])
async def bulk_create_privilegios(
    privilegios: List[PrivilegioCreate], 
    db: AsyncSession = Depends(get_db)
):
    try:
        return await bulk_create_privilegios(db, privilegios)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))