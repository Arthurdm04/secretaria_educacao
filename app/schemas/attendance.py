# app/schemas/attendance.py
from pydantic import BaseModel
from datetime import date
from typing import List

class AttendanceStudent(BaseModel):
    student_id: int
    present: bool

class AttendanceRecord(BaseModel):
    record_date: date
    attendances: List[AttendanceStudent]