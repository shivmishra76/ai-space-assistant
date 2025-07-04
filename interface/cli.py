"""
Basic CLI interface for the AI Space Assistant.
"""

import typer
from backend.space_query import answer_query

def main():
    typer.echo("Welcome to AI Space Assistant! Type your space question or 'exit' to quit.")
    while True:
        user_input = typer.prompt("Ask a space question")
        if user_input.lower() in {"exit", "quit"}:
            break
        response = answer_query(user_input)
        typer.echo(f"\nAssistant: {response}\n")

if __name__ == "__main__":
    typer.run(main)
