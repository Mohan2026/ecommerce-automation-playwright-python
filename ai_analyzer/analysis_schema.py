
from typing import Literal

from pydantic import BaseModel, Field


class PossibleCause(BaseModel):
    cause: str
    evidence: str
    confidence: Literal["low", "medium", "high"]


class FailureAnalysis(BaseModel):
    failure_summary: str
    failure_category: Literal[
        "application_defect",
        "test_automation_defect",
        "test_data_or_environment",
        "unknown",
    ]
    possible_causes: list[PossibleCause]
    investigation_steps: list[str]
    missing_information: list[str]
