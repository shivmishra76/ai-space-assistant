"""
Handles LLM prompt building and query interpretation for space-related questions.
"""

import os
from google import genai
from backend.data_sources.sat_tracker import get_iss_location
from dotenv import load_dotenv

PROMPT_TEMPLATE = (
    "You are a space assistant. The user asked: '{user_input}'. "
    "Based on available satellite data and known missions, answer clearly and concisely."
)

def answer_query(user_input: str) -> str:
    load_dotenv()
    # Simple routing: if ISS in question, call sat-tracker-cli, else use Gemini
    if "iss" in user_input.lower():
        return get_iss_location()
    # Otherwise, use Gemini
    prompt = PROMPT_TEMPLATE.format(user_input=user_input)
    key = os.getenv("GEMINI_API_KEY")
    client = genai.Client(api_key=key)
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )
    return response.text
