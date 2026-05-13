from app.schemas.review import ReviewAction, ReviewRecord, ReviewStatus


def apply_review_action(
    task_id: str,
    action: ReviewAction,
    comment: str | None = None,
    final_result: dict | None = None,
) -> ReviewRecord:
    status_map = {
        ReviewAction.approve: ReviewStatus.approved,
        ReviewAction.edit: ReviewStatus.edited,
        ReviewAction.reject: ReviewStatus.rejected,
        ReviewAction.send_back_for_analysis: ReviewStatus.pending,
    }
    return ReviewRecord(
        task_id=task_id,
        status=status_map[action],
        comment=comment,
        final_result=final_result or {},
    )
