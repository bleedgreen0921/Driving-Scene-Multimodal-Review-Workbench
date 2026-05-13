from uuid import uuid4

from app.schemas.analysis import DiversionType, SceneAnalysis
from app.schemas.review import ReviewStatus
from app.schemas.risk import FilterDecision, RiskResult, ValidationResult
from app.schemas.sample import AnalyzeSampleResponse
from app.services.risk_service import assess_risk, decide_filter_action
from app.services.rule_engine import validate_analysis


def analyze_sample_mock(
    filename: str,
    context_text: str | None,
    rule_profile: str,
) -> AnalyzeSampleResponse:
    """在接入真实模型前，运行占位版单样本分析流程。

    mock 会刻意返回低置信度的不确定结果，方便早期验证规则核验、
    风险判定和人工复核分支是否能正常工作。
    """
    analysis = SceneAnalysis(
        is_diversion_scene=False,
        diversion_type=DiversionType.uncertain,
        key_objects=[],
        visual_evidence=[],
        negative_evidence=["mock_analysis_not_connected_to_model"],
        confidence=0.3,
        explanation="Placeholder response until fine-tuned multimodal model integration is implemented.",
    )
    validation: ValidationResult = validate_analysis(analysis)
    risk: RiskResult = assess_risk(analysis, validation)
    filter_decision: FilterDecision = decide_filter_action(
        analysis=analysis,
        validation=validation,
        risk=risk,
    )

    return AnalyzeSampleResponse(
        task_id=f"sample_{uuid4().hex[:8]}",
        filename=filename,
        rule_profile=rule_profile,
        analysis=analysis,
        validation=validation,
        risk=risk,
        filter_decision=filter_decision,
        review_status=ReviewStatus.pending,
        metadata={"context_text": context_text},
    )
