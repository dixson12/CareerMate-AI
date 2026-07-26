from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.document_service import validate_file, save_file, extract_text

router = APIRouter()

# Simple in-memory store for now — swap for a database in a later sprint
resume_store: dict[str, str] = {}


@router.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):
    content = await file.read()

    is_valid, error_message = validate_file(file.filename, len(content))
    if not is_valid:
        raise HTTPException(status_code=400, detail=error_message)

    file_path = save_file(file.filename, content)

    try:
        extracted_text = extract_text(file_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to extract text: {str(e)}")

    # Store resume text keyed by filename (simple approach for now)
    resume_store[file.filename] = extracted_text

    return {
        "filename": file.filename,
        "text_length": len(extracted_text),
        "message": "Resume uploaded successfully. Ready for analysis."
    }