# app/db/models.py
import enum
import datetime

from sqlalchemy import (Column, Integer, String, Boolean, Date, ForeignKey,
                        Enum, UniqueConstraint, Float)
from sqlalchemy.orm import relationship
from .base import Base

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    COORDINATOR = "coordinator"
    TEACHER = "teacher"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    # MODIFIQUE AQUI
    full_name = Column(String(255), index=True)
    # E AQUI
    email = Column(String(255), unique=True, index=True, nullable=False)
    # E AQUI (Senhas hasheadas podem ser longas)
    hashed_password = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), nullable=False)
    is_active = Column(Boolean, default=True)

class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, index=True)
    # MODIFIQUE AQUI
    full_name = Column(String(255), index=True)
    birth_date = Column(Date)

class Teacher(Base):
    __tablename__ = "teachers"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User")

class SchoolClass(Base): # Turma
    __tablename__ = "school_classes"
    id = Column(Integer, primary_key=True, index=True)
    # MODIFIQUE AQUI
    name = Column(String(255), index=True) # Ex: "3º Ano A"
    year = Column(Integer)
    teacher_id = Column(Integer, ForeignKey("teachers.id"))
    teacher = relationship("Teacher")
    enrollments = relationship("Enrollment", back_populates="school_class")

class Enrollment(Base): # Matrícula
    __tablename__ = "enrollments"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    class_id = Column(Integer, ForeignKey("school_classes.id"), nullable=False)
    enrollment_date = Column(Date, default=datetime.datetime.utcnow) # Pequena correção aqui: datetime.datetime

    student = relationship("Student")
    school_class = relationship("SchoolClass", back_populates="enrollments")

    __table_args__ = (UniqueConstraint('student_id', 'class_id', name='_student_class_uc'),)

class Attendance(Base):
    __tablename__ = "attendances"
    id = Column(Integer, primary_key=True)
    enrollment_id = Column(Integer, ForeignKey("enrollments.id"))
    date = Column(Date, nullable=False)
    present = Column(Boolean, default=True)
    enrollment = relationship("Enrollment")

class Grade(Base):
    __tablename__ = "grades"
    id = Column(Integer, primary_key=True)
    enrollment_id = Column(Integer, ForeignKey("enrollments.id"))
    # MODIFIQUE AQUI
    assessment_name = Column(String(255)) # Ex: "Prova 1", "Trabalho de Ciências"
    score = Column(Float)
    enrollment = relationship("Enrollment")

# ... adicione o tamanho a qualquer outra coluna String que você possa ter.