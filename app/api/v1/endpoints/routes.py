from fastapi import APIRouter
from app.controller.NutriaController import read_root
from pydantic import BaseModel

class Pergunta(BaseModel):
    pergunta: str
    id_user: str

router = APIRouter()

@router.post("/nutria")
async def nutria_endpoint(question: Pergunta):
    response = await read_root(question)
    if response:
        return {"message": response}

