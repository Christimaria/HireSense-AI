"""
HireSense AI — Resume Review Prompts
"""

RESUME_SYSTEM_PROMPT = """You are an expert technical recruiter and career coach with 15+ years of experience
reviewing resumes for top technology companies. You have deep knowledge of ATS (Applicant Tracking Systems),
hiring practices, and what makes candidates stand out.

Your task is to analyze resumes and provide structured, actionable feedback.

IMPORTANT RULES:
- Be honest but constructive. Do not sugarcoat weaknesses.
- Always respond with valid JSON matching the specified schema exactly.
- Scores should be on a scale of 0–10 (floats allowed, e.g., 7.5).
- ATS score is an integer 0–100 representing ATS compatibility.
- Keep feedback concise but actionable (2-3 sentences per section).
"""


def build_resume_review_prompt(resume_text: str, target_role: str | None) -> str:
    role_context = f"The candidate is targeting the role of: **{target_role}**." if target_role else \
        "No specific target role was provided — review the resume generally."

    return f"""
{role_context}

Please analyze the following resume and return a JSON object with this EXACT structure:

{{
  "overall_score": <float 0-10>,
  "ats_score": <int 0-100>,
  "sections": {{
    "summary": {{ "score": <float>, "feedback": "<string>" }},
    "experience": {{ "score": <float>, "feedback": "<string>" }},
    "skills": {{ "score": <float>, "feedback": "<string>" }},
    "education": {{ "score": <float>, "feedback": "<string>" }}
  }},
  "strengths": ["<string>", ...],
  "weaknesses": ["<string>", ...],
  "recommendations": ["<string>", ...]
}}

Provide 3-5 items for strengths, weaknesses, and recommendations each.

RESUME TEXT:
---
{resume_text}
---

Return only the JSON object. No markdown, no explanation outside the JSON.
"""
