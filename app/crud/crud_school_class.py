# app/crud/crud_school_class.py
from app.crud.base import CRUDBase
from app.db import models
from app.schemas import school_class

crud_school_class = CRUDBase(models.SchoolClass)