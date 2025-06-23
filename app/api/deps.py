# api/deps.py

from typing import Generator
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import ValidationError
from sqlalchemy.orm import Session

# Importações de dentro do nosso projeto
from app.db.sessions import SessionLocal
from app.core.config import settings
from app.db import models
from app.schemas import token as token_schema
from app.crud import crud_user

# Esta linha cria um "esquema" de segurança.
# A `tokenUrl` aponta para o nosso endpoint de login que criamos anteriormente.
# O FastAPI usará isso para gerar a documentação interativa (o botão "Authorize").
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/login/token")

def get_db() -> Generator:
    """
    Dependência para obter uma sessão do banco de dados.
    Usa 'yield' para garantir que a sessão seja sempre fechada após a requisição.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> models.User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Decodifica o token JWT
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        # Pega o email (que é o 'sub'ject do token)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = token_schema.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    
    # Busca o usuário no banco de dados
    user = crud_user.get_by_email(db, email=token_data.username)
    if user is None:
        raise credentials_exception
    return user

def get_current_active_user(
    current_user: models.User = Depends(get_current_user)
) -> models.User:
    """
    Dependência que verifica se o usuário obtido pelo token está ativo.
    Rotas que precisam apenas de um usuário logado (qualquer um) usarão esta dependência.
    """
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

# --- Funções de verificação de Papel (Role) ---

def get_current_admin_user(
    current_user: models.User = Depends(get_current_active_user)
) -> models.User:
    """
    Verifica se o usuário logado e ativo é um Administrador.
    """
    if current_user.role != models.UserRole.ADMIN:
        raise HTTPException(
            status_code=403, detail="Not enough permissions. Admin required."
        )
    return current_user

def get_current_coordinator_or_admin(
    current_user: models.User = Depends(get_current_active_user)
) -> models.User:
    """
    Verifica se o usuário logado e ativo é um Coordenador ou Administrador.
    """
    if current_user.role not in [models.UserRole.ADMIN, models.UserRole.COORDINATOR]:
        raise HTTPException(
            status_code=403, detail="Not enough permissions. Coordinator or Admin required."
        )
    return current_user

def get_current_teacher_or_higher(
    current_user: models.User = Depends(get_current_active_user)
) -> models.User:
    """
    Verifica se o usuário logado e ativo é um Professor, Coordenador ou Administrador.
    """
    if current_user.role not in [models.UserRole.ADMIN, models.UserRole.COORDINATOR, models.UserRole.TEACHER]:
        raise HTTPException(
            status_code=403, detail="Not enough permissions. Teacher, Coordinator or Admin required."
        )
    return current_user