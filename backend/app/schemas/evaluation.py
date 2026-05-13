from pydantic import BaseModel, Field


class EvaluationSummary(BaseModel):
    total_samples: int = 0
    schema_valid_rate: float = 0.0
    field_completeness_rate: float = 0.0
    rule_conflict_rate: float = 0.0
    human_review_rate: float = 0.0
    bad_cases: list[str] = Field(default_factory=list)
