"""
Agent B: Requirements Refiner Agent
Runs Requirement Refiner Tool and Acceptance Criteria Generator Tool,
and writes refined_output.json
"""

import json
import logging
import os

from app.core.schemas import FinalRequirement
from app.tools.acceptance_criteria_gen_tool import generate_acceptance_criteria
from app.tools.requirement_rewriter_tool import rewrite_requirement

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
def refine(requirement_txt: str, analysis: dict, rag_context: str = ""):
    logger.info("Agent 2: started")

    # Merge RAG knowledge if provided
    enriched_requirement = requirement_txt
    if rag_context and rag_context.strip():
        enriched_requirement += f"\n\n# Additional Context from Knowledge Base:\n{rag_context}"
        enriched_requirement += "INSTRUCTION: Use the knowledge above to fill in any placeholders in the requirement and make it fully concrete."

    # Run Requirement Rewriter Tool
    rewritten = rewrite_requirement(enriched_requirement,
                                    ambiguities=analysis.get("ambiguous_phrases", []),
                                    missing=analysis.get("missing_information", []))

    # Extract refined requirement from the rewritten output
    refined_text = rewritten.get("refined_requirement", requirement_txt)

    # Run Acceptance Criteria Generator Tool
    acceptance_criteria = generate_acceptance_criteria(refined_text)

    # Ensure acceptance criteria is a list, fallback to empty list if None
    if acceptance_criteria is None:
        acceptance_criteria = []

    # Create the final requirement model (as dict for JSON serialization)
    final_requirement = FinalRequirement(
        refined_requirement=refined_text,
        acceptance_criteria=acceptance_criteria
    ).model_dump()

    # Save the final requirement to a JSON file
    with open(FINAL_PATH, "w", encoding="utf-8") as file:
        json.dump(final_requirement, file, indent=4)

    logger.info(f"Agent 2: completed successfully")
    return final_requirement
