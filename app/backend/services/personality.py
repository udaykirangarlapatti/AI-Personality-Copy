from app.backend.services.gemini import generate_response


def analyze_answer(
    question: str,
    answer: str,
) -> str:

    prompt = f"""
You are an AI personality analysis engine.

Analyze the person's answer to understand behavioral
patterns that can help an AI reproduce how this person
thinks, communicates, makes decisions, and behaves.

QUESTION:
{question}

ANSWER:
{answer}

Analyze:

1. Values
2. Beliefs
3. Decision-making
4. Problem-solving
5. Communication
6. Emotional tendencies
7. Social behavior
8. Motivation
9. Preferences
10. Behavioral patterns
11. Risk tolerance
12. Conflict style
13. Ethical reasoning
14. Ambition
15. Self-perception

For every meaningful insight provide:

- category
- trait
- observation
- evidence
- confidence from 0 to 1

Return ONLY valid JSON.

Example:

[
  {{
    "category": "decision_making",
    "trait": "independence",
    "observation": "Prefers solving problems independently.",
    "evidence": "The person said they usually try to solve problems themselves first.",
    "confidence": 0.91
  }}
]
"""

    return generate_response(prompt)


def generate_next_question(
    question: str,
    answer: str,
    insights: str,
) -> str:

    prompt = f"""
You are an adaptive AI personality interviewer.

Your goal is to deeply understand the person's real
behavior, thinking patterns, values, decisions,
communication style, preferences, and experiences.

PREVIOUS QUESTION:
{question}

PERSON'S ANSWER:
{answer}

EXTRACTED INSIGHTS:
{insights}

Generate the next interview question.

Requirements:

- Explore something revealed by the answer.
- Investigate something that remains uncertain.
- Ask about real behavior rather than idealized behavior.
- Avoid repeating previous questions.
- Encourage a detailed personal response.
- Sound natural and conversational.
- Gradually explore different personality dimensions.
- Do not ask multiple questions at once.

Return ONLY the next question.
"""

    return generate_response(prompt)