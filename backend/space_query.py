"""
Handles LLM prompt building and query interpretation for space-related questions.
"""

import os
from google import genai
from backend.data_sources.sat_tracker import get_satellite_location, get_satellite_location_json
from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate
import re
import json

PROMPT_TEMPLATE = (
    "You are a space assistant. The user asked: '{user_input}'. "
    "Based on available satellite data and known missions, answer clearly and concisely."
)

def extract_satellite_name_and_selection(user_input: str):
    """Extract satellite name or NORAD ID and selection number from user input."""
    # Look for selection number (e.g., '2' or 'select 2')
    sel_match = re.search(r"(?:select|option|#)?\s*(\d+)\b", user_input, re.IGNORECASE)
    selection = int(sel_match.group(1)) if sel_match else None
    # Look for NORAD ID
    match = re.search(r"\b(\d{5})\b", user_input)
    if match:
        return match.group(1), selection
    # Look for common satellite names
    keywords = ["iss", "starlink", "hubble", "landsat", "noaa", "iridium"]
    for word in keywords:
        if word in user_input.lower():
            return word.upper(), selection
    # Fallback: try to extract quoted name
    match = re.search(r'"([^"]+)"', user_input)
    if match:
        return match.group(1), selection
    return None, selection

def clean_json_response(text):
    # Remove code block markers and whitespace
    text = re.sub(r"^```(?:json)?", "", text.strip(), flags=re.IGNORECASE)
    text = re.sub(r"```$", "", text.strip())
    return text.strip()

def extract_satellite_parameters(user_input: str) -> dict:
    """Use Gemini to extract sat-tracker-cli parameters from user input."""
    key = os.getenv("GEMINI_API_KEY")
    client = genai.Client(api_key=key)
    param_prompt = (
        "Extract the following parameters from the user's question for a satellite tracking program as a JSON object: "
        "satellite_name (or NORAD ID), ground_station_latitude, ground_station_longitude, time, date, output_format. "
        "If a parameter is not present, use null. Only return a JSON object without the header that it is a JSON." 
        "Make sure the satellite name is in celestrak's data, pick the closest if there's multiple matches." 
        "Remember Celestrak uses abbreviations a lot so make sure the name is actually in the tle data. \n"
        f"User question: {user_input}"
    )
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=param_prompt,
    )
    try:
        cleaned = clean_json_response(response.text)
        params = json.loads(cleaned)
        return params
    except Exception:
        return {}

def answer_query(user_input: str) -> str:
    load_dotenv()
    # Use Gemini to extract parameters
    params = extract_satellite_parameters(user_input)
    print(params)
    sat_name = params.get("satellite_name")
    if sat_name:
        # Build CLI args from extracted params
        cli_args = [sat_name]
        if params.get("ground_station_latitude"):
            cli_args += ["--gs-lat", str(params["ground_station_latitude"])]
        if params.get("ground_station_longitude"):
            cli_args += ["--gs-lon", str(params["ground_station_longitude"])]
        if params.get("date"):
            cli_args += ["--date", str(params["date"])]
        
        cli_args += ["--json"]
        # Call sat-tracker-cli with these args
        sat_json = get_satellite_location_json(*cli_args)
        if isinstance(sat_json, dict):
            prompt = (
                f"Here is satellite tracking data in JSON:\n{json.dumps(sat_json, indent=2)}\n"
                f"User question: {user_input}\n"
                f"Please answer using the data above, making it in a user-friendly format. Include visibility in the response, also include above where on earth it is right now."
            )
            key = os.getenv("GEMINI_API_KEY")
            client = genai.Client(api_key=key)
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
            )
            return response.text
        else:
            # If not JSON, return the error or ambiguous message
            return sat_json
    # Otherwise, use Gemini for general space questions
    prompt = PROMPT_TEMPLATE.format(user_input=user_input)
    key = os.getenv("GEMINI_API_KEY")
    client = genai.Client(api_key=key)
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )
    return response.text
