import json

import requests
import streamlit as st


API_URL = "http://localhost:8000"


# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="AI Personality Copy",
    page_icon="🧠",
    layout="wide",
)


# =====================================================
# SESSION STATE
# =====================================================

if "interview_session_id" not in st.session_state:
    st.session_state.interview_session_id = None

if "interview_question" not in st.session_state:
    st.session_state.interview_question = None

if "interview_started" not in st.session_state:
    st.session_state.interview_started = False

if "last_insights" not in st.session_state:
    st.session_state.last_insights = None

if "personality_profile" not in st.session_state:
    st.session_state.personality_profile = None

if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []


# =====================================================
# HELPERS
# =====================================================

def api_post(endpoint, payload):

    response = requests.post(
        f"{API_URL}{endpoint}",
        json=payload,
        timeout=180,
    )

    response.raise_for_status()

    return response.json()


def api_get(endpoint):

    response = requests.get(
        f"{API_URL}{endpoint}",
        timeout=180,
    )

    response.raise_for_status()

    return response.json()


def display_profile_category(
    title,
    category,
):

    if not category:
        return

    st.subheader(title)

    summary = category.get(
        "summary",
        "",
    )

    if summary:
        st.write(summary)

    traits = category.get(
        "traits",
        [],
    )

    if traits:

        st.markdown("**Traits**")

        for trait in traits:
            st.write(f"• {trait}")

    evidence = category.get(
        "evidence",
        [],
    )

    if evidence:

        with st.expander("Evidence"):

            for item in evidence:
                st.write(f"• {item}")


# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.title("🧠 AI Personality Copy")

page = st.sidebar.radio(
    "Navigate",
    [
        "Personality Interview",
        "Personality Profile",
        "Personality Evaluation",
        "AI Personality Chat",
    ],
)


# =====================================================
# PAGE 1 — INTERVIEW
# =====================================================

if page == "Personality Interview":

    st.title("🧠 Personality Interview")

    st.write(
        "Answer naturally. The AI will adapt the next "
        "question based on your previous response."
    )

    if not st.session_state.interview_started:

        if st.button(
            "Start Personality Interview",
            type="primary",
        ):

            try:

                data = api_post(
                    "/api/interview/start",
                    {},
                )

                st.session_state.interview_session_id = (
                    data["session_id"]
                )

                st.session_state.interview_question = (
                    data["question"]
                )

                st.session_state.interview_started = True

                st.rerun()

            except Exception as error:

                st.error(
                    f"Could not start interview: {error}"
                )

    else:

        st.success(
            "Interview session active."
        )

        st.info(
            st.session_state.interview_question
        )

        answer = st.text_area(
            "Your answer",
            height=180,
            key="interview_answer",
        )

        if st.button(
            "Submit Answer",
            type="primary",
        ):

            if not answer.strip():

                st.warning(
                    "Please enter an answer."
                )

            else:

                try:

                    data = api_post(
                        "/api/interview/answer",
                        {
                            "session_id": (
                                st.session_state
                                .interview_session_id
                            ),
                            "question": (
                                st.session_state
                                .interview_question
                            ),
                            "answer": answer,
                        },
                    )

                    st.session_state.last_insights = (
                        data.get("insights")
                    )

                    st.session_state.interview_question = (
                        data["next_question"]
                    )

                    st.rerun()

                except Exception as error:

                    st.error(
                        f"Could not process answer: {error}"
                    )

        if st.session_state.last_insights:

            with st.expander(
                "Latest Personality Insights"
            ):

                insights = (
                    st.session_state.last_insights
                )

                try:

                    parsed = json.loads(
                        insights
                    )

                    st.json(parsed)

                except Exception:

                    st.write(insights)

        st.divider()

        if st.button(
            "End Interview",
        ):

            st.session_state.interview_started = False

            st.session_state.interview_question = None

            st.session_state.last_insights = None

            st.rerun()


# =====================================================
# PAGE 2 — PERSONALITY PROFILE
# =====================================================

