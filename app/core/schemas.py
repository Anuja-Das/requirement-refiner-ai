from typing import List

from pydantic import BaseModel, Field


class AnalyzerOutput(BaseModel):
    ambiguous_phrases: List[str] = Field(default_factory=list)
    missing_information: List[str] = Field(default_factory=list)


class FinalRequirement(BaseModel):
    refined_requirement: str
    acceptance_criteria: List[str]
