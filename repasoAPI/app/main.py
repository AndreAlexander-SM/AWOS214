from fastapi import FastAPI, status
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from typing import Optional

# Instancia del servidor
app = FastAPI(
    title='Practica de repaso',
    description='Andre Alexander Sierra Martinez',
    version='1.0.0'
)

libros = [
    {
        "id": 1,
        "nombre": "Cien años de soledad",
        "autor": "Gabriel García Márquez",
        "anio": 1967,
        "paginas": 471,
        "estado": "disponible"
    },
    {
        "id": 2,
        "nombre": "El Quijote",
        "autor": "Miguel de Cervantes",
        "anio": 1605,
        "paginas": 863,
        "estado": "disponible"
    },
]

prestamos = [
    {
        "id": 1,
        "id_libro": 2,
        "nombre_usuario": "Juan Pérez",
        "correo_usuario": "juan@email.com",
        "fecha_prestamo": "15/01/2024",
        "fecha_devolucion": None
    }
]

class Usuario(BaseModel):
    nombre: str = Field(..., min_length=3, max_length=50)
    correo: EmailStr

class Libro(BaseModel):
    id: int = Field(..., gt=0)
    nombre: str = Field(..., min_length=2, max_length=100)
    autor: str = Field(..., min_length=3, max_length=100)
    anio: int = Field(..., gt=1450, le=datetime.now().year)
    paginas: int = Field(..., gt=1)
    estado: str = "disponible"

class Prestamo(BaseModel):
    id: int = Field(..., gt=0)
    id_libro: int = Field(..., gt=0)
    usuario: Usuario

class Devolucion(BaseModel):
    id_prestamo: int = Field(..., gt=0)

@app.get("/", tags=["Inicio"])
async def bienvenida():
    return {"mensaje": "Bienvenido a mi Biblioteca Digital"}

@app.post("/registrar-libro", tags=["Libros"], status_code=status.HTTP_201_CREATED)
async def registrar_libro(libro: Libro):
    for lib in libros:
        if lib["id"] == libro.id:
            return {"status": "400", "mensaje": "El ID del libro ya existe"}

    nuevo_libro = {
        "id": libro.id,
        "nombre": libro.nombre,
        "autor": libro.autor,
        "anio": libro.anio,
        "paginas": libro.paginas,
        "estado": "disponible"
    }
    libros.append(nuevo_libro)

    return {
        "status": "201",
        "mensaje": "Libro registrado exitosamente",
        "libro": nuevo_libro
    }

@app.get("/libros-disponibles", tags=["Libros"])
async def libros_disponibles():
    disponibles = [libro for libro in libros if libro["estado"] == "disponible"]
    return {
        "status": "200",
        "total": len(disponibles),
        "libros": disponibles
    }

@app.get("/buscar-libro", tags=["Libros"])
async def buscar_libro(nombre: str):
    if not nombre or len(nombre.strip()) == 0:
        return {"status": "400", "mensaje": "Debe proporcionar un nombre para buscar"}

    encontrados = [libro for libro in libros if nombre.lower() in libro["nombre"].lower()]
    if not encontrados:
        return {"status": "400", "mensaje": "No se encontró ningún libro con ese nombre"}

    return {
        "status": "200",
        "total": len(encontrados),
        "libros": encontrados
    }

@app.post("/prestar-libro", tags=["Préstamos"], status_code=status.HTTP_201_CREATED)
async def prestar_libro(prestamo: Prestamo):
    libro_encontrado = None
    for libro in libros:
        if libro["id"] == prestamo.id_libro:
            libro_encontrado = libro
            break

    if libro_encontrado is None:
        return {"status": "400", "mensaje": "El libro no existe"}

    if libro_encontrado["estado"] != "disponible":
        return {"status": "409", "mensaje": "El libro ya está prestado"}

    for p in prestamos:
        if p["id"] == prestamo.id:
            return {"status": "400", "mensaje": "El ID del préstamo ya existe"}

    libro_encontrado["estado"] = "prestado"

    nuevo_prestamo = {
        "id": prestamo.id,
        "id_libro": prestamo.id_libro,
        "nombre_usuario": prestamo.usuario.nombre,
        "correo_usuario": prestamo.usuario.correo,
        "fecha_prestamo": datetime.now().strftime("%d/%m/%Y"),
        "fecha_devolucion": None
    }
    prestamos.append(nuevo_prestamo)

    return {
        "status": "201",
        "mensaje": "Préstamo registrado exitosamente",
        "prestamo": nuevo_prestamo
    }

@app.put("/devolver-libro", tags=["Préstamos"])
async def devolver_libro(devolucion: Devolucion):
    prestamo_encontrado = None
    for prestamo in prestamos:
        if prestamo["id"] == devolucion.id_prestamo:
            prestamo_encontrado = prestamo
            break

    if prestamo_encontrado is None:
        return {"status": "409", "mensaje": "El registro de préstamo no existe"}

    if prestamo_encontrado["fecha_devolucion"] is not None:
        return {"status": "400", "mensaje": "Este libro ya fue devuelto anteriormente"}

    prestamo_encontrado["fecha_devolucion"] = datetime.now().strftime("%d/%m/%Y")

    for libro in libros:
        if libro["id"] == prestamo_encontrado["id_libro"]:
            libro["estado"] = "disponible"
            break

    return {
        "status": "200",
        "mensaje": "Libro devuelto exitosamente",
        "prestamo": prestamo_encontrado
    }

@app.delete("/eliminar-prestamo/{id_prestamo}", tags=["Préstamos"])
async def eliminar_prestamo(id_prestamo: int):
    prestamo_encontrado = None
    for prestamo in prestamos:
        if prestamo["id"] == id_prestamo:
            prestamo_encontrado = prestamo
            break

    if prestamo_encontrado is None:
        return {"status": "409", "mensaje": "El registro de préstamo no existe"}

    if prestamo_encontrado["fecha_devolucion"] is None:
        for libro in libros:
            if libro["id"] == prestamo_encontrado["id_libro"]:
                libro["estado"] = "disponible"
                break

    prestamos.remove(prestamo_encontrado)

    return {
        "status": "200",
        "mensaje": "Registro de préstamo eliminado exitosamente",
        "prestamo_eliminado": prestamo_encontrado
    }

@app.get("/todos-los-libros", tags=["Consultas"])
async def ver_todos_libros():
    return {
        "status": "200",
        "total": len(libros),
        "libros": libros
    }

@app.get("/todos-los-prestamos", tags=["Consultas"])
async def ver_todos_prestamos():
    return {
        "status": "200",
        "total": len(prestamos),
        "prestamos": prestamos
    }