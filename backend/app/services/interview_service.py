import json
from google import genai
from app.config import settings

client = genai.Client(api_key=settings.gemini_api_key)

INTERVIEW_PROMPT = """You are an interview preparation coach. Based on the candidate's resume and their target role below, generate realistic interview questions they're likely to face.

IMPORTANT: Base technical questions on the actual skills and experience mentioned in the resume. Do not assume expertise the candidate hasn't demonstrated.

Return ONLY valid JSON in this exact format, with no markdown formatting, no code fences, no extra text:
{{
  "behavioral_questions": ["string", "string", "string"],
  "technical_questions": ["string", "string", "string"],
  "questions_about_gaps": ["string", "string"],
  "tips": ["string", "string"]
}}

"behavioral_questions" — general STAR-format questions (teamwork, conflict, leadership, etc.)
"technical_questions" — specific to the skills/tools mentioned in the resume and relevant to the target role
"questions_about_gaps" — questions an interviewer might ask about weaknesses or missing experience for this role
"tips" — 2-3 practical tips for this candidate specifically, based on their background

Resume text:
{resume_text}

Target Role: {target_role}
"""


def generate_interview_prep(resume_text: str, target_role: str) -> dict:
    prompt = INTERVIEW_PROMPT.format(resume_text=resume_text, target_role=target_role)

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
        return {"error": "Failed to generate interview prep", "raw_output": raw_output}