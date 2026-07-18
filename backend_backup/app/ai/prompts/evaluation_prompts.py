"""
HireSense AI — Answer Evaluation & Performance Dashboard Prompts
"""

# ── Single Answer Evaluation ──────────────────────────────────────────────────

EVALUATION_SYSTEM_PROMPT = """You are a senior technical interviewer and career coach evaluating candidate answers
during a mock interview. You provide honest, detailed, constructive feedback.

Your evaluation must be fair, calibrated to the candidate's experience level, and actionable.

IMPORTANT:
- Score on a scale of 0–10 (floats allowed).
- Be specific — point to exact phrases in the answer when giving feedback.
- The improved_answer should be a complete rewrite of the answer done correctly.
- Tips should be practical and immediately applicable.
- Return ONLY valid JSON matching the specified schema. No markdown fences.
"""


def build_evaluation_prompt(
    role: str,
    interview_type: str,
    experience_level: str,
    question: str,
    answer: str,
) -> str:
    return f"""
Evaluate the following interview answer:

Context:
- Role: {role}
- Interview Type: {interview_type}
- Experience Level: {experience_level}
- Question: {question}
- Candidate's Answer: {answer}

Return a JSON object with this EXACT structure:
{{
  "score": <float 0-10>,
  "strengths": ["<string>", ...],
  "weaknesses": ["<string>", ...],
  "improved_answer": "<string — a well-crafted model answer>",
  "tips": ["<string>", ...]
}}

Provide 2-4 items for strengths, weaknesses, and tips each.
The improved_answer should be 3-6 sentences demonstrating an ideal response.

Return only the JSON object.
"""


# ── Performance Dashboard ─────────────────────────────────────────────────────

DASHBOARD_SYSTEM_PROMPT = """You are a senior career coach and interview performance analyst.
You have reviewed the complete mock interview session for a candidate and must generate
a comprehensive, structured performance dashboard.

Your dashboard must:
- Aggregate performance across all questions into category-wise scores
- Identify top patterns in strengths and weaknesses
- Prioritize improvement areas by impact
- Recommend specific learning resources relevant to the role
- Provide an honest readiness assessment
- Suggest clear, actionable next steps

IMPORTANT:
- category_scores keys should be specific topic areas relevant to the role (e.g., "JavaScript", "System Design")
- performance_grade: "Excellent" (≥8.5), "Good" (≥7), "Average" (≥5.5), "Needs Improvement" (<5.5)
- Return ONLY valid JSON. No markdown.
"""


def build_dashboard_prompt(
    role: str,
    interview_type: str,
    experience_level: str,
    session_data: list[dict],
) -> str:
    session_text = ""
    for item in session_data:
        session_text += f"""
Q{item['question_number']} [{item.get('category', 'General')}] (Score: {item['score']}/10):
  Question: {item['question']}
  Answer: {item['answer'][:400]}{'...' if len(item['answer']) > 400 else ''}
"""

    return f"""
Interview Session Summary:
- Role: {role}
- Interview Type: {interview_type}
- Experience Level: {experience_level}
- Total Questions: {len(session_data)}

Session Transcript:
{session_text}

Generate a comprehensive performance dashboard as a JSON object with this EXACT structure:
{{
  "overall_score": <float 0-10>,
  "performance_grade": "<Excellent|Good|Average|Needs Improvement>",
  "category_scores": {{
    "<category_name>": <float 0-10>,
    ...
  }},
  "top_strengths": ["<string>", ...],
  "key_weaknesses": ["<string>", ...],
  "improvement_areas": [
    {{
      "area": "<string>",
      "priority": "<High|Medium|Low>",
      "suggestion": "<string>"
    }},
    ...
  ],
  "recommended_topics": [
    {{
      "topic": "<string>",
      "resource": "<string>",
      "url": "<string or null>"
    }},
    ...
  ],
  "interview_readiness": "<string — e.g., 'Ready for Junior roles at mid-size companies'>",
  "next_steps": ["<string>", ...]
}}

Provide:
- 3-5 items for top_strengths
- 3-5 items for key_weaknesses
- 3-5 improvement_areas
- 5-7 recommended_topics
- 4-6 next_steps

Return only the JSON object.
"""
