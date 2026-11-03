# 🧠 AI Personality Copy

An AI system that learns a person's personality through an adaptive interview and creates an AI personality copy capable of responding based on the person's values, beliefs, decision-making patterns, communication style, preferences, and behavioral tendencies.

---

## 📌 Project Overview

AI Personality Copy is a full-stack AI application designed to create a behavioral representation of a person from conversational data.

The system conducts an adaptive personality interview where each question is generated based on the user's previous response.

The answers are:

1. Stored in SQLite
2. Analyzed by Google Gemini
3. Converted into semantic memories
4. Stored in Qdrant
5. Used to build a structured personality profile
6. Retrieved during conversations with the AI personality copy

The final AI personality uses both structured personality information and relevant semantic memories to generate personality-consistent responses.

---

# ✨ Features

### 🧠 Adaptive Personality Interview

The system dynamically generates interview questions based on previous answers.

It explores:

- Core values
- Beliefs
- Decision making
- Problem solving
- Communication
- Emotional tendencies
- Social behavior
- Motivation
- Preferences
- Risk tolerance
- Conflict style
- Ethical reasoning
- Ambition
- Self perception
- Behavioral patterns
- Life experiences

---

### 📊 Personality Profile

The application generates a structured personality profile containing:

- Personality summary
- Communication summary
- Decision-making summary
- Core values
- Beliefs
- Problem-solving style
- Emotional tendencies
- Social behavior
- Motivation
- Risk tolerance
- Conflict style
- Ethical reasoning
- Ambition
- Preferences
- Strengths
- Behavioral patterns
- Self-perception

---

### 🧠 Semantic Personality Memory

Interview responses are converted into vector embeddings using Gemini Embeddings.

These embeddings are stored in Qdrant.

When the user sends a message to the personality copy, the system searches for semantically relevant memories and provides them to Gemini as behavioral context.

This allows the system to retrieve relevant past experiences even when the user's current question does not use the same words.

---

### 💬 AI Personality Chat

The chatbot uses:

- Personality profile
- Relevant semantic memories
- Current conversation message

to generate responses that attempt to match the learned personality.

---

### 🎯 Personality Evaluation

The system can compare a human answer and an AI personality answer.

It evaluates:

- Semantic similarity
- Reasoning similarity
- Decision-making similarity
- Values similarity
- Communication style
- Emotional similarity
- Behavioral similarity

The system generates an overall similarity score from `0–100`.

---

# 🏗️ System Architecture

```text
                         ┌──────────────────────┐
                         │      Streamlit       │
                         │       Frontend       │
                         └──────────┬───────────┘
                                    │
                                    │ HTTP
                                    ▼
                         ┌──────────────────────┐
                         │       FastAPI        │
                         │        Backend       │
                         └──────────┬───────────┘
                                    │
                 ┌──────────────────┼──────────────────┐
                 │                  │                  │
                 ▼                  ▼                  ▼
        ┌────────────────┐  ┌────────────────┐  ┌────────────────┐
        │  Google Gemini │  │     SQLite     │  │     Qdrant     │
        │      API       │  │    Database    │  │ Vector Memory  │
        └────────────────┘  └────────────────┘  └────────────────┘



uvicorn app.backend.main:app --reload
streamlit run app/frontend/streamlit_app.py
docker compose up -d