from azure.storage.blob import BlobServiceClient
from app.config import settings

blob_service_client = BlobServiceClient.from_connection_string(
    settings.azure_storage_connection_string
)


def upload_blob(container_name: str, filename: str, content: bytes) -> str:
    container_client = blob_service_client.get_container_client(container_name)
    blob_client = container_client.get_blob_client(filename)
    blob_client.upload_blob(content, overwrite=True)
    return blob_client.url


def download_blob(container_name: str, filename: str) -> bytes:
    container_client = blob_service_client.get_container_client(container_name)
    blob_client = container_client.get_blob_client(filename)
    return blob_client.download_blob().readall()


def blob_exists(container_name: str, filename: str) -> bool:
    container_client = blob_service_client.get_container_client(container_name)
    blob_client = container_client.get_blob_client(filename)
    return blob_client.exists()
def list_blobs(container_name: str) -> list[str]:
    container_client = blob_service_client.get_container_client(container_name)
    return [blob.name for blob in container_client.list_blobs()]


def delete_blob(container_name: str, filename: str) -> bool:
    container_client = blob_service_client.get_container_client(container_name)
    blob_client = container_client.get_blob_client(filename)
    if blob_client.exists():
        blob_client.delete_blob()
        return True
    return False