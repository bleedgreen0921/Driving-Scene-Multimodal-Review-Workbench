from app.schemas.analysis import ChannelizationAnalysis
from app.schemas.risk import (
    FilterAction,
    FilterDecision,
    RiskLevel,
    RiskResult,
    ValidationResult,
)


def assess_risk(
    analysis: ChannelizationAnalysis,
    validation: ValidationResult,
) -> RiskResult:
    """将规则核验结果和外部复核信号转换为风险等级。"""
    reasons: list[str] = []

    if validation.rule_violations:
        reasons.extend(validation.rule_violations)
    if analysis.review_signals.risk_hints:
        reasons.extend(analysis.review_signals.risk_hints)

    # 模型判 true 但外部规则发现问题时，优先进入人工复核保护 precision。
    if analysis.model_output.has_channelization and reasons:
        return RiskResult(risk_level=RiskLevel.needs_human_review, reasons=reasons)

    # 模型判 false 且 reason 质量较差时，也保留复核入口，避免漏掉稀疏正样本。
    if not analysis.model_output.has_channelization and reasons:
        return RiskResult(risk_level=RiskLevel.medium, reasons=reasons)

    return RiskResult(risk_level=RiskLevel.low, reasons=[])


def decide_filter_action(
    analysis: ChannelizationAnalysis,
    validation: ValidationResult,
    risk: RiskResult,
) -> FilterDecision:
    """为单个样本选择最终 keep/review/discard 动作。"""
    if risk.risk_level in {RiskLevel.high, RiskLevel.needs_human_review}:
        return FilterDecision(
            action=FilterAction.review,
            reasons=risk.reasons or validation.rule_violations,
        )

    if risk.risk_level == RiskLevel.medium:
        return FilterDecision(
            action=FilterAction.review,
            reasons=risk.reasons or ["medium_risk_sample"],
        )

    # 通过外部核验的 true 样本才进入导流区挖掘结果。
    if analysis.model_output.has_channelization and validation.rule_pass:
        return FilterDecision(
            action=FilterAction.keep,
            reasons=["validated_channelization_positive"],
        )

    # 明确判 false 且没有复核风险的样本直接过滤掉。
    if not analysis.model_output.has_channelization and validation.rule_pass:
        return FilterDecision(
            action=FilterAction.discard,
            reasons=["validated_channelization_negative"],
        )

    return FilterDecision(
        action=FilterAction.review,
        reasons=validation.rule_violations or ["validation_not_decisive"],
    )
