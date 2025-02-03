from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from backend.config.database import get_db
from backend.schemas.patrocinador import PatrocinadorCreate, PatrocinadorResponse
from backend.crud.patrocinador import create_patrocinador, get_patrocinador, delete_patrocinador, update_patrocinador 

router = APIRouter()

@router.post("/", response_model=PatrocinadorResponse)
async def create_patrocinador_api(patrocinador: PatrocinadorCreate, db: AsyncSession = Depends(get_db)):
    print(f"JSON recebido: {patrocinador.dict()}")  # Debug para verificar o JSON
    return await create_patrocinador(db=db, patrocinador=patrocinador)

@router.get("/{patrocinador_id}", response_model=PatrocinadorResponse)
async def read_patrocinador_api(patrocinador_id: int, db: AsyncSession = Depends(get_db)):
    db_patrocinador = await get_patrocinador(db=db, patrocinador_id=patrocinador_id)
    if db_patrocinador is None:
        raise HTTPException(status_code=404, detail="Patrocinador não encontrado")
    return db_patrocinador

@router.put("/{patrocinador_id}", response_model=PatrocinadorResponse)
async def update_patrocinador_api(
    patrocinador_id: int, 
    patrocinador: PatrocinadorCreate, 
    db: AsyncSession = Depends(get_db)
):
    db_patrocinador = await update_patrocinador(db=db, patrocinador_id=patrocinador_id, patrocinador=patrocinador)
    if db_patrocinador is None:
        raise HTTPException (status_code=404, detail = "Patrocinador nao encontrado")
    return db_patrocinador

@router.delete("/{patrocinador_id}", response_model=PatrocinadorResponse)
async def delete_patrocinador_api(
    patrocinador_id: int, 
    db: AsyncSession = Depends(get_db)
):
    db_patrocinador = await delete_patrocinador(db=db, patrocinador_id=patrocinador_id)
    
    if db_patrocinador is None:
        raise HTTPException(status_code=404, detail="Patrocinador não encontrado")
    
    return db_patrocinador