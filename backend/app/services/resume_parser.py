import json
from google import genai
from app.config import settings

client = genai.Client(api_key=settings.gemini_api_key)

PARSE_PROMPT = """You are a resume parser. Extract structured information from the resume text below.

Return ONLY valid JSON in this exact format, with no markdown formatting, no code fences, no extra text:
{{
  "name": "string or null",
  "email": "string or null",
  "education": [
    {{"degree": "string", "institution": "string", "year": "string or null"}}
  ],
  "experience": [
    {{"title": "string", "company": "string", "duration": "string or null", "description": "string"}}
  ],
  "skills": ["string", "string"],
  "projects": [
    {{"name": "string", "description": "string"}}
  ]
}}

Resume text:
{resume_text}
"""


def parse_resume(resume_text: str) -> dict:
    prompt = PARSE_PROMPT.format(resume_text=resume_text)

    response = client.models.generate_content(
        model=settings.llm_model,
        contents=prompt,
    )

    raw_output = response.text.strip()

    # Gemini sometimes wraps JSON in markdown code fences despite instructions — strip if present
    if raw_output.startswith("```"):
        raw_output = raw_output.split("```")[1]
        if raw_output.startswith("json"):
            raw_output = raw_output[4:]
        raw_output = raw_output.strip()

    try:
        return json.loads(raw_output)
    except json.JSONDecodeError:
        return {"error": "Failed to parse resume structure", "raw_output": raw_output}