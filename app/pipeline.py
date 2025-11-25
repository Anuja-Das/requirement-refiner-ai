"""
Synchronous pipeline: runs Analyzer -> Refiner and returns final JSON result
"""
import os.path

from app.agents import analyzer_agent, refiner_agent
from app.schemas import SynthesizeRequest
import re, json

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
DATA_DIR = os.path.normpath(DATA_DIR)
os.makedirs(DATA_DIR, exist_ok=True)

def run_pipeline(req: SynthesizeRequest) -> dict:

    requirement_text = " ".join(req.transcripts).strip()

    if not requirement_text:
        requirement_text = "No requirement provided"

    # Agent A: Analyze
    analysis = analyzer_agent.analyze(requirement_text)

    # Agent B: Refine
    final = refiner_agent.refine(requirement_text)

    # Return a combined result (include analysis and final)
    result = {
        "analysis": json.loads(analysis.json()),
        "final_requirement": json.loads(final.json())
    }
    return result