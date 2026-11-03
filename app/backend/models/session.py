from typing import List

from pydantic import BaseModel, Field


class InterviewRecord(BaseModel):

    question: str
    answer: str
    insights: str


class InterviewSession(BaseModel):

    session_id: str

    records: List[InterviewRecord] = Field(
        default_factory=list
    )