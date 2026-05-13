from uuid import uuid4

from app.schemas.analysis import ChannelizationAnalysis, ChannelizationModelOutput
from app.schemas.review import ReviewStatus
from app.schemas.risk import FilterDecision, RiskResult, ValidationResult
from app.schemas.sample import AnalyzeSampleResponse
from app.services.risk_service import assess_risk, decide_filter_action
from app.services.rule_engine import derive_review_signals, validate_analysis


def analyze_sample_mock(
    filename: str,
    context_text: str | None,
    rule_profile: str,
) -> AnalyzeSampleResponse:
    """在接入真实模型前，运行占位版单样本分析流程。

    mock 会刻意返回低置信度的不确定结果，方便早期验证规则核验、
    风险判定和人工复核分支是否能正常工作。
    """
    model_output = ChannelizationModelOutput(
        has_channelization=False,
        reason="当前结果来自占位流程，尚未接入 V 形导流区微调模型，不能确认存在完整 V 形导流区。",
    )
    analysis = ChannelizationAnalysis(
        model_output=model_output,
        review_signals=derive_review_signals(model_output),
        model_confidence=0.3,
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
