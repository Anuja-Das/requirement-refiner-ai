"""
Agent A: Requirements Analyzer Agent
Runs Ambiguity Detector + Missing Info Extractor and writes analysis_output.json
"""

from app.tools.ambiguity_detector_tool import detect_ambiguities
from app.tools.missing_info_extractor_tool import extract_missing_info
from app.core.schemas import AnalyzerOutput
import json, os , logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Setup the data directory and the output file path
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", "data")
DATA_DIR = os.path.normpath(DATA_DIR)
os.makedirs(DATA_DIR, exist_ok=True)
ANALYSIS_PATH = os.path.join(DATA_DIR, "analysis_output.json")

# Main function for analyzing requirements
# Accepts a requirement text, runs ambiguity detection and missing info extraction tools,
# saves the analysis to a JSON file,
# and returns an AnalyzerOutput model instance.
def analyze(requirement_text: str) -> AnalyzerOutput:

    logger.info("Agent 1: started")

    # Run Ambiguity Detector Tool
    ambiguities = detect_ambiguities(requirement_text)

    # Run Missing Info Extractor Tool
    missing_info = extract_missing_info(requirement_text)

    # Create the analysis output model
    analysis_output = AnalyzerOutput(
        ambiguous_phrases=ambiguities,
        missing_information=missing_info
    )

    # Save the analysis output to a JSON file
    with open(ANALYSIS_PATH, "w", encoding="utf-8") as file:
        file.write(json.dumps(analysis_output.model_dump(), indent=4))

    logger.info(f"Agent 1: completed successfully")
    return analysis_output