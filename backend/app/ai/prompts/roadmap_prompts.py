"""
HireSense AI — Career Roadmap Prompts
"""

ROADMAP_SYSTEM_PROMPT = """You are a senior software engineering mentor and career coach with expertise
in building personalized learning roadmaps for aspiring tech professionals.

You deeply understand:
- Current technology landscape and in-demand skills
- Realistic learning timelines for different experience levels
- The best free and paid resources for each topic
- What employers actually look for in candidates

IMPORTANT:
- Be realistic about what can be achieved in the given timeline.
- Prioritize high-impact skills over nice-to-haves.
- Include a mix of free and paid resources — prefer free when quality is equal.
- Milestones should be concrete and verifiable (e.g., "Build a project", "Complete 5 exercises").
- Return ONLY valid JSON matching the specified schema. No markdown.
"""


def build_roadmap_prompt(
    current_skills: list[str],
    target_role: str,
    timeline_weeks: int,
) -> str:
    skills_str = ", ".join(current_skills) if current_skills else "No prior tech skills"

    # Dynamically compute the number of week blocks
    if timeline_weeks <= 8:
        week_blocks = "2-week blocks"
    elif timeline_weeks <= 16:
        week_blocks = "2-week blocks (some can be 1-week for quick wins)"
    else:
        week_blocks = "2-3 week blocks"

    return f"""
Generate a personalized career roadmap:

Candidate Profile:
- Current Skills: {skills_str}
- Target Role: {target_role}
- Timeline: {timeline_weeks} weeks
- Week Block Size: {week_blocks}

Identify the skill gaps between the current skills and the target role requirements first.

Return a JSON object with this EXACT structure:
{{
  "roadmap_title": "<string — e.g., 'From Python Beginner to Data Scientist in 12 Weeks'>",
  "skill_gaps": ["<skill>", ...],
  "weeks": [
    {{
      "week_range": "<string — e.g., '1-2'>",
      "focus": "<string — main theme of this block>",
      "topics": ["<string>", ...],
      "resources": [
        {{
          "title": "<string>",
          "url": "<string or null>",
          "type": "<free|paid|book|youtube>"
        }}
      ],
      "milestone": "<string — a concrete deliverable or project>"
    }},
    ...
  ]
}}

Requirements:
- Cover the full {timeline_weeks}-week span without gaps.
- Identify 4-8 skill_gaps.
- Each week block should have 3-5 topics.
- Each week block should have 2-3 resources.
- Keep milestones practical and achievable in the given time block.

Return only the JSON object.
"""
