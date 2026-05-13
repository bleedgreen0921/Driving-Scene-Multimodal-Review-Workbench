from app.schemas.analysis import ChannelizationAnalysis, ChannelizationModelOutput
from app.schemas.risk import FilterAction, RiskLevel
from app.services.risk_service import assess_risk, decide_filter_action
from app.services.rule_engine import derive_review_signals, validate_analysis


def _build_analysis(
    has_channelization: bool,
    reason: str,
    model_confidence: float | None = None,
) -> ChannelizationAnalysis:
    """构造一条完整的 V 形导流区分析对象，减少测试样例重复代码。"""
    model_output = ChannelizationModelOutput(
        has_channelization=has_channelization,
        reason=reason,
    )
    return ChannelizationAnalysis(
        model_output=model_output,
        review_signals=derive_review_signals(model_output),
        model_confidence=model_confidence,
    )


def test_valid_channelization_positive_is_kept() -> None:
    """符合严格规范的 V 形导流区正样本应该进入挖掘结果。"""
    analysis = _build_analysis(
        has_channelization=True,
        reason=(
            "图像中部可见由两侧清晰边界和内部导流线构成的完整楔形导流区，"
            "该区域对主路与分流车道形成明确分隔，整体为 V形且不是 Y形或多分叉结构。"
        ),
    )

    validation = validate_analysis(analysis)
    risk = assess_risk(analysis, validation)
    decision = decide_filter_action(analysis, validation, risk)

    assert validation.rule_pass is True
    assert risk.risk_level == RiskLevel.low
    assert decision.action == FilterAction.keep


def test_positive_without_v_shape_evidence_goes_to_review() -> None:
    """模型判 true 但 reason 没有说明 V 形结构时，应该进入人工复核。"""
    analysis = _build_analysis(
        has_channelization=True,
        reason="图像中有导流线和道路边界，对车辆形成一定引导作用。",
    )

    validation = validate_analysis(analysis)
    risk = assess_risk(analysis, validation)
    decision = decide_filter_action(analysis, validation, risk)

    assert "v_shape_evidence_missing" in validation.rule_violations
    assert risk.risk_level == RiskLevel.needs_human_review
    assert decision.action == FilterAction.review


def test_positive_with_y_shape_risk_goes_to_review() -> None:
    """模型判 true 但 reason 暗示 Y 形或多分叉时，应该进入人工复核。"""
    analysis = _build_analysis(
        has_channelization=True,
        reason=(
            "图像中存在完整 V形导流区域，但整体道路组织连接三个方向，"
            "更接近 Y形多分叉结构。"
        ),
    )

    validation = validate_analysis(analysis)
    risk = assess_risk(analysis, validation)
    decision = decide_filter_action(analysis, validation, risk)

    assert "y_or_multi_fork_conflict" in validation.rule_violations
    assert risk.risk_level == RiskLevel.needs_human_review
    assert decision.action == FilterAction.review


def test_clear_channelization_negative_is_discarded() -> None:
    """明确不满足规范的负样本应该被前置过滤。"""
    analysis = _build_analysis(
        has_channelization=False,
        reason="图像中仅有普通车道线和路肩边界，未形成完整 V形导流区，也没有明确导流关系。",
    )

    validation = validate_analysis(analysis)
    risk = assess_risk(analysis, validation)
    decision = decide_filter_action(analysis, validation, risk)

    assert validation.rule_pass is True
    assert risk.risk_level == RiskLevel.low
    assert decision.action == FilterAction.discard
