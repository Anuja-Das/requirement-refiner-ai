"""
Tool: Acceptance Criteria Generator Tool
Generates acceptance criteria for a given requirement text.
"""

import re
import logging, json
from app.core.llm_adapter import llm
from app.core.prompts import acceptance_criteria_gen_prompt

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# --- FIX: Extract first complete JSON array using balanced brackets ---
def extract_json_array(text: str) -> str:
    """
    Extracts the first complete JSON array using a [ ] bracket counter.
    """
    start = text.find('[')
    if start == -1:
        return ""

    count = 0
    for i in range(start, len(text)):
        if text[i] == '[':
            count += 1
        elif text[i] == ']':
            count -= 1
            if count == 0:
                return text[start:i+1]

    return ""  # No complete array found


# --- Main tool ---
def generate_acceptance_criteria(refined_requirement: str) -> list[str]:
    logger.info("Agent 2 Tool 2: started")

    prompt = acceptance_criteria_gen_prompt.format(refined=refined_requirement)
    response = llm.generate(prompt)

    # Step 1: Extract array
    arr_text = extract_json_array(response)

    if arr_text:
        # Clean control characters
        arr_text_clean = re.sub(r'[\x00-\x1F\x7F]', '', arr_text)

        try:
            parsed = json.loads(arr_text_clean)

            if isinstance(parsed, list):
                logger.info("Agent 2 Tool 2: completed successfully")

                # If dicts → extract 'description'; if strings → return strings
                return [
                    item.get('description', str(item)) if isinstance(item, dict) else str(item)
                    for item in parsed
                ]

        except Exception as e:
            logger.error(f"JSON parsing failed: {e}\nRaw response: {arr_text}")

            # Try regex recovery
            descriptions = re.findall(r'"description"\s*:\s*"(.*?)"', arr_text_clean)
            if descriptions:
                logger.info("Recovered acceptance criteria from malformed JSON.")
                return descriptions

    # No valid JSON found
    logger.error(f"No valid JSON array found in LLM response. Raw response: {response}")

    # Fallback
    return [
        f"System accepts files that conform to the expected format for {refined_requirement}",
        "System returns appropriate error messages on invalid input"
    ]
