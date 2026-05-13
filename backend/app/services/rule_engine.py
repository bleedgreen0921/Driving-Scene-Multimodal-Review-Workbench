from app.schemas.analysis import SceneAnalysis
from app.schemas.risk import ValidationResult


def validate_analysis(analysis: SceneAnalysis) -> ValidationResult:
    violations: list[str] = []

    if not analysis.scene_type:
        violations.append("scene_type_missing")
    if analysis.confidence < 0.5:
        violations.append("confidence_below_default_threshold")
    if not analysis.explanation.strip():
        violations.append("explanation_missing")

    return ValidationResult(
        schema_valid=True,
        rule_pass=len(violations) == 0,
        rule_violations=violations,
    )
