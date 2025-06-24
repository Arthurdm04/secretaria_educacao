# app/api/endpoints/users.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.api import deps
from app.crud import crud_user
from app.db import models
from app.schemas import user

router = APIRouter()

@router.post("/", response_model=user.User, status_code=201)
def create_user(
    *,
    db: Session = Depends(deps.get_db),
    user_in: user.UserCreate,
    current_user: models.User = Depends(deps.get_current_admin_user)
    # Apenas Admins podem criar novos usuários
):
    """
    Cria um novo usuário no sistema (Professor, Coordenador, Admin).
    Acesso: Admin
    """
    # 1. Verifica se já existe um usuário com o mesmo e-mail
    existing_user = crud_user.get_by_email(db, email=user_in.email)
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Já existe um usuário com este e-mail no sistema.",
        )
    
    # 2. Chama a função do CRUD para criar o usuário
    created_user = crud_user.create(db=db, user_in=user_in)
    
    # 3. Retorna o usuário recém-criado
    return created_user

@router.get("/me", response_model=user.User)
def read_user_me(
    current_user: models.User = Depends(deps.get_current_user)
):
    """
    Retorna os dados do usuário logado.
    Acesso: Qualquer usuário logado
    """
    return current_user

@router.get("/{user_id}", response_model=user.User)
def read_user_by_id(
    user_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_admin_user)
):
    """
    Retorna os dados de um usuário específico pelo ID.
    Acesso: Admin
    """
    user = crud_user.get(db, id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user