from pydantic import BaseModel, Field


class PersonalityInsight(BaseModel):

    category: str

    trait: str

    observation: str

    evidence: str

    confidence: float = Field(
        ge=0.0,
        le=1.0,
    )