from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "CareerMate AI"
    openai_api_key: str = ""
    chroma_persist_dir: str = "./chroma_db"
    embedding_model: str = "all-MiniLM-L6-v2"
    llm_model: str = "gpt-4o-mini"

    class Config:
        env_file = ".env"

settings = Settings()