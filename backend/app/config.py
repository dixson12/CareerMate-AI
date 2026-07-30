from pydantic_settings import BaseSettings
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import os


class Settings(BaseSettings):
    app_name: str = "CareerMate AI"
    chroma_persist_dir: str = "./chroma_db"
    embedding_model: str = "all-MiniLM-L6-v2"
    llm_model: str = "gemini-2.5-flash"
    key_vault_url: str = ""

    gemini_api_key: str = ""
    azure_storage_connection_string: str = ""

    class Config:
        env_file = ".env"

    def load_secrets_from_vault(self):
        """Fetch secrets from Azure Key Vault, overriding any local .env values."""
        if not self.key_vault_url:
            return  # No vault configured — fall back to .env (local dev without Key Vault)

        credential = DefaultAzureCredential()
        client = SecretClient(vault_url=self.key_vault_url, credential=credential)

        self.gemini_api_key = client.get_secret("gemini-api-key").value
        self.azure_storage_connection_string = client.get_secret("azure-storage-connection-string").value


settings = Settings()
settings.load_secrets_from_vault()