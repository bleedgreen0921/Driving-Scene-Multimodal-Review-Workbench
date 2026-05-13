from enum import StrEnum

from pydantic import BaseModel, Field


class DiversionType(StrEnum):
    """用于稀疏导流场景筛选的粗粒度分类。"""

    split = "split"
    merge = "merge"
    non_diversion = "non_diversion"
    uncertain = "uncertain"


class SceneAnalysis(BaseModel):
    """微调后的多模态模型需要输出的结构化分析结果。"""

    is_diversion_scene: bool = Field(
        description="样本是否可能属于导流场景。"
    )
    diversion_type: DiversionType = Field(
        description="微调模型使用的粗粒度导流类型。"
    )
    key_objects: list[str] = Field(
        default_factory=list,
        description="支撑分流或合流导流判断的关键对象。",
    )
    visual_evidence: list[str] = Field(
        default_factory=list,
        description="图像中观察到的正向视觉证据。",
    )
    negative_evidence: list[str] = Field(
        default_factory=list,
        description="不支持导流判断的反向视觉证据。",
    )
    confidence: float = Field(ge=0.0, le=1.0)
    explanation: str = Field(
        description="解释筛选判断的简短理由。"
    )
