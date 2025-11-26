"""
Tool: Missing Information Extractor
Generates a list of missing details an engineer would need to implement the requirement.
"""

import json
import logging

from app.core.llm_adapter import llm
from app.core.prompts import missing_info_extractor_prompt

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# This function extracts missing information from a requirement text.
def extract_missing_info(requirement: str) -> list[str] | None:
    logger.info("Agent 1 Tool 2: started")
    prompt = missing_info_extractor_prompt.format(requirement=requirement)
    response = llm.generate(prompt)

    # Try to extract a JSON array from the LLM response
    start = response.find('[')
    end = response.find(']')
    if start != -1 and end != -1 and end > start:
        arr_text = response[start:end + 1]
        parsed = json.loads(arr_text)
        # If the parsed result is a list, return it as missing info
        if isinstance(parsed, list):
            logger.info("Agent 1 Tool 2: completed successfully")
            return [str(x) for x in parsed]

    # If no valid list is found, return None
    return None
