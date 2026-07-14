from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.document_service import validate_file, save_file, extract_text

router = APIRouter()


@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    content = await file.read()

    is_valid, error_message = validate_file(file.filename, len(content))
    if not is_valid:
        raise HTTPException(status_code=400, detail=error_message)

    file_path = save_file(file.filename, content)

    try:
        extracted_text = extract_text(file_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to extract text: {str(e)}")

    return {
        "filename": file.filename,
        "size_bytes": len(content),
        "text_preview": extracted_text[:300],  # first 300 chars, just for confirmation
        "text_length": len(extracted_text)
    }