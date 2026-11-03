import os
import time

from dotenv import load_dotenv
from google import genai


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError(
        "GEMINI_API_KEY is not configured."
    )


client = genai.Client(
    api_key=api_key
)

MODEL_NAME = "gemini-3.5-flash-lite"


def generate_response(
    prompt: str,
    max_retries: int = 3,
) -> str:

    for attempt in range(max_retries):

        try:

            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=prompt,
            )

            if not response.text:
                raise RuntimeError(
                    "Gemini returned an empty response."
                )

            return response.text.strip()

        except Exception as error:

            error_text = str(error)

            retryable = (
                "503" in error_text
                or "429" in error_text
                or "UNAVAILABLE" in error_text
                or "RESOURCE_EXHAUSTED" in error_text
            )

            if retryable and attempt < max_retries - 1:

                time.sleep(
                    2 ** attempt
                )

                continue

            raise


    raise RuntimeError(
        "Gemini failed after multiple attempts."
    )