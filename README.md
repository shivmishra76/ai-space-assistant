# AI Space Assistant

A natural language assistant for answering space-related queries, such as satellite tracking, ISS positions, or orbital info. It integrates LLMs (OpenAI GPT or local models) with real-time space data sources like sat-tracker-cli and NASA APIs.

## Features
- Answer questions like "Where is the ISS right now?" or "What satellites are overhead?"
- Uses LLMs to interpret user queries
- Connects to satellite data sources (sat-tracker-cli, NASA, OpenNotify, NORAD)
- Modular: CLI, API, and web interface planned

## Project Structure
```
ai-space-assistant/
├── backend/
│   ├── main.py                # Entrypoint for the assistant
│   ├── space_query.py         # LLM prompt building and query interpretation
│   ├── data_sources/
│   │   ├── sat_tracker.py     # Interface to sat-tracker-cli
│   │   ├── nasa_api.py        # NASA or other APIs
│   ├── models/                # Prompt templates or local models
│   └── utils/                 # Helper functions
├── interface/
│   ├── cli.py                 # CLI interface
│   └── web/                   # (optional) FastAPI or web frontend
├── tests/                     # Test cases for user queries
├── requirements.txt
└── README.md
```

## Example Queries
- "Where is the ISS right now?"
- "What satellites are overhead in my area?"
- "Give me info on Starlink satellites passing over Illinois tonight."
- "What is the TLE for satellite NORAD ID 25544?"

## Getting Started
1. Clone the repo and install requirements:
   ```sh
   pip install -r requirements.txt
   ```
2. Run the CLI (to be implemented):
   ```sh
   python interface/cli.py
   ```

## Contributing
Contributions are welcome! See issues for ideas or open a PR.
