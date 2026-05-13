from app.schemas.analysis import (
    ChannelizationAnalysis,
    ChannelizationModelOutput,
    ChannelizationReviewSignals,
)
from app.schemas.risk import ValidationResult


V_SHAPE_TERMS = ("V形", "v形", "V 型", "v 型", "楔形", "三角", "夹角", "倒V")
DIVERSION_TERMS = ("导流", "分隔", "引导", "分流", "收口", "限制", "非通行", "过渡")
CONTOUR_TERMS = ("完整", "清晰", "可见", "轮廓", "边界", "开口方向")
INCOMPLETE_TERMS = ("不完整", "遮挡", "裁切", "出画", "模糊", "难以", "无法", "不可")
EXCLUDED_SHAPE_TERMS = ("Y形", "Y 型", "y形", "y 型", "三叉", "多分叉")
NEGATION_CUES = ("不是", "不属于", "未形成", "没有形成", "不存在", "非")


def derive_review_signals(
    model_output: ChannelizationModelOutput,
) -> ChannelizationReviewSignals:
    """从现有模型的 reason 中派生外部复核信号。"""
    reason = model_output.reason.strip()
    extracted_evidence: list[str] = []
    risk_hints: list[str] = []

    v_shape_visible = _contains_any(reason, V_SHAPE_TERMS)
    contour_complete = _contains_any(reason, CONTOUR_TERMS) and not _contains_any(
        reason,
        INCOMPLETE_TERMS,
    )
    evidence_sufficient = _contains_any(reason, DIVERSION_TERMS) and (
        v_shape_visible or contour_complete
    )
    y_or_multi_fork_risk = _mentions_excluded_shape_as_risk(reason)
    reason_quality_pass = len(reason) >= 12

    if v_shape_visible:
        extracted_evidence.append("v_shape_visible")
    if contour_complete:
        extracted_evidence.append("contour_complete")
    if evidence_sufficient:
        extracted_evidence.append("diversion_evidence_sufficient")
    if not reason_quality_pass:
        risk_hints.append("reason_too_short")
    if y_or_multi_fork_risk:
        risk_hints.append("y_or_multi_fork_mentioned")
    if _contains_any(reason, INCOMPLETE_TERMS):
        risk_hints.append("incomplete_or_unclear_contour_mentioned")

    return ChannelizationReviewSignals(
        contour_complete=contour_complete,
        v_shape_visible=v_shape_visible,
        y_or_multi_fork_risk=y_or_multi_fork_risk,
        evidence_sufficient=evidence_sufficient,
        reason_quality_pass=reason_quality_pass,
        extracted_evidence=extracted_evidence,
        risk_hints=risk_hints,
    )


def validate_analysis(analysis: ChannelizationAnalysis) -> ValidationResult:
    """根据 V 形导流区标注规范核验模型输出。"""
    violations: list[str] = []
    output = analysis.model_output
    signals = analysis.review_signals

    if not signals.reason_quality_pass:
        violations.append("reason_too_short")

    # 模型判 true 时，必须能在 reason 中看到 V 形、完整轮廓和导流证据。
    if output.has_channelization:
        if not signals.evidence_sufficient:
            violations.append("positive_evidence_insufficient")
        if not signals.v_shape_visible:
            violations.append("v_shape_evidence_missing")
        if not signals.contour_complete:
            violations.append("contour_completeness_missing")
        if signals.y_or_multi_fork_risk:
            violations.append("y_or_multi_fork_conflict")

    # 模型判 false 时，只要求 reason 能说明关键否定原因，不强行变更标签语义。
    if not output.has_channelization and not output.reason.strip():
        violations.append("negative_reason_missing")

    if analysis.model_confidence is not None and analysis.model_confidence < 0.5:
        violations.append("confidence_below_default_threshold")

    return ValidationResult(
        schema_valid=True,
        rule_pass=len(violations) == 0,
        rule_violations=violations,
    )


def _contains_any(text: str, terms: tuple[str, ...]) -> bool:
    """判断文本中是否包含任一关键词。"""
    return any(term in text for term in terms)


def _mentions_excluded_shape_as_risk(reason: str) -> bool:
    """判断 reason 是否把 Y 形或多分叉作为正向风险提到。

    如果 reason 写的是“不是 Y 形”或“不属于多分叉”，这是排除风险的证据，
    不应被当作冲突处理。
    """
    for term in EXCLUDED_SHAPE_TERMS:
        index = reason.find(term)
        while index != -1:
            context_start = max(0, index - 8)
            context = reason[context_start:index]
            if not any(cue in context for cue in NEGATION_CUES):
                return True
            index = reason.find(term, index + len(term))
    return False
