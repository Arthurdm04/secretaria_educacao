# app/api/endpoints/classes.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.api import deps
from app.db import models
from app.schemas import school_class, enrollment, grade, attendance # Supondo que esses schemas existem

router = APIRouter()

# --- TURMAS ---

@router.post("/", response_model=school_class.SchoolClass, status_code=201)
def create_school_class(
    *,
    db: Session = Depends(deps.get_db),
    class_in: school_class.SchoolClassCreate,
    current_user: models.User = Depends(deps.get_current_coordinator_or_admin)
):
    """
    Cria uma nova turma.
    Acesso: Coordenador, Admin
    """
    # ... (lógica para chamar o crud_class.create)
    return new_class

@router.get("/", response_model=List[school_class.SchoolClass])
def read_school_classes(db: Session = Depends(deps.get_db)):
    """
    Lista todas as turmas.
    Acesso: Qualquer usuário logado
    """
    # ... (lógica para listar turmas)
    return classes

# --- MATRÍCULAS ---

@router.post("/{class_id}/enrollments", response_model=enrollment.Enrollment)
def enroll_student_in_class(
    class_id: int,
    *,
    db: Session = Depends(deps.get_db),
    enrollment_in: enrollment.EnrollmentCreate,
    current_user: models.User = Depends(deps.get_current_coordinator_or_admin)
):
    """
    Matricula um aluno em uma turma.
    O sistema deve garantir que o aluno não seja matriculado duas vezes.
    Acesso: Coordenador, Admin
    """
    # ... (lógica para criar a matrícula, tratando a exceção de duplicidade)
    # Lembre-se de verificar se enrollment_in.student_id e class_id existem
    return new_enrollment

# --- PRESENÇA ---

@router.post("/{class_id}/attendances", status_code=status.HTTP_201_CREATED)
def record_attendance(
    class_id: int,
    *,
    db: Session = Depends(deps.get_db),
    attendance_in: attendance.AttendanceRecord, # Schema com data e lista de {student_id, present}
    current_user: models.User = Depends(deps.get_current_teacher_or_higher) # Acesso para professor
):
    """
    Registra a presença dos alunos de uma turma em uma data específica.
    Acesso: Professor da turma, Coordenador, Admin
    """
    # ... (lógica para percorrer a lista de alunos e salvar a presença)
    # Validar se o current_user é o professor da turma class_id
    return {"message": "Attendance recorded successfully"}

# --- NOTAS ---

@router.post("/enrollments/{enrollment_id}/grades", response_model=grade.Grade)
def post_grade_for_student(
    enrollment_id: int,
    *,
    db: Session = Depends(deps.get_db),
    grade_in: grade.GradeCreate,
    current_user: models.User = Depends(deps.get_current_teacher_or_higher)
):
    """
    Lança uma nota para um aluno em uma avaliação.
    Acesso: Professor da turma, Coordenador, Admin
    """
    # ... (lógica para lançar a nota vinculada à matrícula)
    return new_grade

# --- RELATÓRIOS ---

@router.get("/{class_id}/reports/attendance")
def get_attendance_report(class_id: int, db: Session = Depends(deps.get_db)):
    """
    Consulta o relatório de frequência de uma turma.
    Acesso: Professor da turma, Coordenador, Admin
    """
    # ... (lógica para gerar o relatório)
    return report_data

@router.get("/students/{student_id}/reports/performance")
def get_performance_report(student_id: int, db: Session = Depends(deps.get_db)):
    """
    Consulta o relatório de desempenho (notas) de um aluno.
    Acesso: Professor, Coordenador, Admin (e talvez pais no futuro)
    """
    # ... (lógica para gerar o relatório)
    return report_data