# app/schemas/enrollment.py

from pydantic import BaseModel
from datetime import date
from .student import Student  # Importa o schema do aluno para aninhar dados

class EnrollmentBase(BaseModel):
    student_id: int
    class_id: int

class EnrollmentCreate(EnrollmentBase):
    pass

class Enrollment(EnrollmentBase):
    id: int
    enrollment_date: date
    student: Student # Aninha os dados do aluno na resposta

    class Config:
        from_attributes = True