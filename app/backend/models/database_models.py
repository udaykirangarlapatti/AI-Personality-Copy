from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, Text

from app.backend.database import Base


class InterviewSessionDB(Base):

    __tablename__ = "interview_sessions"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    session_id = Column(
        String,
        unique=True,
        index=True,
        nullable=False,
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )


class InterviewRecordDB(Base):

    __tablename__ = "interview_records"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    session_id = Column(
        String,
        index=True,
        nullable=False,
    )

    question = Column(
        Text,
        nullable=False,
    )

    answer = Column(
        Text,
        nullable=False,
    )

    insights = Column(
        Text,
        nullable=False,
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )