import json
from google import genai
from app.config import settings

client = genai.Client(api_key=settings.gemini_api_key)

MATCH_PROMPT = """You are a resume-to-job matching engine. Compare the candidate's resume against the job description below.

Return ONLY valid JSON in this exact format, with no markdown formatting, no code fences, no extra text:
{{
  "overall_match_percentage": <integer 0-100>,
  "summary": "2-3 sentence assessment of fit",
  "matched_skills": ["string", "string"],
  "missing_skills": ["string", "string"],
  "missing_soft_skills": ["string", "string"],
  "recommendation": "1-2 sentence suggestion on how to improve fit for this role"
}}

Resume text:
{resume_text}

Job Description:
{job_description}
"""


def match_resume_to_job(resume_text: str, job_description: str) -> dict:
    prompt = MATCH_PROMPT.format(resume_text=resume_text, job_description=job_description)

    response = client.models.generate_content(
        model=settings.llm_model,
        contents=prompt,
    )

    raw_output = response.text.strip()

    if raw_output.startswith("```"):
        raw_output = raw_output.split("```")[1]
        if raw_output.startswith("json"):
            raw_output = raw_output[4:]
        raw_output = raw_output.strip()

    try:
        return json.loads(raw_output)
    except json.JSONDecodeError:
        return {"error": "Failed to match resume to job", "raw_output": raw_output}