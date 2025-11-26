"""
Tool: Requirement Rewriter
Produces a concise, unambiguous, engineering-ready requirement
"""

import json
import logging
import re
from typing import Any

from app.core.llm_adapter import llm
from app.core.prompts import requirement_rewriter_prompt

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# --- FIX 1: Extract complete JSON using balanced braces ---
def extract_json_block(text: str) -> str:
    """
    Extracts the first complete JSON object from the text
    using a balanced-brace counter.
    """
    start = text.find('{')
    if start == -1:
        return ""

    brace_count = 0
    for i in range(start, len(text)):
        if text[i] == '{':
            brace_count += 1
        elif text[i] == '}':
            brace_count -= 1
            if brace_count == 0:
                return text[start:i + 1]

    return ""  # No complete JSON found


# Main function: Rewrites requirement
def rewrite_requirement(requirement: str, ambiguities: list = None, missing: list = None) -> dict[str, Any]:
    logger.info("Agent 2 Tool 1: started")

    ambiguities = ambiguities or []
    missing = missing or []

    prompt = requirement_rewriter_prompt.format(
        requirement=requirement,
        ambiguities=json.dumps(ambiguities, indent=4),
        missing=json.dumps(missing, indent=4)
    )

    response = llm.generate(prompt)

    # Extract full JSON from response
    obj_text = extract_json_block(response)

    if obj_text:
        # Remove control characters before parsing
        obj_text_clean = re.sub(r'[\x00-\x1F\x7F]', '', obj_text)

        try:
            parsed = json.loads(obj_text_clean)

            # Keep only known fields
            allowed_keys = ["refined_requirement", "acceptance_criteria"]
            clean_dict = {k: parsed.get(k, "") for k in allowed_keys}

            logger.info("Agent 2 Tool 1: completed successfully")
            return clean_dict

        except Exception as e:
            logger.error(f"JSON parsing failed: {e}\nRaw response: {obj_text}")

            return {
                "refined_requirement": requirement
            }

    # No JSON found at all
    logger.error(f"No valid JSON object found in LLM response. Raw response: {response}")

    return {
        "refined_requirement": requirement
    }
