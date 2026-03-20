from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables and a .env file.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Database
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/notes_rag"

    # Notes
    NOTES_DIR: str = "/path/to/your/files"

    # Embedding model
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"

    # Ollama
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "llama3.2"

    # RAG parameters
    CHUNK_SIZE: int = 512
    CHUNK_OVERLAP: int = 64
    TOP_K: int = 5


settings = Settings()
