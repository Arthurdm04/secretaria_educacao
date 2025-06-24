# app/core/config.py

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    DATABASE_URL: str

    GEMINI_API_KEY: str | None = None  # Definindo como opcional

    # ✅ Variáveis usadas no LangChain com Azure OpenAI
    azure_openai_api_key: str
    azure_openai_endpoint: str
    azure_openai_deployment_name: str
    azure_openai_api_version: str
    azure_openai_deployment_name_embeddings: str
    azure_openai_api_version_embeddings: str

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'
        # extra = "forbid"  # pode deixar implícito (default do pydantic)

# Instância global
settings = Settings()
