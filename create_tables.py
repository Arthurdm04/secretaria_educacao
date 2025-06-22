# create_tables.py

# Este script deve ser executado uma única vez para criar as tabelas no banco.

from app.db.sessions import engine
from app.db.base import Base
# Importe aqui TODOS os seus modelos para que o SQLAlchemy saiba sobre eles
from app.db import models

print("Criando tabelas no banco de dados...")

# Este comando mágico lê todos os modelos que herdaram de `Base` e os cria no banco
# de dados que está configurado no `engine`.
Base.metadata.create_all(bind=engine)

print("Tabelas criadas com sucesso!")

# NOTA: Para projetos em produção ou que evoluem muito, usa-se uma ferramenta de
# "migrations" como o Alembic para gerenciar alterações no banco de dados.
# Para este projeto, este script é mais do que suficiente.