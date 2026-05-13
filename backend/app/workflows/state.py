from typing import TypedDict


class ReviewWorkflowState(TypedDict, total=False):
    task_id: str
    image_path: str
    context_text: str | None
    rule_profile: str
    analysis: dict
    validation: dict
    risk: dict
    review_status: str
