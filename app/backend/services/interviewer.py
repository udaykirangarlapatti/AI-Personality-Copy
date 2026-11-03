from app.backend.services.gemini import generate_response


INTERVIEW_CATEGORIES = [
    "values",
    "beliefs",
    "decision_making",
    "problem_solving",
    "communication",
    "emotional_responses",
    "social_behavior",
    "risk_tolerance",
    "motivation",
    "preferences",
    "conflict_style",
    "ethical_reasoning",
    "ambition",
    "self_perception",
    "behavioral_patterns",
    "life_experiences",
]


def generate_first_question() -> str:

    prompt = """
You are an AI personality interviewer.

Your goal is to understand a person's:

- values
- beliefs
- decision-making
- problem-solving
- communication
- emotional responses
- social behavior
- motivations
- preferences
- conflict style
- ethical reasoning
- ambition
- self-perception
- behavioral patterns
- life experiences

Start with one open-ended question.

Requirements:

- Encourage a detailed personal answer.
- Ask about real experiences or behavior.
- Avoid making it feel like a psychological test.
- Sound natural and conversational.
- Do not ask multiple questions.
- Do not ask for sensitive personal information.
- Return ONLY the question.

"""

    return generate_response(prompt)