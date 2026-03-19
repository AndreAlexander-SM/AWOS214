
#Endponits de usuario

from fastapi import status, HTTPException, Depends, APIRouter
from app.models.usuario import usuario_create
from app.data.database import usuarios
from app.security.auth import verificar_Peticion

router = APIRouter(
    prefix= "/v1/usuarios", tags= ["CRUD HTTP"]
) 

@router.get("/")
async def leer_usuarios():
    return{
        "status":"200",
        "total": len(usuarios),
        "usuarios":usuarios
    }

@router.post("/",status_code=status.HTTP_201_CREATED)
async def crear_usuario(usuario:usuario_create):
    for usr in usuarios: 
        if usr["id"] == usuario.id:
            raise HTTPException(
                status_code=400,
                detail="El id ya existe"
            )
    usuarios.append(usuario)
    return{
        "mensaje":"Usuario Agregado",
        "Usuario":usuario
    }

@router.put("/{id}")
async def actualizar_usuario(id: int, usuario_actualizado: dict):
    for index, usr in enumerate(usuarios):
        if usr["id"] == id:
            usuarios[index].update(usuario_actualizado)
            return {
                "mensaje": "Usuario actualizado correctamente",
                "usuario": usuarios[index]
            }
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"El usuario con ID {id} no existe."
    )

@router.delete("/{id}")
async def eliminar_usuario(id: int, userAuth= Depends(verificar_Peticion)):
    for usuario in usuarios:
        if usuario["id"] == id:
            usuarios.remove(usuario)
            return {
                "mensaje": f"Usuario eliminado exitosamente {userAuth}",
                "usuarios_restantes": len(usuarios)
            }
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"No se pudo eliminar: El poñoñoin con ID {id} no existe"
    )