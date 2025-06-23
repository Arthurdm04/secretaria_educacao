# app/api/endpoints/login.py
# VERSÃO CORRIGIDA E LIMPA

from datetime import timedelta
from fastapi import APIRouter, Depends, Form, HTTPException, status
from sqlalchemy.orm import Session
import logging

# Organizando os imports da sua aplicação
from app.api import deps
from app.core import security
# Importando a instância 'crud_user' diretamente do seu arquivo CRUD de usuário
from app.crud.crud_user import crud_user 
# Importando os schemas necessários com apelidos claros
from app.schemas import user as user_schema
from app.schemas import token as token_schema


router = APIRouter()

@router.post("/token", response_model=token_schema.Token)
def login_for_access_token(
    db: Session = Depends(deps.get_db),
    username: str | None = Form(default=None),
    password: str | None = Form(default=None)
):
    """
    Obtém um token de acesso JWT.
    Recebe 'username' e 'password' via form-data.
    """
    # Este print AGORA VAI APARECER!
    print("--- ROTA /token ACIONADA ---")

    if not username or not password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Os campos 'username' e 'password' são obrigatórios.",
        )

    user = crud_user.authenticate(db, email=username, password=password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Verifique se a sua função create_access_token está correta (recebendo 'data: dict')
    access_token = security.create_access_token(
        data={"sub": user.email, "role": user.role.value if user.role else None}
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register", response_model=user_schema.User, status_code=status.HTTP_201_CREATED)
def register_user(
    *,
    db: Session = Depends(deps.get_db),
    user_in: user_schema.UserCreate,
):
    """
    Cria um novo usuário no sistema (registro público).
    """
    print(f"Tentativa de registro para o e-mail: {user_in.email}")
    user = crud_user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="Um usuário com este e-mail já existe no sistema.",
        )
    
    new_user = crud_user.create(db=db, obj_in=user_in)
    return new_user