import json
from google import genai
from app.config import settings

client = genai.Client(api_key=settings.gemini_api_key)

SKILL_EXTRACTION_PROMPT = """You are a skill extraction engine. Analyze the resume text below and identify ALL skills, including:
- Skills explicitly listed in a Skills section
- Skills implied by experience or project descriptions (e.g. "built a dashboard in Power BI" implies Power BI)

Return ONLY valid JSON in this exact format, with no markdown formatting, no code fences, no extra text:
{{
  "technical_skills": ["string", "string"],
  "soft_skills": ["string", "string"],
  "tools_and_platforms": ["string", "string"]
}}

Resume text:
{resume_text}
"""


def extract_skills(resume_text: str) -> dict:
    prompt = SKILL_EXTRACTION_PROMPT.format(resume_text=resume_text)

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
        return {"error": "Failed to extract skills", "raw_output": raw_output}