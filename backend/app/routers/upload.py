from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.document_service import validate_file, save_file_to_blob, extract_text_from_bytes
from app.services.rag_service import add_document_to_store

router = APIRouter()


@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    content = await file.read()

    is_valid, error_message = validate_file(file.filename, len(content))
    if not is_valid:
        raise HTTPException(status_code=400, detail=error_message)

    save_file_to_blob(file.filename, content, container_name="documents")

    try:
        extracted_text = extract_text_from_bytes(file.filename, content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to extract text: {str(e)}")

    chunk_count = add_document_to_store(file.filename, extracted_text)

    return {
        "filename": file.filename,
        "size_bytes": len(content),
        "text_preview": extracted_text[:300],
        "text_length": len(extracted_text),
        "chunks_stored": chunk_count
    }