from fastapi import FastAPI,status, HTTPException, Depends
import asyncio
from pydantic import BaseModel, Field
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets

app = FastAPI(
    title="Examen 2parcial",
    description="Andre Alexander Sierra Martinez",
    version="1.0.0"
)

tickets = [
    {"id":1, "nombre" : "Andre", "descripcion" : "No prende la lap", "prioridad" : "baja", "estado": "pediente"},
    {"id":2, "nombre" : "Santiago", "descripcion" : "No prende corre el programa", "prioridad" : "media", "estado": "pediente"},
    {"id":3, "nombre" : "Ruth", "descripcion" : "Salio pantallaso azul", "prioridad" : "alta", "estado": "pediente"}
]   

nombre:str = Field(..., min_length=5, max_digits=50, example="Andre")
descripcion:str = Field(...,min_length=26, max_digits=200, description="Descripción del problea")


security = HTTPBasic()

def verificar_Peticon(credenciales: HTTPBasicCredentials=Depends(security)):
    userAuth = secrets.compare_digest(credenciales.username, "soporte")
    passAuth = secrets.compare_digest(credenciales.password, "4321")

    if not(userAuth and passAuth):
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail= "Credenciales no autorizadas"
        )
    
    return credenciales.username

@app.get("/v1/listar/", tags=["CRUD"])
async def listar_ticket():
    return {
        "status" : "200",
        "total" :len(tickets),
        "tickets": tickets
    }

@app.post("/v1/crear", tags=["CRUD"])
async def crear_ticket(ticket):
    for urs in tickets:
        if urs["id"] == ticket.id:
            raise HTTPException(
                status_code=400,
                detail="El id ya existe"
            )
    tickets.append(ticket)
    return{
        "mensaje":"Ticket creado",
        "Ticket":ticket
    }

@app.get("/v1/porId", tags=["CRUD"])
async def buscar_id(id: int, userAuth = Depends(verificar_Peticon)):
    encontrado = [ticket for ticket in tickets if id == id]
    if not encontrado :
        return{"status": "400", "mensaje":"No se encontro ningun id"}
    
    return{
        "status" : "200",
        "total": len(encontrado),
        "tickets": encontrado
    }

@app.delete("/v1/eliminar/{id}", tags=["CRUD"])
async def eliminar_ticket(id:int):
    for ticket in tickets:
        if ticket["id"] == id:
            tickets.remove(ticket)
            return  
