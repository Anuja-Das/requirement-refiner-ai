"""
Tool: Acceptance Criteria Generator Tool
Generates acceptance criteria for a given requirement text.
"""
import re

from app.llm_adapter import llm
from app.prompts import acceptance_criteria_gen_prompt
import logging, os, json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# This function generates acceptance criteria for the provided requirement text
def generate_acceptance_criteria(refined_requirement: str) -> list[str]:
    logger.info("Agent 2 Tool 2: started")

    prompt = acceptance_criteria_gen_prompt.format(refined=refined_requirement)

    response = llm.generate(prompt)

    # Remove code block markers and extra text if present
    response_clean = response
    # Remove triple backticks and 'json' markers
    response_clean = re.sub(r'```json```', '', response_clean)
    # Remove any text before the first '['
    first_bracket = response_clean.find('[')
    if first_bracket != -1:
        response_clean = response_clean[first_bracket:]
    # Remove any text after the last ']'
    last_bracket = response_clean.rfind(']')
    if last_bracket != -1:
        response_clean = response_clean[:last_bracket + 1]

    # Try to extract the first JSON array from the cleaned response
    start = response_clean.find('[')
    end = response_clean.find('[', start)
    if start != -1 and end != -1 and end > start:
        arr_text = response_clean[start:end + 1]
        arr_text_clean = re.sub(r'[\x00-\x1F\x7F]', '', arr_text)
        try:
            parsed = json.loads(arr_text_clean)

            # If the parsed result is a list, return it as acceptance criteria
            if isinstance(parsed, list):
                logger.info("Agent 2 Tool 2: completed successfully")
                # Extract 'description' if items are dicts, else str
                return [item.get('description', str(item)) if isinstance(item, dict) else str(item) for item in parsed]
        except Exception as e:
            logger.error(f"JSON parsing failed: {e}\nRaw response: {arr_text}")
            # Attempt to recover valid descriptions using regex
            descriptions = re.findall(r'"description"\s*:\s*"(.*?)"', arr_text_clean)
            if descriptions:
                logger.info("Recovered acceptance criteria from malformed JSON.")
                return descriptions

    logger.error(f"No valid JSON array found in LLM response. Raw response: {response}")

    # Fallback: Return a default acceptance criteria list
    return [
        f"System accepts files that conform to the expected format for {refined_requirement}",
        "System returns appropriate error messages on invalid input"
    ]