from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from backend.config.database import get_db
from backend.schemas.autenticador import AutenticadorCreate, AutenticadorResponse
from backend.crud.autenticador import create_autenticador, get_autenticador, update_autenticador, delete_autenticador

router = APIRouter()

@router.post("/", response_model=AutenticadorResponse)
async def create_autenticador_api(autenticador: AutenticadorCreate, db: AsyncSession = Depends(get_db)):
    return await create_autenticador(db=db, autenticador=autenticador)

@router.get("/{autenticador_id}", response_model=AutenticadorResponse)
async def read_autenticador_api(autenticador_id: int, db: AsyncSession = Depends(get_db)):
    db_autenticador = await get_autenticador(db=db, autenticador_id=autenticador_id)
    if db_autenticador is None:
        raise HTTPException(status_code=404, detail="Autenticador não encontrado")
    return db_autenticador

@router.put("/{autenticador_id}", response_model=AutenticadorResponse)
async def update_autenticador_api(
    autenticador_id: int,
    autenticador: AutenticadorCreate,
    db: AsyncSession = Depends(get_db)
):
    db_autenticador = await update_autenticador(db=db, autenticador_id=autenticador_id, autenticador=autenticador)
    if db_autenticador is None:
        raise HTTPException(status_code=404, detail="Autenticador não encontrado")
    return db_autenticador

@router.delete("/{autenticador_id}", response_model=AutenticadorResponse)
async def delete_autenticador_api(
    autenticador_id: int,
    db: AsyncSession = Depends(get_db)
):
    db_autenticador = await delete_autenticador(db=db, autenticador_id=autenticador_id)
    if db_autenticador is None:
        raise HTTPException(status_code=404, detail="Autenticador não encontrado")
    return db_autenticador
