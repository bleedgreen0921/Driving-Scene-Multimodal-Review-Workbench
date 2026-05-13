from pydantic import BaseModel, Field

from app.schemas.analysis import SceneAnalysis
from app.schemas.review import ReviewStatus
from app.schemas.risk import RiskResult, ValidationResult


class SampleInput(BaseModel):
    sample_id: str
    image_path: str
    context_text: str | None = None
    rule_profile: str = "default_driving_scene"


class AnalyzeSampleResponse(BaseModel):
    task_id: str
    filename: str
    rule_profile: str
    analysis: SceneAnalysis
    validation: ValidationResult
    risk: RiskResult
    review_status: ReviewStatus = ReviewStatus.pending
    metadata: dict[str, str | None] = Field(default_factory=dict)
