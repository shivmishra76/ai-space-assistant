"""
Basic CLI interface for the AI Space Assistant.
"""

import typer
from backend.space_query import answer_query

# State for ambiguous satellite selection
last_ambiguous = {"sat_name": None, "options": None}

def main():
    typer.echo("Welcome to AI Space Assistant! Type your space question or 'exit' to quit.")
    while True:
        user_input = typer.prompt("Ask a space question")
        if user_input.lower() in {"exit", "quit"}:
            break
        # If last response was ambiguous and user enters a number, use last sat_name
        if last_ambiguous["sat_name"] and user_input.strip().isdigit():
            response = answer_query(f"{last_ambiguous['sat_name']} select {user_input.strip()}")
            last_ambiguous["sat_name"] = None
            last_ambiguous["options"] = None
        else:
            response = answer_query(user_input)
            # If response contains 'Multiple satellites found', store state
            if response.startswith("Multiple satellites found"):
                # Try to extract the satellite name from the user input
                words = user_input.split()
                last_ambiguous["sat_name"] = words[-1] if words else None
                last_ambiguous["options"] = response
        typer.echo(f"\nAssistant: {response}\n")

if __name__ == "__main__":
    typer.run(main)
