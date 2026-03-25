
#Endponits de usuario

from fastapi import status, HTTPException, Depends, APIRouter
from app.models.usuario import usuario_create
from app.data.database import usuarios
from app.security.auth import verificar_Peticion

from sqlalchemy.orm import Session
from app.data.db import get_db
from app.data.usuario import Usuario as usuarioDB

router = APIRouter(
    prefix= "/v1/usuarios", tags= ["CRUD HTTP"]
) 

@router.get("/")
async def leer_usuarios(db: Session = Depends(get_db)):
    
    queryUsers= db.query(usuarioDB).all() 
    return{
        "status":"200",
        "total": len(queryUsers),
        "usuarios":queryUsers
    }

@router.post("/",status_code=status.HTTP_201_CREATED)
async def crear_usuario(usuarioP:usuario_create, db:Session= Depends(get_db)):
    
    nuevoUsuario= usuarioDB(nombre= usuarioP.nombre, edad= usuarioP.edad)
    db.add(nuevoUsuario)
    db.commit()
    db.refresh(nuevoUsuario)


    return{
        "mensaje":"Usuario Agregado",
        "Usuario":usuarioP
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