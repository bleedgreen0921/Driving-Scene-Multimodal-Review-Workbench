from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/health")
async def health_check() -> dict[str, str]:
    """返回最小健康检查结果，用于本地开发和 CI。"""
    return {"status": "ok"}
