#Importaciones
from fastapi import FastAPI
from app.routers import usuarios, varios
from app.data.db import engine
from app.data import usuario

usuario.Base.metadata.create_all(bind=engine)

# Instancia del servidor
app = FastAPI(
    title='Mi primer API 2',
    description='Andre Alexander Sierra Martinez',
    version='1.0.0'
    )

app.include_router(usuarios.router)
app.include_router(varios.router)