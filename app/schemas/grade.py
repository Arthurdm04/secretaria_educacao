# app/schemas/grade.py

from pydantic import BaseModel

class GradeBase(BaseModel):
    assessment_name: str
    score: float
    enrollment_id: int

class GradeCreate(GradeBase):
    pass

class Grade(GradeBase):
    id: int

    class Config:
        from_attributes = True