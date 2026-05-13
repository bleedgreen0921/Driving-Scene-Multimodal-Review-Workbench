from fastapi.testclient import TestClient

from app.main import create_app


def test_health_check() -> None:
    """健康检查接口应该能证明 API 应用可以正常启动。"""
    client = TestClient(create_app())

    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
