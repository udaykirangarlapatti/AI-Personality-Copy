import uuid

from sqlalchemy.orm import Session

from app.backend.models.database_models import (
    InterviewRecordDB,
    InterviewSessionDB,
)


def create_interview_session(
    db: Session,
) -> str:

    session_id = str(uuid.uuid4())

    session = InterviewSessionDB(
        session_id=session_id
    )

    db.add(session)
    db.commit()
    db.refresh(session)

    return session_id


def session_exists(
    db: Session,
    session_id: str,
) -> bool:

    session = (
        db.query(InterviewSessionDB)
        .filter(
            InterviewSessionDB.session_id == session_id
        )
        .first()
    )

    return session is not None


def save_interview_record(
    db: Session,
    session_id: str,
    question: str,
    answer: str,
    insights: str,
):

    record = InterviewRecordDB(
        session_id=session_id,
        question=question,
        answer=answer,
        insights=insights,
    )

    db.add(record)
    db.commit()
    db.refresh(record)

    return record


def get_interview_history(
    db: Session,
    session_id: str,
):

    return (
        db.query(InterviewRecordDB)
        .filter(
            InterviewRecordDB.session_id == session_id
        )
        .order_by(
            InterviewRecordDB.created_at
        )
        .all()
    )