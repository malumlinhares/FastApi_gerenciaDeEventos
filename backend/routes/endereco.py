from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from backend.config.database import get_db
from backend.schemas.endereco import EnderecoCreate, EnderecoResponse
from backend.crud.endereco import create_endereco, get_endereco, update_endereco, delete_endereco

router = APIRouter()

@router.post("/", response_model=EnderecoResponse)
async def create_endereco_api(endereco: EnderecoCreate, db: AsyncSession = Depends(get_db)):
    return await create_endereco(db=db, endereco=endereco)

@router.get("/{endereco_id}", response_model=EnderecoResponse)
async def read_endereco_api(endereco_id: int, db: AsyncSession = Depends(get_db)):
    db_endereco = await get_endereco(db=db, endereco_id=endereco_id)
    if db_endereco is None:
        raise HTTPException(status_code=404, detail="Endereço não encontrado")
    return db_endereco

@router.put("/{endereco_id}", response_model=EnderecoResponse)
async def update_endereco_api(
    endereco_id: int,
    endereco: EnderecoCreate,
    db: AsyncSession = Depends(get_db)
):
    db_endereco = await update_endereco(db=db, endereco_id=endereco_id, endereco=endereco)
    if db_endereco is None:
        raise HTTPException(status_code=404, detail="Endereço não encontrado")
    return db_endereco

@router.delete("/{endereco_id}", response_model=EnderecoResponse)
async def delete_endereco_api(
    endereco_id: int,
    db: AsyncSession = Depends(get_db)
):
    db_endereco = await delete_endereco(db=db, endereco_id=endereco_id)
    if db_endereco is None:
        raise HTTPException(status_code=404, detail="Endereço não encontrado")
    return db_endereco
