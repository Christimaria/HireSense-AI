"""
HireSense AI — Resume Review Prompts

Two public symbols are consumed by the service layer:
  RESUME_SYSTEM_PROMPT  — the immutable system context for Gemini
  build_resume_review_prompt(resume_text, target_role) → str
"""

RESUME_SYSTEM_PROMPT = """\
You are an expert technical recruiter and career coach with 15+ years of experience
reviewing resumes for top technology companies. You have deep knowledge of ATS
(Applicant Tracking Systems), hiring practices, and what separates exceptional
candidates from average ones.

Your task is to analyse resumes and return structured, honest, actionable feedback.

RULES:
- Be candid but constructive. Do not inflate scores or hide weaknesses.
- Scores use a 0–10 float scale (e.g. 7.5 is valid).
- ats_score is an integer 0–100 measuring ATS keyword/format compatibility.
- Keep per-section feedback concise: 2–3 sentences, one concrete improvement tip.
- strengths, weaknesses, and recommendations must each have 3–5 items.
- Your entire response must be a single JSON object — no prose outside the JSON.
"""


def build_resume_review_prompt(resume_text: str, target_role: str | None) -> str:
    """
    Construct the user-turn prompt for a resume review.

    Args:
        resume_text: Plain-text content of the candidate's resume.
        target_role: Optional job title the candidate is applying for.

    Returns:
        A formatted prompt string ready to be sent to Gemini.
    """
    role_context = (
        f"The candidate is targeting the role of: **{target_role}**.\n"
        f"Tailor your scoring and feedback with this role in mind."
        if target_role
        else "No specific target role was provided — evaluate the resume on general merit."
    )

    return f"""\
{role_context}

Analyse the resume below and return exactly this JSON structure:

{{
  "overall_score": <float 0-10>,
  "ats_score": <int 0-100>,
  "sections": {{
    "summary":    {{"score": <float>, "feedback": "<string>"}},
    "experience": {{"score": <float>, "feedback": "<string>"}},
    "skills":     {{"score": <float>, "feedback": "<string>"}},
    "education":  {{"score": <float>, "feedback": "<string>"}}
  }},
  "strengths":       ["<string>", ...],
  "weaknesses":      ["<string>", ...],
  "recommendations": ["<string>", ...]
}}

RESUME TEXT:
───────────────────────────────────────
{resume_text}
───────────────────────────────────────

Return ONLY the JSON object. No markdown fences, no extra text.
"""
