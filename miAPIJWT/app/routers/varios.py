#Endpoints
import asyncio
from typing import Optional
from fastapi.security import OAuth2PasswordRequestForm
from app.security.authJWT import autenticar_usuario, crear_token_acceso, ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import timedelta
from fastapi import status, HTTPException, Depends, APIRouter
from app.data.database import usuarios
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
    
@router.post("/v1/auth/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    usuario = autenticar_usuario(form_data.username, form_data.password)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = crear_token_acceso(
        data={"sub": usuario["username"]},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": token, "token_type": "bearer"}
