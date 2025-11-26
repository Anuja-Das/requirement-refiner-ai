from typing import List, Optional

from pydantic import BaseModel, Field


class SynthesizeRequest(BaseModel):
    transcripts: List[str]
    constraints: Optional[str] = ""
    backlog: Optional[str] = ""


class AnalyzerOutput(BaseModel):
    ambiguous_phrases: List[str] = Field(default_factory=list)
    missing_information: List[str] = Field(default_factory=list)


class AcceptanceCriteriaItem(BaseModel):
    criterion: str


class FinalRequirement(BaseModel):
    refined_requirement: str
    acceptance_criteria: List[str]
