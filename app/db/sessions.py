from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# Cria o "motor" do SQLAlchemy que se conectará ao seu MySQL.
# `pool_pre_ping=True` verifica as conexões antes de usá-las, o que ajuda a evitar
# erros com conexões que foram fechadas pelo servidor do banco de dados.
engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)

# Cria uma fábrica de sessões. Cada instância de SessionLocal será uma
# nova sessão do banco de dados.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)