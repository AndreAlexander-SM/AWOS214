#Importaciones
from fastapi import FastAPI
import asyncio

# Instancia del servidor
app = FastAPI()

#Endpoints
@app.get("/")
async def bienvenida():
    return {"mensaje": "Bienvenido a mi API!"}

@app.get("/HolaMundo")
async def hola():
    await asyncio.sleep(4) #simulacion de una peticion
    return {
        "mensaje": "Hola Mundo FastAPI!",
        "estatus":"200"
        }