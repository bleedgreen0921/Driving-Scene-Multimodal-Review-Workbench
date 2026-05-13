from pydantic import BaseModel, Field

from app.schemas.analysis import ChannelizationAnalysis
from app.schemas.review import ReviewStatus
from app.schemas.risk import FilterDecision, RiskResult, ValidationResult


class SampleInput(BaseModel):
    """单个本地或上传样本进入流程时所需的元数据。"""

    sample_id: str
    image_path: str
    context_text: str | None = None
    rule_profile: str = "default_v_channelization"


class AnalyzeSampleResponse(BaseModel):
    """单样本分析接口返回的完整响应。"""

    task_id: str
    filename: str
    rule_profile: str
    analysis: ChannelizationAnalysis
    validation: ValidationResult
    risk: RiskResult
    filter_decision: FilterDecision
    review_status: ReviewStatus = ReviewStatus.pending
    metadata: dict[str, str | None] = Field(default_factory=dict)
