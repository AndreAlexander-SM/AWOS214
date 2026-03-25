#Modelo de validacion Pydantic
from pydantic import BaseModel, Field

class usuario_create(BaseModel):
    nombre:str = Field(..., min_length=3,max_length=50,example="Juanita")
    edad:int = Field(..., ge=1, le=123, description="Edad valida entre 1 y 123")