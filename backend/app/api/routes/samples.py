from fastapi import APIRouter, File, Form, UploadFile

from app.schemas.sample import AnalyzeSampleResponse
from app.services.analysis_service import analyze_sample_mock

router = APIRouter(prefix="/samples", tags=["samples"])


@router.post("/analyze", response_model=AnalyzeSampleResponse)
async def analyze_sample(
    image: UploadFile = File(...),
    context_text: str | None = Form(default=None),
    rule_profile: str = Form(default="default_driving_scene"),
) -> AnalyzeSampleResponse:
    return analyze_sample_mock(
        filename=image.filename or "uploaded_image",
        context_text=context_text,
        rule_profile=rule_profile,
    )
