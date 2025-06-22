# app/schemas/student.py
from pydantic import BaseModel
from datetime import date

class StudentBase(BaseModel):
    full_name: str
    birth_date: date | None = None

class StudentCreate(StudentBase):
    pass

class StudentUpdate(StudentBase):
    pass

class Student(StudentBase):
    id: int

    class Config:
        from_attributes = True