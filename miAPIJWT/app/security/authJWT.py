from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

# ── Configuración JWT ────────────────────────────────────────────
SECRET_KEY = "8c412d7278d43b2e87906eb663aa88b56e5877d01017c22f630eace0627ddd0"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# ── Configuración OAuth2 ─────────────────────────────────────────
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/auth/login")

# ── Hash de contraseñas ──────────────────────────────────────────
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ── Base de usuarios para autenticación (en memoria) ─────────────
usuarios_auth = {
    "admin": {
        "username": "admin",
        "hashed_password": pwd_context.hash("admin123"),
        "activo": True
    }
}

# ── Funciones ────────────────────────────────────────────────────

def verificar_password(password_plano: str, password_hash: str) -> bool:
    return pwd_context.verify(password_plano, password_hash)

def autenticar_usuario(username: str, password: str):
    usuario = usuarios_auth.get(username)
    if not usuario:
        return None
    if not verificar_password(password, usuario["hashed_password"]):
        return None
    return usuario

def crear_token_acceso(data: dict, expires_delta: timedelta = None) -> str:
    datos = data.copy()
    if expires_delta:
        if expires_delta > timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES):
            expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        expiracion = datetime.now(timezone.utc) + expires_delta
    else:
        expiracion = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    datos.update({"exp": expiracion})
    return jwt.encode(datos, SECRET_KEY, algorithm=ALGORITHM)

async def verificar_Peticion(token: str = Depends(oauth2_scheme)) -> dict:
    credenciales_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credenciales_exception
    except JWTError:
        raise credenciales_exception

    usuario = usuarios_auth.get(username)
    if usuario is None or not usuario["activo"]:
        raise credenciales_exception

    return usuario