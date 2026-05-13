from app.schemas.analysis import DiversionType, SceneAnalysis
from app.schemas.risk import ValidationResult


def validate_analysis(analysis: SceneAnalysis) -> ValidationResult:
    """根据导流场景业务规则核验模型输出。"""
    violations: list[str] = []

    # 目标布尔标记和导流类型应该表达同一个判断。
    if (
        analysis.is_diversion_scene
        and analysis.diversion_type == DiversionType.non_diversion
    ):
        violations.append("diversion_flag_type_conflict")

    if (
        not analysis.is_diversion_scene
        and analysis.diversion_type in {DiversionType.split, DiversionType.merge}
    ):
        violations.append("diversion_flag_type_conflict")

    # 正向分流/合流预测必须有具体对象和视觉证据支撑。
    if analysis.diversion_type in {DiversionType.split, DiversionType.merge}:
        if not analysis.key_objects:
            violations.append("diversion_key_objects_missing")
        if not analysis.visual_evidence:
            violations.append("diversion_visual_evidence_missing")

    if analysis.diversion_type == DiversionType.uncertain:
        violations.append("diversion_type_uncertain")

    # 导流场景较稀少，低置信度样本不直接丢弃，而是进入复核保护召回。
    if analysis.confidence < 0.5:
        violations.append("confidence_below_default_threshold")

    # 面向人工复核的工具需要可解释性，过短解释视为弱证据。
    if len(analysis.explanation.strip()) < 12:
        violations.append("explanation_missing")

    return ValidationResult(
        schema_valid=True,
        rule_pass=len(violations) == 0,
        rule_violations=violations,
    )
