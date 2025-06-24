# app/core/security.py

from datetime import datetime, timedelta, timezone
from typing import Any
from jose import jwt
from passlib.context import CryptContext

from app.core.config import settings

# Configura o passlib para usar o algoritmo bcrypt para hashear as senhas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ALGORITHM = settings.ALGORITHM

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """
    Cria um novo token de acesso JWT a partir de um dicionário de dados.
    """
    # MUDANÇA 1: Copiamos o dicionário 'data' que recebemos como argumento.
    # Este dicionário já contém o 'sub' e a 'role'.
    to_encode = data.copy()

    # A lógica de expiração continua a mesma
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    # MUDANÇA 2: Adicionamos a data de expiração ao nosso dicionário.
    to_encode.update({"exp": expire})

    # A lógica de encoding continua a mesma
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