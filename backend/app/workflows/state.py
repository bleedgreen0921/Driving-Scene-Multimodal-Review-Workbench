from typing import TypedDict


class ReviewWorkflowState(TypedDict, total=False):
    """后续 LangGraph 各节点之间传递的共享状态。"""

    task_id: str
    image_path: str
    context_text: str | None
    rule_profile: str
    analysis: dict
    validation: dict
    risk: dict
    filter_decision: dict
    review_status: str
