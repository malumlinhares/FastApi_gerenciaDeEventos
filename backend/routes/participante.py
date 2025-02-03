from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from backend.config.database import get_db
from backend.schemas.participante import ParticipanteCreate, ParticipanteResponse
from backend.crud.participante import create_participante, get_participante, update_participante, delete_participante

router = APIRouter()

@router.post("/", response_model=ParticipanteResponse)
async def create_participante_api(participante: ParticipanteCreate, db: AsyncSession = Depends(get_db)):
    return await create_participante(db=db, participante=participante)

@router.get("/{participante_id}", response_model=ParticipanteResponse)
async def read_participante_api(participante_id: int, db: AsyncSession = Depends(get_db)):
    db_participante = await get_participante(db=db, participante_id=participante_id)
    if db_participante is None:
        raise HTTPException(status_code=404, detail="Participante não encontrado")
    return db_participante

@router.put("/{participante_id}", response_model=ParticipanteResponse)
async def update_participante_api(
    participante_id: int,
    participante: ParticipanteCreate,
    db: AsyncSession = Depends(get_db)
):
    db_participante = await update_participante(db=db, participante_id=participante_id, participante=participante)
    if db_participante is None:
        raise HTTPException(status_code=404, detail="Participante não encontrado")
    return db_participante

@router.delete("/{participante_id}", response_model=ParticipanteResponse)
async def delete_participante_api(
    participante_id: int,
    db: AsyncSession = Depends(get_db)
):
    db_participante = await delete_participante(db=db, participante_id=participante_id)
    if db_participante is None:
        raise HTTPException(status_code=404, detail="Participante não encontrado")
    return db_participante
