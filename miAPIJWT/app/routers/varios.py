#Endpoints
from typing import Optional
from app.data.database import usuarios
import asyncio
from fastapi import APIRouter

router = APIRouter(tags=['Varios'])

@router.get("/")
async def bienvenida():
    return {"mensaje": "Bienvenido a mi API!"}

@router.get("/HolaMundo")
async def hola():
    await asyncio.sleep(3) #simulacion de una peticion
    return {
        "mensaje": "Hola Mundo FastAPI!",
        "estatus":"200"
        }

@router.get("/v1/parametroOb/{id}")
async def consultaUno(id:int):
    return {"Se encontro usuario": id}

@router.get("/v1/parametroOp/")
async def consultaTodos(id:Optional[int] = None):
    if id is not None:
        for usuario in usuarios:
            if usuario["id"] == id:
                return{"mensaje":"usuario encontrado", "usuario": usuario}
        return{"mensaje":"usuario no encontrado", "usuario": id}
    else:
        return{"mensaje":"No se proporciono id" }