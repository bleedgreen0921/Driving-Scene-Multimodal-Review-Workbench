from uuid import uuid4

from app.schemas.analysis import SceneAnalysis
from app.schemas.review import ReviewStatus
from app.schemas.risk import RiskResult, ValidationResult
from app.schemas.sample import AnalyzeSampleResponse
from app.services.risk_service import assess_risk
from app.services.rule_engine import validate_analysis


def analyze_sample_mock(
    filename: str,
    context_text: str | None,
    rule_profile: str,
) -> AnalyzeSampleResponse:
    analysis = SceneAnalysis(
        scene_type="unknown",
        key_objects=[],
        issues=["mock_analysis_not_connected_to_model"],
        missing_labels=[],
        confidence=0.3,
        explanation="Placeholder response until multimodal model integration is implemented.",
    )
    validation: ValidationResult = validate_analysis(analysis)
    risk: RiskResult = assess_risk(analysis, validation)

    return AnalyzeSampleResponse(
        task_id=f"sample_{uuid4().hex[:8]}",
        filename=filename,
        rule_profile=rule_profile,
        analysis=analysis,
        validation=validation,
        risk=risk,
        review_status=ReviewStatus.pending,
        metadata={"context_text": context_text},
    )
