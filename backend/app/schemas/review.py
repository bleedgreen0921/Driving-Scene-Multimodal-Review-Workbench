from enum import StrEnum

from pydantic import BaseModel, Field


class ReviewStatus(StrEnum):
    """样本当前的人工复核状态。"""

    pending = "pending"
    approved = "approved"
    edited = "edited"
    rejected = "rejected"


class ReviewAction(StrEnum):
    """复核人员可以对不确定或高风险样本执行的操作。"""

    approve = "approve"
    edit = "edit"
    reject = "reject"
    send_back_for_analysis = "send_back_for_analysis"


class ReviewRecord(BaseModel):
    """人工检查或修改模型判断后保存的复核结果。"""

    task_id: str
    status: ReviewStatus = ReviewStatus.pending
    comment: str | None = None
    final_result: dict = Field(default_factory=dict)
