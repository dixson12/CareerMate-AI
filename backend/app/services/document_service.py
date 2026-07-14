import os
from pathlib import Path
from pypdf import PdfReader
from docx import Document

UPLOAD_DIR = Path("uploaded_files")
UPLOAD_DIR.mkdir(exist_ok=True)

ALLOWED_EXTENSIONS = {".pdf", ".docx", ".txt"}
MAX_FILE_SIZE_MB = 10


def validate_file(filename: str, file_size: int) -> tuple[bool, str]:
    ext = Path(filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        return False, f"Unsupported file type: {ext}. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
    if file_size > MAX_FILE_SIZE_MB * 1024 * 1024:
        return False, f"File too large. Max size: {MAX_FILE_SIZE_MB}MB"
    return True, ""


def save_file(filename: str, content: bytes) -> Path:
    file_path = UPLOAD_DIR / filename
    with open(file_path, "wb") as f:
        f.write(content)
    return file_path


def extract_text(file_path: Path) -> str:
    ext = file_path.suffix.lower()

    if ext == ".pdf":
        reader = PdfReader(str(file_path))
        return "\n".join(page.extract_text() or "" for page in reader.pages)

    elif ext == ".docx":
        doc = Document(str(file_path))
        return "\n".join(para.text for para in doc.paragraphs)

    elif ext == ".txt":
        return file_path.read_text(encoding="utf-8")

    else:
        raise ValueError(f"Unsupported file type: {ext}")