from pydantic import BaseModel, Field


class EvaluationSummary(BaseModel):
    """批量筛选和 bad case 分析的聚合指标。"""

    total_samples: int = 0
    schema_valid_rate: float = 0.0
    field_completeness_rate: float = 0.0
    rule_conflict_rate: float = 0.0
    human_review_rate: float = 0.0
    keep_rate: float = 0.0
    discard_rate: float = 0.0
    precision: float | None = None
    recall: float | None = None
    f1: float | None = None
    bad_cases: list[str] = Field(default_factory=list)
