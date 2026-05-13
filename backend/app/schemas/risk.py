from enum import StrEnum

from pydantic import BaseModel, Field


class RiskLevel(StrEnum):
    """用于判断样本是否需要人工复核的风险等级。"""

    low = "low"
    medium = "medium"
    high = "high"
    needs_human_review = "needs_human_review"


class FilterAction(StrEnum):
    """经过规则核验和风险判定后的最终数据挖掘动作。"""

    keep = "keep"
    review = "review"
    discard = "discard"


class ValidationResult(BaseModel):
    """结构化模型输出对应的规则核验结果。"""

    schema_valid: bool = True
    rule_pass: bool = True
    rule_violations: list[str] = Field(default_factory=list)


class RiskResult(BaseModel):
    """根据模型置信度和规则违规情况得到的风险判定结果。"""

    risk_level: RiskLevel
    reasons: list[str] = Field(default_factory=list)


class FilterDecision(BaseModel):
    """前置过滤流程使用的最终 keep/review/discard 决策。"""

    action: FilterAction
    reasons: list[str] = Field(default_factory=list)
