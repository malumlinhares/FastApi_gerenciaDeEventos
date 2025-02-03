from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from backend.config.database import get_db
from backend.schemas.inscricao import InscricaoCreate, InscricaoResponse
from backend.crud.inscricao import create_inscricao, get_inscricao, update_inscricao, delete_inscricao

router = APIRouter()

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
