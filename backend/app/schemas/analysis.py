from pydantic import BaseModel, Field


class SceneAnalysis(BaseModel):
    scene_type: str = Field(description="Detected driving scene category.")
    key_objects: list[str] = Field(default_factory=list)
    issues: list[str] = Field(default_factory=list)
    missing_labels: list[str] = Field(default_factory=list)
    confidence: float = Field(ge=0.0, le=1.0)
    explanation: str
