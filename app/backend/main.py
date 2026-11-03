from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.backend.database import (
    Base,
    SessionLocal,
    engine,
)

from app.backend.services.gemini import generate_response
from app.backend.services.interviewer import generate_first_question
from app.backend.services.personality import (
    analyze_answer,
    generate_next_question,
)
from app.backend.services.database_service import (
    create_interview_session,
    session_exists,
    save_interview_record,
    get_interview_history,
)
from app.backend.services.evaluation import evaluate_personality
from app.backend.services.chat import generate_personality_reply
from app.backend.services.vector_memory import store_memory
from app.backend.services.profile import build_personality_profile


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="AI Personality Copy API",
    description="Backend API for the AI Personality Copy project",
    version="0.5.0",
)


def get_db():

    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


class PromptRequest(BaseModel):
    prompt: str


class InterviewAnswerRequest(BaseModel):
    session_id: str
    question: str
    answer: str


class EvaluationRequest(BaseModel):
    question: str
    human_answer: str
    ai_answer: str


class ChatRequest(BaseModel):
    session_id: str
    message: str


@app.get("/")
def root():

    return {
        "message": "AI Personality Copy API is running"
    }


@app.get("/health")
def health_check():

    return {
        "status": "healthy"
    }


@app.post("/api/generate")
def generate(request: PromptRequest):

    response = generate_response(
        request.prompt
    )

    return {
        "response": response
    }


@app.post("/api/interview/start")
def start_interview(
    db: Session = Depends(get_db),
):

    session_id = create_interview_session(db)

    question = generate_first_question()

    return {
        "session_id": session_id,
        "question": question,
    }


@app.post("/api/interview/answer")
def process_interview_answer(
    request: InterviewAnswerRequest,
    db: Session = Depends(get_db),
):

    if not session_exists(
        db,
        request.session_id,
    ):

        raise HTTPException(
            status_code=404,
            detail="Interview session not found.",
        )

    insights = analyze_answer(
        request.question,
        request.answer,
    )

    save_interview_record(
        db=db,
        session_id=request.session_id,
        question=request.question,
        answer=request.answer,
        insights=insights,
    )

    store_memory(
        session_id=request.session_id,
        question=request.question,
        answer=request.answer,
        insights=insights,
    )

    next_question = generate_next_question(
        request.question,
        request.answer,
        insights,
    )

    return {
        "session_id": request.session_id,
        "insights": insights,
        "next_question": next_question,
    }


@app.get("/api/interview/{session_id}")
def get_interview_session(
    session_id: str,
    db: Session = Depends(get_db),
):

    if not session_exists(
        db,
        session_id,
    ):

        raise HTTPException(
            status_code=404,
            detail="Interview session not found.",
        )

    records = get_interview_history(
        db,
        session_id,
    )

    return {
        "session_id": session_id,
        "records": [
            {
                "question": record.question,
                "answer": record.answer,
                "insights": record.insights,
                "created_at": record.created_at,
            }
            for record in records
        ],
    }


@app.get("/api/profile/{session_id}")
def get_personality_profile(
    session_id: str,
    db: Session = Depends(get_db),
):

    if not session_exists(
        db,
        session_id,
    ):

        raise HTTPException(
            status_code=404,
            detail="Interview session not found.",
        )

    records = get_interview_history(
        db,
        session_id,
    )

    if not records:

        raise HTTPException(
            status_code=400,
            detail="No interview answers available.",
        )

    profile_records = [
        {
            "question": record.question,
            "answer": record.answer,
            "insights": record.insights,
        }
        for record in records
    ]

    profile = build_personality_profile(
        profile_records
    )

    return {
        "session_id": session_id,
        "profile": profile,
    }


@app.post("/api/evaluation")
def evaluation(
    request: EvaluationRequest,
):

    result = evaluate_personality(
        question=request.question,
        human_answer=request.human_answer,
        ai_answer=request.ai_answer,
    )

    return {
        "evaluation": result
    }


@app.post("/api/chat")
def personality_chat(
    request: ChatRequest,
    db: Session = Depends(get_db),
):

    if not session_exists(
        db,
        request.session_id,
    ):

        raise HTTPException(
            status_code=404,
            detail="Interview session not found.",
        )

    reply = generate_personality_reply(
        message=request.message,
        session_id=request.session_id,
        db=db,
    )

    return {
        "session_id": request.session_id,
        "message": request.message,
        "reply": reply,
    }