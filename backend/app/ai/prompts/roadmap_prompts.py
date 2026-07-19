"""
HireSense AI — Career Roadmap Prompts

Defines prompts to generate week-by-week learning pathways to close skill gaps.
"""

ROADMAP_SYSTEM_PROMPT = """\
You are an expert career coach, senior technical trainer, and talent development specialist with 15+ years of experience helping professionals transition roles and level up.
Your task is to analyze a candidate's current skills and target role, identify the core skill gaps, and generate a customized week-by-week learning roadmap for the specified timeline.

RULES:
- Be highly practical. Focus on project-based learning and hands-on milestones.
- Ensure the roadmap fits the requested timeline (e.g. if the timeline is '3 months', generate weekly plans for approximately 12 weeks. If the timeline is '8 weeks', generate 8 weekly plans).
- The resources you recommend must be highly reputable (e.g. official documentation, widely-known free or paid courses, books). Include placeholders or real links where appropriate.
- Every week must have a clear main focus, a list of sub-topics, and a list of practical tasks.
- Your entire response must be a single JSON object matching the requested structure.
- Do NOT include markdown formatting or prose outside the JSON block. Return ONLY the JSON object.
"""


def build_roadmap_prompt(
    current_skills: list[str],
    target_role: str,
    timeline: str,
) -> str:
    """
    Construct user prompt for generating a career roadmap.

    Args:
        current_skills: Candidate's existing skills.
        target_role: Target job title.
        timeline: Expected timeframe (e.g. '3 months', '8 weeks').

    Returns:
        Formatted user prompt.
    """
    skills_list = ", ".join(current_skills)

    return f"""\
Candidate Context:
- Current Skills: {skills_list}
- Target Role: {target_role}
- Timeline: {timeline}

Analyze the difference between the candidate's current skills and the target role's expectations. Generate a detailed, week-by-week roadmap to bridge these skill gaps within the {timeline} timeframe.

Your response must follow exactly this JSON structure:
{{
  "weekly_roadmap": [
    {{
      "week": 1,
      "focus": "<main focus topic of the week>",
      "topics": [
        "<sub-topic 1>",
        "<sub-topic 2>"
      ],
      "tasks": [
        "<practical coding task or hands-on practice step 1>",
        "<practical coding task or hands-on practice step 2>"
      ]
    }},
    ...
  ],
  "skill_gaps": [
    "<core gap/missing concept 1>",
    "<core gap/missing concept 2>",
    "<core gap/missing concept 3>"
  ],
  "learning_resources": [
    {{
      "title": "<name of learning resource, e.g. 'Official MDN JavaScript Guide' or 'React - The Complete Guide'>",
      "url": "<optional direct link to resource if known, or null>",
      "type": "<e.g., Course, Documentation, Book, Tutorial>",
      "description": "<why this resource is recommended for this transition>"
    }},
    ...
  ],
  "milestones": [
    {{
      "week_number": <integer week index of checkpoint>,
      "title": "<title of milestone check>",
      "description": "<success criteria or project demonstration expected>"
    }},
    ...
  ]
}}

Return ONLY the JSON object. No markdown fences, no backticks, no markdown formatting outside of JSON string fields.
"""
