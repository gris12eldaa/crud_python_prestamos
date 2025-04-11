from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
import crud.user as UserCrud
import config.db
from schemas.user import User, UserCreate, UserUpdate, UserLogin, Token
from typing import List
from datetime import datetime, timedelta
from jose import JWTError, jwt

user = APIRouter()

SECRET_KEY = "secret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

bearer_scheme = HTTPBearer()

def get_db():
    db = config.db.SesionLocal()
    try:
        yield db
    finally:
        db.close()

def verify_token_simple(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    token = credentials.credentials
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token no proporcionado o inválido",
        )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")
        return email
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido o expirado")

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@user.post("/users/login", response_model=Token, tags=["Usuarios"])
async def login_for_access_token(user: UserLogin, db: Session = Depends(get_db)):
    user_db = UserCrud.get_user_by_email(db, email=user.correoElectronico)
    if not user_db or user_db.contrasena != user.contrasena:
        raise HTTPException(status_code=400, detail="Correo o contraseña incorrectos")
    access_token = create_access_token(data={"sub": user_db.correoElectronico})
    return {"access_token": access_token, "token_type": "bearer"}

@user.get('/users/', response_model=List[User], tags=['Usuarios'])
async def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), user_email: str = Depends(verify_token_simple)):
    return UserCrud.get_users(db=db, skip=skip, limit=limit)

@user.get("/users/{user_id}", response_model=User, tags=["Usuarios"])
async def get_user(user_id: str, db: Session = Depends(get_db), user_email: str = Depends(verify_token_simple)):
    user = UserCrud.get_user_by_id(db=db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user

@user.post("/usersCreate/", response_model=User, tags=["Usuarios"])
async def create_user(user: UserCreate, db: Session = Depends(get_db)):  
    return UserCrud.create_user(db=db, user=user)

@user.put("/usersUpdate/{user_id}", response_model=User, tags=["Usuarios"])
async def update_user(user_id: str, user_update: UserUpdate, db: Session = Depends(get_db), user_email: str = Depends(verify_token_simple)):
    updated_user = UserCrud.update_user(db=db, user_id=user_id, user=user_update)
    if updated_user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado o no se pudo actualizar")
    return updated_user

@user.delete("/usersDelete/{user_id}", tags=["Usuarios"])
async def delete_user(user_id: str, db: Session = Depends(get_db), user_email: str = Depends(verify_token_simple)):
    deleted = UserCrud.delete_user(db=db, user_id=user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Usuario no encontrado o no se pudo eliminar")
    return {"message": "Usuario eliminado correctamente"}