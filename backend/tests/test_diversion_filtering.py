from app.schemas.analysis import DiversionType, SceneAnalysis
from app.schemas.risk import FilterAction, RiskLevel
from app.services.risk_service import assess_risk, decide_filter_action
from app.services.rule_engine import validate_analysis


def test_high_confidence_split_diversion_is_kept() -> None:
    """高置信度分流导流预测应该进入挖掘正样本。"""
    analysis = SceneAnalysis(
        is_diversion_scene=True,
        diversion_type=DiversionType.split,
        key_objects=["traffic_cone", "temporary_lane_marking"],
        visual_evidence=["cones guide vehicles away from the original lane"],
        negative_evidence=[],
        confidence=0.86,
        explanation="The scene shows cones splitting traffic into a guided path.",
    )

    validation = validate_analysis(analysis)
    risk = assess_risk(analysis, validation)
    decision = decide_filter_action(analysis, validation, risk)

    assert validation.rule_pass is True
    assert risk.risk_level == RiskLevel.low
    assert decision.action == FilterAction.keep


def test_uncertain_diversion_goes_to_review() -> None:
    """不确定且低置信度的样本应该进入人工复核。"""
    analysis = SceneAnalysis(
        is_diversion_scene=False,
        diversion_type=DiversionType.uncertain,
        key_objects=[],
        visual_evidence=[],
        negative_evidence=["visual evidence is not enough to confirm diversion"],
        confidence=0.42,
        explanation="The scene is unclear and needs human review.",
    )

    validation = validate_analysis(analysis)
    risk = assess_risk(analysis, validation)
    decision = decide_filter_action(analysis, validation, risk)

    assert validation.rule_pass is False
    assert "diversion_type_uncertain" in validation.rule_violations
    assert risk.risk_level == RiskLevel.needs_human_review
    assert decision.action == FilterAction.review


def test_high_confidence_non_diversion_is_discarded() -> None:
    """明确的非导流负样本应该在后续挖掘前被过滤。"""
    analysis = SceneAnalysis(
        is_diversion_scene=False,
        diversion_type=DiversionType.non_diversion,
        key_objects=["vehicle", "lane_marking"],
        visual_evidence=[],
        negative_evidence=["no cones, temporary signs, lane split, or merge pattern"],
        confidence=0.91,
        explanation="The road scene does not contain split or merge diversion evidence.",
    )

    validation = validate_analysis(analysis)
    risk = assess_risk(analysis, validation)
    decision = decide_filter_action(analysis, validation, risk)

    assert validation.rule_pass is True
    assert risk.risk_level == RiskLevel.low
    assert decision.action == FilterAction.discard


def test_diversion_flag_type_conflict_goes_to_review() -> None:
    """模型字段自相矛盾时，不应该自动保留或自动丢弃。"""
    analysis = SceneAnalysis(
        is_diversion_scene=False,
        diversion_type=DiversionType.merge,
        key_objects=["traffic_cone"],
        visual_evidence=["lanes appear to merge under cone guidance"],
        negative_evidence=[],
        confidence=0.8,
        explanation="The type says merge diversion but the diversion flag is false.",
    )

    validation = validate_analysis(analysis)
    risk = assess_risk(analysis, validation)
    decision = decide_filter_action(analysis, validation, risk)

    assert "diversion_flag_type_conflict" in validation.rule_violations
    assert risk.risk_level == RiskLevel.needs_human_review
    assert decision.action == FilterAction.review
