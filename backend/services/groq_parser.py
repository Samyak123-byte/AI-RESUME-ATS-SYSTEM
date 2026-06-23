import os
import json
import logging
from typing import Dict, Optional

from groq import Groq

# ==========================================================
# Logging
# ==========================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger("ats_resume_scorer")

# ==========================================================
# Configuration
# ==========================================================

GROQ_MODEL = "llama-3.3-70b-versatile"

_client = None

# ==========================================================
# Client
# ==========================================================

def _get_client() -> Groq:
    global _client

    if _client is None:
        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            raise ValueError(
                "GROQ_API_KEY environment variable not set"
            )

        _client = Groq(api_key=api_key)

    return _client


# ==========================================================
# Resume Prompts
# ==========================================================

RESUME_SYSTEM_PROMPT = (
    "You are a resume parser. "
    "Extract information from the resume and return ONLY a valid JSON object."
)

RESUME_USER_PROMPT = """
Extract the following from this resume and return as JSON:

{{
  "name": "full name",
  "email": "email address",
  "phone": "phone number",
  "linkedin": "LinkedIn URL if present, otherwise null",
  "github": "GitHub URL if present, otherwise null",
  "professional_summary": "full summary text",
  "skills": ["list", "of", "skills"],
  "experience": [
    {{
      "job_title": "",
      "company": "",
      "start_date": "",
      "end_date": "",
      "duration_months": 0,
      "description": ""
    }}
  ],
  "education": [
    {{
      "degree": "",
      "institution": "",
      "year": ""
    }}
  ],
  "certifications": ["list"],
  "projects": [
    {{
      "title": "",
      "description": "",
      "technologies": []
    }}
  ],
  "action_verbs": [],
  "keywords": []
}}

Rules:
- Return ONLY valid JSON.
- No markdown.
- No explanation.
- Calculate duration_months.
- Extract all skills.
- Extract ATS keywords.

Resume Text:

{raw_text}
"""

# ==========================================================
# JD Prompts
# ==========================================================

JD_SYSTEM_PROMPT = (
    "You are a job description parser. "
    "Return ONLY valid JSON."
)

JD_USER_PROMPT = """
Extract the following from this job description:

{{
  "job_title": "",
  "required_skills": [],
  "preferred_skills": [],
  "experience_required": "",
  "education_required": "",
  "key_responsibilities": [],
  "keywords": []
}}

Return ONLY valid JSON.

Job Description:

{raw_text}
"""

# ==========================================================
# Groq Call
# ==========================================================

def _call_groq(
    client: Groq,
    system_prompt: str,
    user_prompt: str
) -> str:

    try:
        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ],
            temperature=0,
            max_tokens=4096
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        logger.exception("Groq API error")
        raise RuntimeError(f"Groq request failed: {e}")


# ==========================================================
# JSON Parsing
# ==========================================================

def _try_parse_json(text: str) -> Optional[dict]:

    if not text:
        return None

    cleaned = text.strip()

    # Remove markdown fences
    if cleaned.startswith("```"):

        first_newline = cleaned.find("\n")

        if first_newline != -1:
            cleaned = cleaned[first_newline + 1:]

        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]

        cleaned = cleaned.strip()

    try:
        return json.loads(cleaned)

    except json.JSONDecodeError:
        pass

    # Try extracting JSON object
    start = cleaned.find("{")
    end = cleaned.rfind("}")

    if start != -1 and end != -1:

        candidate = cleaned[start:end + 1]

        try:
            return json.loads(candidate)

        except json.JSONDecodeError:
            pass

    return None


# ==========================================================
# Resume Parsing
# ==========================================================

def parse_resume(raw_text: str) -> Dict:

    client = _get_client()

    prompt = RESUME_USER_PROMPT.format(
        raw_text=raw_text
    )

    raw_response = _call_groq(
        client,
        RESUME_SYSTEM_PROMPT,
        prompt
    )

    result = _try_parse_json(raw_response)

    if result is not None:
        return _validate_resume_result(result)

    logger.warning(
        "Resume parse returned invalid JSON. Retrying..."
    )

    retry_prompt = (
        "Return ONLY a valid JSON object.\n\n"
        + prompt
    )

    raw_response = _call_groq(
        client,
        RESUME_SYSTEM_PROMPT,
        retry_prompt
    )

    result = _try_parse_json(raw_response)

    if result is not None:
        return _validate_resume_result(result)

    raise ValueError(
        f"Unable to parse Groq response:\n{raw_response[:500]}"
    )


# ==========================================================
# JD Parsing
# ==========================================================

def parse_job_description(raw_text: str) -> Dict:

    client = _get_client()

    prompt = JD_USER_PROMPT.format(
        raw_text=raw_text
    )

    raw_response = _call_groq(
        client,
        JD_SYSTEM_PROMPT,
        prompt
    )

    result = _try_parse_json(raw_response)

    if result is not None:
        return _validate_jd_result(result)

    logger.warning(
        "JD parse returned invalid JSON. Retrying..."
    )

    retry_prompt = (
        "Return ONLY a valid JSON object.\n\n"
        + prompt
    )

    raw_response = _call_groq(
        client,
        JD_SYSTEM_PROMPT,
        retry_prompt
    )

    result = _try_parse_json(raw_response)

    if result is not None:
        return _validate_jd_result(result)

    raise ValueError(
        f"Unable to parse Groq response:\n{raw_response[:500]}"
    )


# ==========================================================
# JD Validation
# ==========================================================

def _validate_jd_result(
    result: Optional[dict]
) -> dict:

    if result is None:
        result = {}

    defaults = {
        "job_title": "",
        "required_skills": [],
        "preferred_skills": [],
        "experience_required": "",
        "education_required": "",
        "key_responsibilities": [],
        "keywords": [],
    }

    for key, default in defaults.items():

        if key not in result or result[key] is None:
            result[key] = default

        if isinstance(default, list) and not isinstance(result[key], list):
            result[key] = default

    return result


# ==========================================================
# Resume Validation
# ==========================================================

def _validate_resume_result(
    result: Optional[dict]
) -> dict:

    if result is None:
        result = {}

    defaults = {
        "name": "",
        "email": None,
        "phone": None,
        "linkedin": None,
        "github": None,
        "professional_summary": "",
        "skills": [],
        "experience": [],
        "education": [],
        "certifications": [],
        "projects": [],
        "action_verbs": [],
        "keywords": [],
    }

    for key, default in defaults.items():

        if key not in result or result[key] is None:
            result[key] = default

        if isinstance(default, list) and not isinstance(result[key], list):
            result[key] = default

    if not isinstance(result["experience"], list):
        result["experience"] = []

    for exp in result["experience"]:

        if not isinstance(exp, dict):
            continue

        exp.setdefault("job_title", "")
        exp.setdefault("company", "")
        exp.setdefault("start_date", "")
        exp.setdefault("end_date", "")
        exp.setdefault("duration_months", 0)
        exp.setdefault("description", "")

        try:
            exp["duration_months"] = int(
                exp["duration_months"]
            )
        except (TypeError, ValueError):
            exp["duration_months"] = 0

    if not isinstance(result["projects"], list):
        result["projects"] = []

    for proj in result["projects"]:

        if not isinstance(proj, dict):
            continue

        proj.setdefault("title", "")
        proj.setdefault("description", "")
        proj.setdefault("technologies", [])

        if not isinstance(proj["technologies"], list):
            proj["technologies"] = []

    return result