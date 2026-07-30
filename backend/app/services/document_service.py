import os
from pathlib import Path
from pypdf import PdfReader
from docx import Document
from io import BytesIO
from app.services.blob_service import upload_blob, download_blob

ALLOWED_EXTENSIONS = {".pdf", ".docx", ".txt"}
MAX_FILE_SIZE_MB = 10


def validate_file(filename: str, file_size: int) -> tuple[bool, str]:
    ext = Path(filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        return False, f"Unsupported file type: {ext}. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
    if file_size > MAX_FILE_SIZE_MB * 1024 * 1024:
        return False, f"File too large. Max size: {MAX_FILE_SIZE_MB}MB"
    return True, ""


def save_file_to_blob(filename: str, content: bytes, container_name: str = "documents") -> str:
    return upload_blob(container_name, filename, content)


def extract_text_from_bytes(filename: str, content: bytes) -> str:
    ext = Path(filename).suffix.lower()

    if ext == ".pdf":
        reader = PdfReader(BytesIO(content))
        return "\n".join(page.extract_text() or "" for page in reader.pages)

    elif ext == ".docx":
        doc = Document(BytesIO(content))
        return "\n".join(para.text for para in doc.paragraphs)

    elif ext == ".txt":
        return content.decode("utf-8")

    else:
        raise ValueError(f"Unsupported file type: {ext}")