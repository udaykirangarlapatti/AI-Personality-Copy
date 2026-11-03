import json

from app.backend.services.gemini import generate_response


def build_personality_profile(
    records: list,
) -> dict:

    if not records:
        return {
            "error": "No interview data available."
        }

    interview_data = []

    for record in records:

        interview_data.append(
            {
                "question": record["question"],
                "answer": record["answer"],
                "insights": record["insights"],
            }
        )

    prompt = f"""
You are a personality profiling engine.

Build a structured personality profile from the person's
interview responses and extracted insights.

INTERVIEW DATA:

{json.dumps(interview_data, indent=2)}

Create a profile covering:

1. Core values
2. Beliefs
3. Decision-making style
4. Problem-solving style
5. Communication style
6. Emotional tendencies
7. Social behavior
8. Motivation
9. Risk tolerance
10. Conflict style
11. Ethical reasoning
12. Ambition
13. Preferences
14. Strengths
15. Behavioral patterns
16. Self-perception

For every category provide:

- summary
- traits
- evidence

Also provide:

- personality_summary
- communication_summary
- decision_making_summary

Important:

- Base the profile only on evidence in the interview.
- Do not diagnose psychological disorders.
- Do not invent information.
- Clearly represent uncertainty where evidence is weak.

Return ONLY valid JSON.

Use this structure:

{{
    "personality_summary": "",
    "communication_summary": "",
    "decision_making_summary": "",

    "core_values": {{
        "summary": "",
        "traits": [],
        "evidence": []
    }},

    "beliefs": {{
        "summary": "",
        "traits": [],
        "evidence": []
    }},

    "decision_making": {{
        "summary": "",
        "traits": [],
        "evidence": []
    }},

    "problem_solving": {{
        "summary": "",
        "traits": [],
        "evidence": []
    }},

    "communication": {{
        "summary": "",
        "traits": [],
        "evidence": []
    }},

    "emotional_tendencies": {{
        "summary": "",
        "traits": [],
        "evidence": []
    }},

    "social_behavior": {{
        "summary": "",
        "traits": [],
        "evidence": []
    }},

    "motivation": {{
        "summary": "",
        "traits": [],
        "evidence": []
    }},

    "risk_tolerance": {{
        "summary": "",
        "traits": [],
        "evidence": []
    }},

    "conflict_style": {{
        "summary": "",
        "traits": [],
        "evidence": []
    }},

    "ethical_reasoning": {{
        "summary": "",
        "traits": [],
        "evidence": []
    }},

    "ambition": {{
        "summary": "",
        "traits": [],
        "evidence": []
    }},

    "preferences": {{
        "summary": "",
        "traits": [],
        "evidence": []
    }},

    "strengths": {{
        "summary": "",
        "traits": [],
        "evidence": []
    }},

    "behavioral_patterns": {{
        "summary": "",
        "traits": [],
        "evidence": []
    }},

    "self_perception": {{
        "summary": "",
        "traits": [],
        "evidence": []
    }}
}}
"""

    response = generate_response(
        prompt
    )

    try:

        return json.loads(
            response
        )

    except json.JSONDecodeError:

        cleaned = response.strip()

        if cleaned.startswith("```json"):
            cleaned = cleaned[7:]

        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]

        return json.loads(
            cleaned.strip()
        )