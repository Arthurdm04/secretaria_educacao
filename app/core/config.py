# app/core/config.py

import os
from pydantic_settings import BaseSettings

# app/core/config.py
class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    DATABASE_URL: str

    # ADICIONE ESTA LINHA
    GEMINI_API_KEY: str | None = None # Definindo como opcional

    class Config:
        # ...
        # Pede para o Pydantic ler as variáveis de um arquivo .env
        env_file = ".env"
        env_file_encoding = 'utf-8'

# Cria uma instância única das configurações que será usada em toda a aplicação
settings = Settings()