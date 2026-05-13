# Backend

FastAPI 后端服务，负责样本接入、多模态分析、规则核验、风险判定、人工复核和评测接口。

## 本地启动

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

服务启动后访问：

- `GET http://127.0.0.1:8000/api/health`
- `GET http://127.0.0.1:8000/docs`
