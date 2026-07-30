from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.document_service import validate_file, save_file, extract_text
from app.services.resume_parser import parse_resume
from app.services.skill_extractor import extract_skills
from pydantic import BaseModel
from app.services.job_matcher import match_resume_to_job

from app.services.resume_analyzer import analyze_resume
from app.services.interview_service import generate_interview_prep
from app.services.learning_roadmap import generate_roadmap





router = APIRouter()

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

class InterviewPrepRequest(BaseModel):
    target_role: str


@router.post("/interview-prep/{filename}")
async def interview_prep_endpoint(filename: str, request: InterviewPrepRequest):
    if filename not in resume_store:
        raise HTTPException(status_code=404, detail="Resume not found. Upload it first.")

    if not request.target_role.strip():
        raise HTTPException(status_code=400, detail="Target role cannot be empty")

    prep = generate_interview_prep(resume_store[filename], request.target_role)

    return {"filename": filename, "interview_prep": prep}

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
@router.post("/analyze-resume/{filename}")
async def analyze_resume_endpoint(filename: str):
    if filename not in resume_store:
        raise HTTPException(status_code=404, detail="Resume not found. Upload it first.")

    analysis = analyze_resume(resume_store[filename])

    return {"filename": filename, "analysis": analysis}
# ... existing code ...

class JobMatchRequest(BaseModel):
    job_description: str


@router.post("/match-job/{filename}")
async def match_job_endpoint(filename: str, request: JobMatchRequest):
    if filename not in resume_store:
        raise HTTPException(status_code=404, detail="Resume not found. Upload it first.")

    if not request.job_description.strip():
        raise HTTPException(status_code=400, detail="Job description cannot be empty")

    match_result = match_resume_to_job(resume_store[filename], request.job_description)

    return {"filename": filename, "match": match_result}

resume_store: dict[str, str] = {}
parsed_resume_store: dict[str, dict] = {}


class RoadmapRequest(BaseModel):
    missing_skills: list[str]
    missing_soft_skills: list[str] = []


@router.post("/skill-gap-roadmap")
async def skill_gap_roadmap_endpoint(request: RoadmapRequest):
    if not request.missing_skills and not request.missing_soft_skills:
        raise HTTPException(status_code=400, detail="No missing skills provided")

    roadmap = generate_roadmap(request.missing_skills, request.missing_soft_skills)

    return {"roadmap": roadmap}