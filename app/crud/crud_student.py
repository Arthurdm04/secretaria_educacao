# app/crud/crud_student.py
from app.crud.base import CRUDBase
from app.db import models
from app.schemas import student

# Instanciamos a classe base com o modelo e os schemas de Aluno.
# Não precisamos de métodos customizados por enquanto.
crud_student = CRUDBase(models.Student)