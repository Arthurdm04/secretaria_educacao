# app/core/security.py

from datetime import datetime, timedelta, timezone
from typing import Any
from jose import jwt
from passlib.context import CryptContext

from app.core.config import settings

# Configura o passlib para usar o algoritmo bcrypt para hashear as senhas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ALGORITHM = settings.ALGORITHM

def create_access_token(subject: str | Any, expires_delta: timedelta | None = None) -> str:
    """
    Cria um novo token de acesso JWT.
    """
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    # O 'sub' (subject) é o email do usuário, e 'exp' é o tempo de expiração.
    # Você pode adicionar outros dados ao token se precisar.
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica se uma senha em texto plano corresponde a uma senha hasheada.
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Gera o hash de uma senha em texto plano.
    """
    return pwd_context.hash(password)