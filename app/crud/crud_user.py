# app/crud/crud_user.py
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.db import models
from app.schemas import user
from app.core.security import get_password_hash, verify_password

class CRUDUser(CRUDBase[models.User, user.UserCreate, user.UserUpdate]):
    def get_by_email(self, db: Session, *, email: str) -> models.User | None:
        return db.query(self.model).filter(models.User.email == email).first()

    def create(self, db: Session, *, obj_in: user.UserCreate) -> models.User:
        # Sobrescrevemos o método create para hashear a senha
        hashed_password = get_password_hash(obj_in.password)
        db_obj = models.User(
            email=obj_in.email,
            full_name=obj_in.full_name,
            hashed_password=hashed_password,
            role=obj_in.role,
            is_active=obj_in.is_active
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def authenticate(
        self, db: Session, *, email: str, password: str
    ) -> models.User | None:
        user = self.get_by_email(db, email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

# Instancia a classe para ser usada nas dependências
crud_user = CRUDUser(models.User)