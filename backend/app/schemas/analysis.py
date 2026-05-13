from pydantic import BaseModel, Field


class ChannelizationModelOutput(BaseModel):
    """现有微调模型的原始输出格式，保持与标注规范一致。"""

    has_channelization: bool = Field(
        description="图像中是否存在严格意义上的 V 形导流区。"
    )
    reason: str = Field(
        description="模型基于图像可见内容给出的判断理由。"
    )


class ChannelizationReviewSignals(BaseModel):
    """外部增强框架从模型 reason 中派生的复核信号。

    这些字段不要求微调模型直接输出，只用于后续规则核验、风险判定
    和人工复核排序，避免改动已有微调数据格式。
    """

    contour_complete: bool | None = Field(
        default=None,
        description="reason 是否支持“轮廓完整可见”的判断。",
    )
    v_shape_visible: bool | None = Field(
        default=None,
        description="reason 是否明确提到 V 形、楔形或三角夹角结构。",
    )
    y_or_multi_fork_risk: bool | None = Field(
        default=None,
        description="reason 是否存在 Y 形、三叉或多分叉风险。",
    )
    evidence_sufficient: bool | None = Field(
        default=None,
        description="reason 是否提供足够的导流关系和视觉证据。",
    )
    reason_quality_pass: bool = Field(
        description="reason 是否达到最基本的长度和可复核性要求。"
    )
    extracted_evidence: list[str] = Field(
        default_factory=list,
        description="从 reason 中抽取到的正向证据标签。",
    )
    risk_hints: list[str] = Field(
        default_factory=list,
        description="从 reason 中抽取到的风险提示标签。",
    )


class ChannelizationAnalysis(BaseModel):
    """外部框架使用的完整分析对象。

    `model_output` 是已有微调模型的原始结果；`review_signals` 是外部框架
    为了质检和复核而派生的辅助信息。
    """

    model_output: ChannelizationModelOutput
    review_signals: ChannelizationReviewSignals
    model_confidence: float | None = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="可选模型置信度；如果现有推理流程没有该值，可以为空。",
    )
