from enum import StrEnum

from pydantic import BaseModel, Field


class ReviewStatus(StrEnum):
    pending = "pending"
    approved = "approved"
    edited = "edited"
    rejected = "rejected"


class ReviewAction(StrEnum):
    approve = "approve"
    edit = "edit"
    reject = "reject"
    send_back_for_analysis = "send_back_for_analysis"


class ReviewRecord(BaseModel):
    task_id: str
    status: ReviewStatus = ReviewStatus.pending
    comment: str | None = None
    final_result: dict = Field(default_factory=dict)
