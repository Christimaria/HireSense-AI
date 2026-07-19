"""
HireSense AI — Performance Dashboard Prompts

Defines prompts to analyze the full mock interview session transcript.
"""

from app.ai.prompts.interview_prompts import ROLE_CONTEXT, INTERVIEW_TYPE_CONTEXT, EXPERIENCE_CONTEXT

DASHBOARD_SYSTEM_PROMPT = """\
You are an elite executive recruiter and technical interviewer with 15+ years of experience conducting performance assessments and calibration panels.
Your task is to analyze an entire mock interview transcript (questions and candidate answers) and produce a detailed, honest, structured performance dashboard.

RULES:
- Evaluate the candidate holistically. Look for patterns in technical depth, communication clarity, problem-solving structure, and resilience.
- Scores must be fair, strictly graded, and not artificially inflated.
- Provide a grade (e.g. A, B+, B, C-, F) matching typical industry standards for the specified role and experience level.
- category_scores must cover at least 3-4 distinct criteria relevant to the interview (e.g., Technical Depth, Communication Skills, Problem Solving, Scenario Analysis).
- Each list (strengths, weaknesses, improvement_areas, next_steps) must contain between 3 and 5 high-quality, actionable items.
- Your entire response must be a single JSON object matching the requested structure.
- Do NOT include markdown formatting or prose outside the JSON block. Return ONLY the JSON object.
"""


def build_dashboard_prompt(
    role: str,
    experience_level: str,
    interview_type: str,
    session_turns: list[dict],
) -> str:
    """
    Construct user prompt for generating a mock interview performance dashboard.

    Args:
        role: Targeted job role.
        experience_level: Experience seniority level.
        interview_type: Focus type of the interview.
        session_turns: Serialized list of Q&A conversation turns.

    Returns:
        Formatted user prompt.
    """
    role_ctx = ROLE_CONTEXT.get(role, role)
    type_ctx = INTERVIEW_TYPE_CONTEXT.get(interview_type, "")
    exp_ctx = EXPERIENCE_CONTEXT.get(experience_level, experience_level)

    transcript_lines = []
    for idx, turn in enumerate(session_turns, start=1):
        transcript_lines.append(f"Turn #{idx}:")
        transcript_lines.append(f"  Question Asked: {turn['question']}")
        transcript_lines.append(f"  Candidate Answer: {turn['answer']}")
        transcript_lines.append("")

    transcript_text = "\n".join(transcript_lines)

    return f"""\
Interview Metadata:
- Role: {role}
- Experience Level: {experience_level} ({exp_ctx})
- Interview Type: {interview_type}
- Role Context: {role_ctx}
- Interview Context: {type_ctx}

Mock Interview Transcript:
────────────────────────────────────────────────────────────
{transcript_text}
────────────────────────────────────────────────────────────

Analyze the transcript above and return exactly this JSON structure:
{{
  "overall_score": <float between 0.0 and 10.0 representing overall performance>,
  "category_scores": {{
    "Technical Depth": <float 0.0 to 10.0>,
    "Communication Clarity": <float 0.0 to 10.0>,
    "Problem Solving": <float 0.0 to 10.0>,
    "Context Relevance": <float 0.0 to 10.0>
  }},
  "performance_grade": "<string, e.g. A-, B+, C>",
  "strengths": [
    "<strength 1>",
    "<strength 2>",
    "<strength 3>"
  ],
  "weaknesses": [
    "<weakness 1>",
    "<weakness 2>",
    "<weakness 3>"
  ],
  "improvement_areas": [
    "<improvement area 1>",
    "<improvement area 2>",
    "<improvement area 3>"
  ],
  "interview_readiness": "<a brief summary sentence assessing readiness (e.g., 'Strong candidate; ready for interviews with minor review of database indexing.')>",
  "next_steps": [
    "<actionable roadmap step 1>",
    "<actionable roadmap step 2>",
    "<actionable roadmap step 3>"
  ]
}}

Return ONLY the JSON object. No markdown fences, no backticks, no markdown formatting outside of JSON string fields.
"""
