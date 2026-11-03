import json

from app.backend.services.gemini import generate_response


def evaluate_personality(
    question: str,
    human_answer: str,
    ai_answer: str,
) -> dict:

    prompt = f"""
You are a personality similarity evaluation engine.

Compare the HUMAN and AI PERSONALITY answers to the same question.

QUESTION:
{question}

HUMAN ANSWER:
{human_answer}

AI PERSONALITY ANSWER:
{ai_answer}

Evaluate these dimensions:

1. semantic_similarity
2. reasoning_similarity
3. decision_making_similarity
4. values_similarity
5. communication_style_similarity
6. emotional_similarity
7. behavioral_similarity

For every dimension provide:

- score: integer from 0 to 100
- explanation: concise explanation

Also provide:

- overall_score: integer from 0 to 100
- strongest_match
- biggest_difference
- improvement_suggestion

Important:

- Judge actual similarity, not whether both answers are simply positive.
- Focus on reasoning, values, behavior, and communication.
- Do not invent information.
- Return ONLY valid JSON.

Use exactly this structure:

{{
    "semantic_similarity": {{
        "score": 0,
        "explanation": ""
    }},
    "reasoning_similarity": {{
        "score": 0,
        "explanation": ""
    }},
    "decision_making_similarity": {{
        "score": 0,
        "explanation": ""
    }},
    "values_similarity": {{
        "score": 0,
        "explanation": ""
    }},
    "communication_style_similarity": {{
        "score": 0,
        "explanation": ""
    }},
    "emotional_similarity": {{
        "score": 0,
        "explanation": ""
    }},
    "behavioral_similarity": {{
        "score": 0,
        "explanation": ""
    }},
    "overall_score": 0,
    "strongest_match": "",
    "biggest_difference": "",
    "improvement_suggestion": ""
}}
"""

    response = generate_response(prompt)

    cleaned = response.strip()

    if cleaned.startswith("```json"):
        cleaned = cleaned[7:]

    elif cleaned.startswith("```"):
        cleaned = cleaned[3:]

    if cleaned.endswith("```"):
        cleaned = cleaned[:-3]

    cleaned = cleaned.strip()

    try:
        return json.loads(cleaned)

    except json.JSONDecodeError:
        return {
            "error": "Unable to parse evaluation.",
            "raw_response": response,
        }