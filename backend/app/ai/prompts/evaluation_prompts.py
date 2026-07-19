"""
HireSense AI — Interview Evaluation Prompts

Defines the system context and prompt builder for grading candidate responses.
"""

from app.ai.prompts.interview_prompts import ROLE_CONTEXT, INTERVIEW_TYPE_CONTEXT, EXPERIENCE_CONTEXT

EVALUATION_SYSTEM_PROMPT = """\
You are an expert technical recruiter, senior engineering manager, and career coach with 15+ years of experience conducting interviews for top technology companies.
Your task is to review a candidate's answer to an interview question, grade it constructively and strictly, and provide actionable improvement advice.

RULES:
- Be realistic and fair. Do not inflate scores.
- High scores (e.g. 8.5+) should only be given to answers that are technically accurate, structurally sound, clear, and context-appropriate.
- Low scores (e.g. <5.0) are appropriate for answers with major technical gaps, misunderstandings, or excessive vagueness.
- Grading must scale according to the candidate's Experience Level:
  - Freshers: Expect foundation concepts, basic code mechanics, and enthusiasm.
  - Seniors: Expect architecture-level thinking, trade-off analysis, edge-cases, and leadership.
- Your entire response must be a single JSON object matching the requested structure.
- Do NOT include markdown formatting or HTML outside the JSON block. Return ONLY the JSON object.
"""


def build_evaluation_prompt(
    question: str,
    answer: str,
    role: str,
    experience_level: str,
    interview_type: str,
) -> str:
    """
    Construct the user prompt instructing Gemini to analyze the candidate's answer.

    Args:
        question: The interview question that was asked.
        answer: The candidate's response.
        role: Targeted job role.
        experience_level: Seniority level.
        interview_type: Focus type of the interview.

    Returns:
        A formatted user prompt.
    """
    role_ctx = ROLE_CONTEXT.get(role, role)
    type_ctx = INTERVIEW_TYPE_CONTEXT.get(interview_type, "")
    exp_ctx = EXPERIENCE_CONTEXT.get(experience_level, experience_level)

    return f"""\
Interview Context:
- Role: {role}
- Experience Level: {experience_level} ({exp_ctx})
- Interview Type: {interview_type}
- Key Topics for Role: {role_ctx}
- Interview Style: {type_ctx}

Question Asked:
"{question}"

Candidate's Answer:
"{answer}"

Evaluate the candidate's answer and return exactly this JSON structure:
{{
  "score": <float between 0.0 and 10.0 representing the quality of the answer>,
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
  "improved_answer": "<a model answer tailored to the candidate's role and experience level that is technically precise, thorough, and structured>",
  "tips": [
    "<tip 1>",
    "<tip 2>",
    "<tip 3>"
  ]
}}

Return ONLY the JSON object. No markdown fences, no backticks, no markdown formatting outside of JSON string fields.
"""
