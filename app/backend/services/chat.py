import json

from app.backend.services.gemini import generate_response
from app.backend.services.vector_memory import search_memory
from app.backend.services.database_service import get_interview_history
from app.backend.services.profile import build_personality_profile


def generate_personality_reply(
    message: str,
    session_id: str,
    db,
) -> str:

    records = get_interview_history(db, session_id)

    if records:
        profile_records = [
            {
                "question": record.question,
                "answer": record.answer,
                "insights": record.insights,
            }
            for record in records
        ]

        profile = build_personality_profile(profile_records)

        profile_context = json.dumps(
            profile,
            indent=2,
        )
    else:
        profile_context = "No personality profile is available."

    memories = search_memory(
        session_id=session_id,
        query=message,
        limit=5,
    )

    if memories:
        memory_context = "\n\n".join(
            [
                f"""
QUESTION:
{memory.payload.get("question", "")}

ANSWER:
{memory.payload.get("answer", "")}

INSIGHTS:
{memory.payload.get("insights", "")}
"""
                for memory in memories
            ]
        )
    else:
        memory_context = "No relevant personality memories were found."

    prompt = f"""
You are an AI personality copy of a real person.

PERSONALITY PROFILE:
{profile_context}

RELEVANT MEMORIES:
{memory_context}

USER MESSAGE:
{message}

Instructions:

- Respond as this person's personality copy.
- Match their communication style.
- Match their values.
- Match their decision-making patterns.
- Match their preferences.
- Use memories as behavioral evidence.
- Do not invent personal facts.
- Do not claim information that is not available.
- If information is insufficient, respond naturally.
- Never mention Qdrant, embeddings, memories, profile generation,
  retrieval, or the AI system.

Return ONLY the response.
"""

    return generate_response(prompt)