elif page == "Personality Profile":

    st.title("📊 Personality Profile")

    session_id = (
        st.session_state.interview_session_id
    )

    if not session_id:

        st.info(
            "Complete at least one interview answer first."
        )

    else:

        st.write(
            f"Session: `{session_id}`"
        )

        if st.button(
            "Generate Personality Profile",
            type="primary",
        ):

            try:

                data = api_get(
                    f"/api/profile/{session_id}"
                )

                st.session_state.personality_profile = (
                    data["profile"]
                )

            except Exception as error:

                st.error(
                    f"Could not generate profile: {error}"
                )

        profile = (
            st.session_state.personality_profile
        )

        if profile:

            if "error" in profile:

                st.error(
                    profile["error"]
                )

            else:

                st.header(
                    "Personality Summary"
                )

                st.write(
                    profile.get(
                        "personality_summary",
                        "",
                    )
                )

                col1, col2 = st.columns(2)

                with col1:

                    st.subheader(
                        "Communication"
                    )

                    st.write(
                        profile.get(
                            "communication_summary",
                            "",
                        )
                    )

                with col2:

                    st.subheader(
                        "Decision Making"
                    )

                    st.write(
                        profile.get(
                            "decision_making_summary",
                            "",
                        )
                    )

                st.divider()

                display_profile_category(
                    "Core Values",
                    profile.get(
                        "core_values"
                    ),
                )

                display_profile_category(
                    "Beliefs",
                    profile.get(
                        "beliefs"
                    ),
                )

                display_profile_category(
                    "Decision Making",
                    profile.get(
                        "decision_making"
                    ),
                )

                display_profile_category(
                    "Problem Solving",
                    profile.get(
                        "problem_solving"
                    ),
                )

                display_profile_category(
                    "Communication",
                    profile.get(
                        "communication"
                    ),
                )

                display_profile_category(
                    "Emotional Tendencies",
                    profile.get(
                        "emotional_tendencies"
                    ),
                )

                display_profile_category(
                    "Social Behavior",
                    profile.get(
                        "social_behavior"
                    ),
                )

                display_profile_category(
                    "Motivation",
                    profile.get(
                        "motivation"
                    ),
                )

                display_profile_category(
                    "Risk Tolerance",
                    profile.get(
                        "risk_tolerance"
                    ),
                )

                display_profile_category(
                    "Conflict Style",
                    profile.get(
                        "conflict_style"
                    ),
                )

                display_profile_category(
                    "Ethical Reasoning",
                    profile.get(
                        "ethical_reasoning"
                    ),
                )

                display_profile_category(
                    "Ambition",
                    profile.get(
                        "ambition"
                    ),
                )

                display_profile_category(
                    "Preferences",
                    profile.get(
                        "preferences"
                    ),
                )

                display_profile_category(
                    "Strengths",
                    profile.get(
                        "strengths"
                    ),
                )

                display_profile_category(
                    "Behavioral Patterns",
                    profile.get(
                        "behavioral_patterns"
                    ),
                )

                display_profile_category(
                    "Self Perception",
                    profile.get(
                        "self_perception"
                    ),
                )


# =====================================================
# PAGE 3 — EVALUATION
# =====================================================

elif page == "Personality Evaluation":

    st.title("🎯 Personality Evaluation")

    st.write(
        "Compare a human answer with the AI personality "
        "copy's answer."
    )

    question = st.text_area(
        "Question",
        height=100,
    )

    human_answer = st.text_area(
        "Human Answer",
        height=150,
    )

    ai_answer = st.text_area(
        "AI Personality Answer",
        height=150,
    )

    if st.button(
        "Evaluate Personality",
        type="primary",
    ):

        if not question.strip():

            st.warning(
                "Please enter the question."
            )

        elif not human_answer.strip():

            st.warning(
                "Please enter the human answer."
            )

        elif not ai_answer.strip():

            st.warning(
                "Please enter the AI answer."
            )

        else:

            try:

                data = api_post(
                    "/api/evaluation",
                    {
                        "question": question,
                        "human_answer": human_answer,
                        "ai_answer": ai_answer,
                    },
                )

                evaluation = data[
                    "evaluation"
                ]

                try:

                    parsed = json.loads(
                        evaluation
                    )

                    st.subheader(
                        "Evaluation Result"
                    )

                    overall = parsed.get(
                        "overall_score"
                    )

                    if overall is not None:

                        st.metric(
                            "Overall Personality Match",
                            f"{overall}/100",
                        )

                    st.json(parsed)

                except Exception:

                    st.write(evaluation)

            except Exception as error:

                st.error(
                    f"Evaluation failed: {error}"
                )


# =====================================================
# PAGE 4 — AI PERSONALITY CHAT
# =====================================================

elif page == "AI Personality Chat":

    st.title("💬 AI Personality Chat")

    session_id = (
        st.session_state.interview_session_id
    )

    if not session_id:

        st.warning(
            "Start a personality interview first."
        )

    else:

        st.caption(
            f"Personality session: {session_id}"
        )

        for message in (
            st.session_state.chat_messages
        ):

            with st.chat_message(
                message["role"]
            ):

                st.write(
                    message["content"]
                )

        user_message = st.chat_input(
            "Talk to your AI personality..."
        )

        if user_message:

            st.session_state.chat_messages.append(
                {
                    "role": "user",
                    "content": user_message,
                }
            )

            with st.chat_message("user"):

                st.write(
                    user_message
                )

            try:

                data = api_post(
                    "/api/chat",
                    {
                        "session_id": session_id,
                        "message": user_message,
                    },
                )

                reply = data["reply"]

                st.session_state.chat_messages.append(
                    {
                        "role": "assistant",
                        "content": reply,
                    }
                )

                with st.chat_message(
                    "assistant"
                ):

                    st.write(reply)

            except Exception as error:

                st.error(
                    f"Chat failed: {error}"
                )