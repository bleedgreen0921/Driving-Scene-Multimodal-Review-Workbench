from app.workflows.state import ReviewWorkflowState


def build_review_workflow() -> None:
    """构建后续要接入的 LangGraph 工作流。

    第一版会串联模型分析、规则核验、风险判定和人工复核中断。
    """
    return None
