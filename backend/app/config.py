from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "CareerMate AI"
    gemini_api_key: str = ""
    chroma_persist_dir: str = "./chroma_db"
    embedding_model: str = "all-MiniLM-L6-v2"
    llm_model: str = "gemini-2.5-flash"

    class Config:
        env_file = ".env"

settings = Settings()