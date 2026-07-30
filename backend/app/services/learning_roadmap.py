import json
from google import genai
from app.config import settings

client = genai.Client(api_key=settings.gemini_api_key)

ROADMAP_PROMPT = """You are a career learning coach. Based on the missing skills below (gaps between a candidate's resume and a target job), create a realistic, prioritized learning roadmap.

IMPORTANT: Prioritize skills by likely impact and learning difficulty. Keep the plan realistic — don't claim someone can master a complex skill in a few days. If a skill genuinely requires more than a few weeks to become job-ready in, say so honestly rather than compressing the timeline to fit a clean weekly structure.

Return ONLY valid JSON in this exact format, with no markdown formatting, no code fences, no extra text:
{{
  "roadmap": [
    {{"week": 1, "focus": "skill name", "goal": "specific learning goal for this week", "suggested_resources": ["resource type, e.g. 'Official documentation', 'freeCodeCamp course'"]}}
  ],
  "priority_order_reasoning": "1-2 sentences explaining why skills were ordered this way"
}}

Missing technical skills: {missing_skills}
Missing soft skills: {missing_soft_skills}
"""


def generate_roadmap(missing_skills: list[str], missing_soft_skills: list[str]) -> dict:
    prompt = ROADMAP_PROMPT.format(
        missing_skills=", ".join(missing_skills) if missing_skills else "None",
        missing_soft_skills=", ".join(missing_soft_skills) if missing_soft_skills else "None"
    )

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
        return {"error": "Failed to generate roadmap", "raw_output": raw_output}