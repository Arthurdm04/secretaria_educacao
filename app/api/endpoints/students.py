# app/api/endpoints/students.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.api import deps
from app.crud import crud_student
from app.db import models
from app.schemas import student

router = APIRouter()

@router.post("/", response_model=student.Student, status_code=201)
def create_student(
    *,
    db: Session = Depends(deps.get_db),
    student_in: student.StudentCreate,
    current_user: models.User = Depends(deps.get_current_coordinator_or_admin) # Exemplo de permissão
):
    """
    Cadastra um novo aluno.
    Acesso: Coordenador, Admin
    """
    # ... (lógica para chamar o crud_student.create)
    return created_student

@router.get("/", response_model=List[student.Student])
def read_students(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user)
):
    """
    Lista todos os alunos (com paginação).
    Acesso: Qualquer usuário logado
    """
    students = crud_student.get_multi(db, skip=skip, limit=limit)
    return students

@router.get("/{student_id}", response_model=student.Student)
def read_student(
    student_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user)
):
    """
    Busca um aluno pelo ID.
    Acesso: Qualquer usuário logado
    """
    db_student = crud_student.get(db, id=student_id)
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return db_student