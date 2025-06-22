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
    # Apenas Admins podem criar novos usuários
    current_user: models.User = Depends(deps.get_current_admin_user)
):
    """
    Cria um novo usuário no sistema (Professor, Coordenador, Admin).
    Acesso: Admin
    """
    # ... (lógica para chamar o crud_user.create)
    return created_user

@router.get("/me", response_model=user.User)
def read_user_me(
    current_user: models.User = Depends(deps.get_current_active_user)
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