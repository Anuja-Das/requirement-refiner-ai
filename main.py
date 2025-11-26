import json
import os
import time

from app.agents.analyzer_agent import analyze
from app.agents.refiner_agent import refine

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

INPUT_FILE = os.path.join(DATA_DIR, "requirement_input.txt")
ANALYSIS_FILE = os.path.join(DATA_DIR, "analysis_output.json")
FINAL_FILE = os.path.join(DATA_DIR, "final_requirement_output.json")


def load_input():
    with open(INPUT_FILE, "r", encoding="utf-8") as file:
        raw = file.read()
    # Split into lines and remove empty ones
    transcripts = [line.strip() for line in raw.split("\n") if line.strip()]
    return transcripts


def save_json(filepath, data):
    # Ensure output directory exists
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


def main():
    start_time = time.time()

    # Load input requirements
    transcripts = load_input()
    requirement_text = "\n".join(transcripts)

    # Step 1: Analyze the requirements
    analysis_model = analyze(requirement_text)

    # Convert pydantic model to dictionary for JSON serialization
    analysis = analysis_model.model_dump()

    save_json(ANALYSIS_FILE, analysis)

    # Step 2: Refine the analyzed requirements
    refined = refine(requirement_text, analysis)

    save_json(FINAL_FILE, refined)

    print("\nDONE - results stored in:")
    print(f" - {ANALYSIS_FILE}")
    print(f" - {FINAL_FILE}")


    duration = (time.time() - start_time) / 60
    print(f"\nTotal execution time: {duration:.2f} minutes")


if __name__ == "__main__":
    main()

