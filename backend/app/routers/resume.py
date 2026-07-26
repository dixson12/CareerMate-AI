from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.document_service import validate_file, save_file, extract_text
from app.services.resume_parser import parse_resume
from app.services.skill_extractor import extract_skills
router = APIRouter()

resume_store: dict[str, str] = {}
parsed_resume_store: dict[str, dict] = {}


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

    resume_store[file.filename] = extracted_text

    return {
        "filename": file.filename,
        "text_length": len(extracted_text),
        "message": "Resume uploaded successfully. Ready for analysis."
    }


@router.post("/parse-resume/{filename}")
async def parse_resume_endpoint(filename: str):
    if filename not in resume_store:
        raise HTTPException(status_code=404, detail="Resume not found. Upload it first.")

    parsed = parse_resume(resume_store[filename])
    parsed_resume_store[filename] = parsed

    return {"filename": filename, "parsed_data": parsed}


@router.post("/extract-skills/{filename}")
async def extract_skills_endpoint(filename: str):
    if filename not in resume_store:
        raise HTTPException(status_code=404, detail="Resume not found. Upload it first.")

    skills = extract_skills(resume_store[filename])

    return {"filename": filename, "skills": skills}