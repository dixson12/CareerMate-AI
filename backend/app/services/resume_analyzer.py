import json
from google import genai
from app.config import settings

client = genai.Client(api_key=settings.gemini_api_key)

ANALYSIS_PROMPT = """You are an expert resume reviewer. Analyze the resume text below and provide constructive, specific feedback.

Return ONLY valid JSON in this exact format, with no markdown formatting, no code fences, no extra text:
{{
  "overall_score": <integer 0-100>,
  "summary": "2-3 sentence overall assessment",
  "strengths": ["string", "string"],
  "weaknesses": ["string", "string"],
  "bullet_point_improvements": [
    {{"original": "the weak bullet point as written", "improved": "a stronger, quantified rewrite"}}
  ],
  "formatting_notes": ["string"]
}}

Focus on: quantifiable achievements, action verbs, clarity, and relevance for the roles this resume targets.
Identify at most 3-5 bullet points that could be improved with rewrites.

Resume text:
{resume_text}
"""


def analyze_resume(resume_text: str) -> dict:
    prompt = ANALYSIS_PROMPT.format(resume_text=resume_text)

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
        return {"error": "Failed to analyze resume", "raw_output": raw_output}