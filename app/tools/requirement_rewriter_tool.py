"""
Tool: Requirement Rewriter
Produces a concise, unambiguous, engineering-ready requirement
"""

import json, logging, re
from typing import Any
from app.llm_adapter import llm
from app.prompts import requirement_rewriter_prompt

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# This function rewrites a requirement to be clear and engineering-ready.
def rewrite_requirement(requirement: str, ambiguities: list = None, missing: list = None) -> dict[str, Any]:
    logger.info("Agent 2 Tool 1: started")

    # Use empty lists if ambiguities or missing info are not provided
    ambiguities = ambiguities or []
    missing = missing or []

    # Build a rich prompt for the LLM, including the original requirement and analysis results
    prompt = requirement_rewriter_prompt.format(
        requirement=requirement,
        ambiguities=json.dumps(ambiguities, indent=4),
        missing=json.dumps(missing, indent=4)
    )

    response = llm.generate(prompt)

    # Try to extract a JSON object from the LLM response
    start = response.find('{')
    end = response.find('}')
    if start != -1 and end != -1 and end > start:
        obj_text = response[start:end + 1]

        # Remove control characters that break JSON parsing
        obj_text_clean = re.sub(r'[\x00-\x1F\x7F]', '', obj_text)
        try:
            parsed = json.loads(obj_text_clean)

            # Only keep the expected keys: refined_requirement and notes
            clean_dict = {k: parsed.get(k, "") for k in ["refined_requirement", "notes"]}

            logger.info("Agent 2 Tool 1: completed successfully")
            return clean_dict
        except Exception as e:
            logger.error(f"JSON parsing failed: {e}\nRaw response: {obj_text}")

            # Fallback: Return a dict with the original requirement and an error note
            return {"refined_requirement": requirement, "notes": f"LLM output could not be parsed: {e}"}

    logger.error(f"No valid JSON object found in LLM response. Raw response: {response}")

    # Fallback: Return a dict with the original requirement and an error note
    return {"refined_requirement": requirement, "notes": "LLM did not return a valid JSON object."}