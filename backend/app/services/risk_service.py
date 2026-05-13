from app.schemas.analysis import SceneAnalysis
from app.schemas.risk import RiskLevel, RiskResult, ValidationResult


def assess_risk(analysis: SceneAnalysis, validation: ValidationResult) -> RiskResult:
    reasons: list[str] = []

    if analysis.confidence < 0.5:
        reasons.append("low_confidence")
    if validation.rule_violations:
        reasons.extend(validation.rule_violations)
    if analysis.missing_labels:
        reasons.append("missing_labels")

    if reasons:
        return RiskResult(risk_level=RiskLevel.needs_human_review, reasons=reasons)

    return RiskResult(risk_level=RiskLevel.low, reasons=[])
