from enum import StrEnum

from pydantic import BaseModel, Field


class RiskLevel(StrEnum):
    low = "low"
    medium = "medium"
    high = "high"
    needs_human_review = "needs_human_review"


class ValidationResult(BaseModel):
    schema_valid: bool = True
    rule_pass: bool = True
    rule_violations: list[str] = Field(default_factory=list)


class RiskResult(BaseModel):
    risk_level: RiskLevel
    reasons: list[str] = Field(default_factory=list)
