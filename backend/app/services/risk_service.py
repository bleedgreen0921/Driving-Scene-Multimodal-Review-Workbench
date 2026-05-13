from app.schemas.analysis import DiversionType, SceneAnalysis
from app.schemas.risk import (
    FilterAction,
    FilterDecision,
    RiskLevel,
    RiskResult,
    ValidationResult,
)


def assess_risk(analysis: SceneAnalysis, validation: ValidationResult) -> RiskResult:
    """将规则核验结果和模型证据转换为复核风险等级。"""
    reasons: list[str] = []

    if analysis.confidence < 0.5:
        reasons.append("low_confidence")
    if validation.rule_violations:
        reasons.extend(validation.rule_violations)
    if analysis.negative_evidence:
        reasons.append("negative_evidence_present")

    # 只要存在明确冲突或弱信号，就优先交给人工复核。
    if reasons:
        return RiskResult(risk_level=RiskLevel.needs_human_review, reasons=reasons)

    if analysis.diversion_type == DiversionType.uncertain:
        return RiskResult(
            risk_level=RiskLevel.medium,
            reasons=["diversion_type_uncertain"],
        )

    return RiskResult(risk_level=RiskLevel.low, reasons=[])


def decide_filter_action(
    analysis: SceneAnalysis,
    validation: ValidationResult,
    risk: RiskResult,
) -> FilterDecision:
    """为单个样本选择最终数据挖掘动作。"""
    # 规则未通过或风险不低时，不自动保留，也不自动丢弃。
    if not validation.rule_pass or risk.risk_level != RiskLevel.low:
        return FilterDecision(
            action=FilterAction.review,
            reasons=risk.reasons or validation.rule_violations,
        )

    # 高置信度的分流/合流样本是数据挖掘所需的有效正样本。
    if (
        analysis.diversion_type in {DiversionType.split, DiversionType.merge}
        and analysis.confidence >= 0.75
    ):
        return FilterDecision(
            action=FilterAction.keep,
            reasons=["high_confidence_diversion_scene"],
        )

    # 高置信度的非导流样本可以提前过滤，减少后续处理数据量。
    if (
        analysis.diversion_type == DiversionType.non_diversion
        and analysis.confidence >= 0.7
    ):
        return FilterDecision(
            action=FilterAction.discard,
            reasons=["high_confidence_non_diversion_scene"],
        )

    # 边界样本保留复核入口，以保护稀疏导流数据的召回率。
    return FilterDecision(
        action=FilterAction.review,
        reasons=["confidence_or_evidence_not_decisive"],
    )
