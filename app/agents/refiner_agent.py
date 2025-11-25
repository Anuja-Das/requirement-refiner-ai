"""
Agent B: Requirements Refiner Agent
Runs Requirement Refiner Tool and Acceptance Criteria Generator Tool,
and writes refined_output.json
"""

import os, logging, json

from app.tools.requirement_rewriter_tool import rewrite_requirement
from app.tools.acceptance_criteria_gen_tool import generate_acceptance_criteria
from app.schemas import FinalRequirement

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Setup the data directory and the output file path
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", "data")
DATA_DIR = os.path.normpath(DATA_DIR)
FINAL_PATH = os.path.join(DATA_DIR, "final_requirement_output.json")


# Main function for refining requirements
# Accepts the original requirement text and analysis dictionary from Agent A
# 1. Runs Requirement Rewriter Tool to refine the requirement
# 2. Runs Acceptance Criteria Generator Tool to generate acceptance criteria
# 3. Saves the final refined requirement to a JSON file
# 4. Returns a FinalRequirement model instance
def refine(requirement_txt: str, analysis: dict):
    logger.info("Agent 2: started")

    # Run Requirement Rewriter Tool
    rewritten = rewrite_requirement(requirement_txt,
                                              ambiguities=analysis.get("ambiguous_phrases", []),
                                              missing_info=analysis.get("missing_information", []))

    # Extract refined requirement and notes from the rewritten output
    refined_text = rewritten.get("refined_requirement", requirement_txt)
    notes = rewritten.get("notes", "")

    # Ensure notes is a string, fallback to empty string if None
    if notes is None:
        notes = ""

    # Run Acceptance Criteria Generator Tool
    acceptance_criteria = generate_acceptance_criteria(refined_text)

    # Ensure acceptance criteria is a list, fallback to empty list if None
    if acceptance_criteria is None:
        acceptance_criteria = []

    # Create the final requirement model (as dict for JSON serialization)
    final_requirement = FinalRequirement(
        refined_requirement=refined_text,
        acceptance_criteria=acceptance_criteria,
        notes=notes
    ).model_dump()

    # Save the final requirement to a JSON file
    with open(FINAL_PATH, "w", encoding="utf-8") as file:
        json.dump(final_requirement, file, indent=4)

    logger.info(f"Agent 2: completed successfully")
    return final_requirement
