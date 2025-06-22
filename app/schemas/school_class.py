# app/schemas/school_class.py

from pydantic import BaseModel

class SchoolClassBase(BaseModel):
    name: str
    year: int
    teacher_id: int | None = None

class SchoolClassCreate(SchoolClassBase):
    pass

class SchoolClassUpdate(BaseModel):
    name: str | None = None
    year: int | None = None
    teacher_id: int | None = None

class SchoolClass(SchoolClassBase):
    id: int
    
    # Configuração para permitir que o Pydantic leia dados de um objeto do SQLAlchemy
    class Config:
        from_attributes = True