from pydantic import BaseModel, Field


class InterviewAnswer(BaseModel):

    session_id: str

    answer: str = Field(
        min_length=1,
        max_length=5000,
    )


class InterviewQuestion(BaseModel):

    question: str

    category: str = "general"