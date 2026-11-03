import os
import uuid

from dotenv import load_dotenv
from google import genai

from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    FieldCondition,
    Filter,
    MatchValue,
    PointStruct,
    VectorParams,
)


load_dotenv()


QDRANT_URL = os.getenv(
    "QDRANT_URL",
    "http://localhost:6333",
)

COLLECTION_NAME = "personality_memory"

EMBEDDING_MODEL = "gemini-embedding-001"


api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError(
        "GEMINI_API_KEY is not configured."
    )


qdrant = QdrantClient(
    url=QDRANT_URL
)

gemini_client = genai.Client(
    api_key=api_key
)


def create_embedding(text: str) -> list[float]:

    response = gemini_client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=text,
    )

    return response.embeddings[0].values


def create_collection():

    collections = qdrant.get_collections()

    existing = [
        collection.name
        for collection in collections.collections
    ]

    if COLLECTION_NAME in existing:
        return

    embedding = create_embedding(
        "personality memory"
    )

    qdrant.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(
            size=len(embedding),
            distance=Distance.COSINE,
        ),
    )


def store_memory(
    session_id: str,
    question: str,
    answer: str,
    insights: str,
):

    create_collection()

    text = f"""
Question:
{question}

Answer:
{answer}

Insights:
{insights}
"""

    embedding = create_embedding(text)

    qdrant.upsert(
        collection_name=COLLECTION_NAME,
        points=[
            PointStruct(
                id=str(uuid.uuid4()),
                vector=embedding,
                payload={
                    "session_id": session_id,
                    "question": question,
                    "answer": answer,
                    "insights": insights,
                },
            )
        ],
    )


def search_memory(
    session_id: str,
    query: str,
    limit: int = 5,
):

    create_collection()

    embedding = create_embedding(query)

    result = qdrant.query_points(
        collection_name=COLLECTION_NAME,
        query=embedding,
        query_filter=Filter(
            must=[
                FieldCondition(
                    key="session_id",
                    match=MatchValue(
                        value=session_id
                    ),
                )
            ]
        ),
        limit=limit,
    )

    return result.points