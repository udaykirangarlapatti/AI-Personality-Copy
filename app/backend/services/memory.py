from typing import Dict, List


def build_personality_context(
    records: List[Dict],
) -> str:

    if not records:
        return "No personality information is available."

    context = []

    for index, record in enumerate(
        records,
        start=1,
    ):

        context.append(
            f"""
INTERVIEW {index}

QUESTION:
{record.get("question", "")}

ANSWER:
{record.get("answer", "")}

INSIGHTS:
{record.get("insights", "")}
"""
        )

    return "\n".join(context)


def build_personality_summary(
    records: List[Dict],
) -> str:

    if not records:
        return "No personality profile has been created yet."

    return build_personality_context(records)