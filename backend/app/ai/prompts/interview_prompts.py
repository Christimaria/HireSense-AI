"""
HireSense AI — Interview Question Prompts
"""

# ── Role-specific context hints ────────────────────────────────────────────────

ROLE_CONTEXT = {
    "Software Engineer": "algorithms, data structures, system design, OOP, clean code principles",
    "Frontend": "HTML, CSS, JavaScript, React/Vue, browser APIs, performance, accessibility, responsive design",
    "Backend": "REST APIs, databases, server architecture, caching, authentication, microservices",
    "Full Stack": "frontend frameworks, backend services, databases, deployment, full product ownership",
    "Data Analyst": "SQL, Excel, data visualization, statistics, business insights, dashboards, reporting",
    "Data Scientist": "machine learning, statistics, Python/R, model evaluation, feature engineering, experimentation",
    "AI Engineer": "LLMs, deep learning, model deployment, MLOps, vector databases, fine-tuning, prompt engineering",
    "DevOps": "CI/CD pipelines, Docker, Kubernetes, cloud infrastructure, monitoring, IaC, SRE practices",
    "Cybersecurity": "threat analysis, penetration testing, SIEM, incident response, network security, compliance",
    "HR": "company culture, team fit, communication, conflict resolution, motivation, career goals",
}

INTERVIEW_TYPE_CONTEXT = {
    "Technical": "Focus on technical depth, problem-solving, architecture decisions, and coding concepts.",
    "Behavioral": "Use the STAR method (Situation, Task, Action, Result). Focus on past experiences and soft skills.",
    "HR": "Focus on culture fit, motivation, work ethic, communication, and career aspirations.",
}

EXPERIENCE_CONTEXT = {
    "Fresher": "entry-level candidate with no or very little professional experience. Ask foundational questions.",
    "Junior": "1-2 years of experience. Expect basic practical knowledge but limited system design exposure.",
    "Mid": "3-5 years. Expect solid technical knowledge, project ownership, and some mentoring experience.",
    "Senior": "5+ years. Expect architectural thinking, leadership, trade-off analysis, and broad domain expertise.",
}


# ── System Prompt ──────────────────────────────────────────────────────────────

INTERVIEW_SYSTEM_PROMPT = """You are a professional technical interviewer at a top technology company.
Your job is to conduct realistic, challenging, and fair mock interviews.

RULES:
- Ask ONE question at a time. Never ask multiple questions in a single response.
- Questions must be relevant to the role, experience level, and interview type.
- Do NOT repeat questions that have already been asked in this session.
- Progress naturally: start easier, build complexity as the session continues.
- For behavioral questions, set up scenarios clearly.
- For technical questions, be specific — avoid vague or generic questions.
- Return ONLY the question text. No greetings, no prefixes like "Question 3:", no explanations.
"""


def build_question_prompt(
    role: str,
    experience_level: str,
    interview_type: str,
    question_number: int,
    total_questions: int,
    conversation_history: list[dict],
) -> str:
    role_ctx = ROLE_CONTEXT.get(role, role)
    type_ctx = INTERVIEW_TYPE_CONTEXT.get(interview_type, "")
    exp_ctx = EXPERIENCE_CONTEXT.get(experience_level, experience_level)

    history_text = ""
    if conversation_history:
        history_lines = []
        for turn in conversation_history:
            history_lines.append(f"Q: {turn['question']}")
            history_lines.append(f"A: {turn['answer'][:300]}...")  # Truncate long answers
        history_text = "\n".join(history_lines)

    return f"""
Interview Configuration:
- Role: {role}
- Experience Level: {experience_level} ({exp_ctx})
- Interview Type: {interview_type}
- Question: {question_number} of {total_questions}
- Key Topics: {role_ctx}
- Style Guidance: {type_ctx}

{"Previous conversation history:" if history_text else "This is the FIRST question of the session."}
{history_text}

Now generate question #{question_number}. Return ONLY the question text.
"""
