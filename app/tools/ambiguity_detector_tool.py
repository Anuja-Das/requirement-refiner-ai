"""
Tool: Ambiguity Detector
Takes a requirement text and returns a list of ambiguous phrases
"""

from app.core.llm_adapter import llm
from app.core.prompts import ambiguity_detector_prompt
import logging, json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# This function detects ambiguous phrases in a requirement text.
def detect_ambiguities(requirement):
    logger.info("Agent 1 Tool 1: started")

    # --- Normalize input ---
    # If input is a list, join elements into a single string
    if isinstance(requirement, list):
        requirement = " ".join(str(x) for x in requirement)
    # If input is a dict, ocnvert to string using JSON
    if isinstance(requirement, dict):
        requirement = json.dumps(requirement)
    # Ensure input is a string
    if not isinstance(requirement, str):
        requirement = str(requirement)

    prompt = ambiguity_detector_prompt.format(requirement=requirement)

    response = llm.generate(prompt)

    # Try to parse a JSON array from the LLM response
    start = response.find('[')
    end = response.find(']')
    if start != -1 and end != -1 and end > start:
        arr_text = response[start:end + 1]
        parsed = json.loads(arr_text)
        # If the parsed result is a list, return it as ambiguous phrases
        if isinstance(parsed, list):
            logger.info("Agent 1 Tool 1: completed successfully")
            return [str(x) for x in parsed]
    return None