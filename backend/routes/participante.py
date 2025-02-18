from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from backend.config.database import get_db
from backend.schemas.participante import ParticipanteCreate, ParticipanteResponse
from backend.crud.participante import create_participante, get_participante, update_participante, delete_participante, bulk_create_participante, get_participantes_com_certificados_inner_join, get_participantes_com_certificados_left_join, get_participantes_ordenados, create_participante_com_endereco, get_all_participantes
from typing import List, Dict

router = APIRouter()

@router.get("/", response_model=List[ParticipanteResponse])
async def list_autenticadores(db: AsyncSession = Depends(get_db)):
    autenticadores = await get_all_participantes(db=db)  
    return autenticadores

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


@router.post("/bulk", response_model=List[ParticipanteResponse])
async def bulk_create_participantes(
    participantes: List[ParticipanteCreate], 
    db: AsyncSession = Depends(get_db)
):
    try:
        return await bulk_create_participante(db, participantes)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/participantes/com-certificados-inner", response_model=List[ParticipanteResponse])
async def read_participantes_com_certificados_inner(db: AsyncSession = Depends(get_db)):

    return await get_participantes_com_certificados_inner_join(db)

@router.get("/participantes/com-certificados-left", response_model=List[ParticipanteResponse])
async def read_participantes_com_certificados_left(db: AsyncSession = Depends(get_db)):

    return await get_participantes_com_certificados_left_join(db)

@router.get("/participantes/ordenados", response_model=List[ParticipanteResponse])
async def read_participantes_ordenados(db: AsyncSession = Depends(get_db), ordem: str = 'ASC'):
    return await get_participantes_ordenados(db, ordem)

from backend.schemas.endereco import EnderecoCreate
@router.post("/participante-com-endereco")
async def create_participante_com_endereco_route(
    participante: ParticipanteCreate,
    endereco: EnderecoCreate,
    db: AsyncSession = Depends(get_db)
):
    return await create_participante_com_endereco(db, participante, endereco)