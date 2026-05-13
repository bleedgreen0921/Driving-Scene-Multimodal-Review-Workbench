# backend/app/api 分析

本文档用于记录 `backend/app/api` 目录的当前设计、职责边界和后续扩展方向。

## 1. API 层定位

`backend/app/api` 是 FastAPI 的 HTTP 入口层。

它主要负责：

- 接收 HTTP 请求。
- 声明接口路径、请求参数和响应模型。
- 调用 service 层完成业务逻辑。
- 将 service 层结果返回给前端、评测脚本或其他调用方。

它不应该负责：

- 直接调用模型。
- 编写规则核验逻辑。
- 编写风险判定逻辑。
- 直接处理数据库细节。
- 编写复杂工作流编排。

当前项目推荐的分层边界是：

```text
api 层：接收 HTTP 请求，声明入参和响应模型
schemas 层：定义输入输出数据结构
services 层：执行业务逻辑
storage 层：保存和读取数据
workflows 层：后续编排多步骤流程
```

## 2. 当前目录结构

```text
backend/app/api/
├── __init__.py
└── routes/
    ├── __init__.py
    ├── health.py
    └── samples.py
```

当前真正包含接口逻辑的是：

- `backend/app/api/routes/health.py`
- `backend/app/api/routes/samples.py`

路由注册发生在 `backend/app/main.py`：

```python
app.include_router(health.router, prefix="/api")
app.include_router(samples.router, prefix="/api")
```

因此当前最终接口路径是：

```text
GET  /api/health
POST /api/samples/analyze
```

## 3. health.py 分析

`health.py` 提供健康检查接口：

```python
@router.get("/health")
async def health_check() -> dict[str, str]:
    """返回最小健康检查结果，用于本地开发和 CI。"""
    return {"status": "ok"}
```

最终路径：

```text
GET /api/health
```

这个接口的作用是确认：

- 后端服务可以启动。
- FastAPI app 可以创建。
- 路由注册正常。
- 测试客户端可以访问服务。

该接口没有业务逻辑，是本地调试、CI、部署健康检查中最基础的接口。

对应测试位于 `backend/tests/test_health.py`：

```python
response = client.get("/api/health")

assert response.status_code == 200
assert response.json() == {"status": "ok"}
```

## 4. samples.py 分析

`samples.py` 是当前最核心的业务 API 入口。

文件中的 router 定义：

```python
router = APIRouter(prefix="/samples", tags=["samples"])
```

这里的 `prefix="/samples"` 会和 `main.py` 中的 `prefix="/api"` 叠加，所以最终路径是：

```text
POST /api/samples/analyze
```

接口定义：

```python
@router.post("/analyze", response_model=AnalyzeSampleResponse)
async def analyze_sample(
    image: UploadFile = File(...),
    context_text: str | None = Form(default=None),
    rule_profile: str = Form(default="default_v_channelization"),
) -> AnalyzeSampleResponse:
    """使用当前 mock 流程分析一张上传的道路图像。"""
    return analyze_sample_mock(
        filename=image.filename or "uploaded_image",
        context_text=context_text,
        rule_profile=rule_profile,
    )
```

### 4.1 请求参数

`image: UploadFile = File(...)`

表示接口要求上传一个图片文件。`...` 表示该字段必填。

`context_text: str | None = Form(default=None)`

表示可以额外传入文本上下文，例如：

- 任务说明。
- 样本来源。
- 现有模型输出。
- 人工备注。

`rule_profile: str = Form(default="default_v_channelization")`

表示默认使用 V 形导流区规则模板。

### 4.2 响应模型

接口声明了：

```python
response_model=AnalyzeSampleResponse
```

这意味着 FastAPI 会使用 Pydantic 对返回结果进行校验和序列化。

当前响应模型定义在 `backend/app/schemas/sample.py`：

```python
class AnalyzeSampleResponse(BaseModel):
    """单样本分析接口返回的完整响应。"""

    task_id: str
    filename: str
    rule_profile: str
    analysis: ChannelizationAnalysis
    validation: ValidationResult
    risk: RiskResult
    filter_decision: FilterDecision
    review_status: ReviewStatus = ReviewStatus.pending
    metadata: dict[str, str | None] = Field(default_factory=dict)
```

该响应体现了当前项目的核心流程：

```text
上传样本
-> 模型原始输出
-> 外部复核信号
-> 规则核验
-> 风险判定
-> keep/review/discard 筛选决策
```

### 4.3 当前调用链

`samples.py` 当前调用的是：

```python
analyze_sample_mock(...)
```

该函数位于 `backend/app/services/analysis_service.py`。

当前调用链是：

```text
POST /api/samples/analyze
-> analyze_sample()
-> analyze_sample_mock()
-> ChannelizationModelOutput
-> derive_review_signals()
-> validate_analysis()
-> assess_risk()
-> decide_filter_action()
-> AnalyzeSampleResponse
```

注意：当前还没有真正读取图片内容，也没有接入微调模型。

现在的 API 层只把以下信息传递给 service 层：

- 上传文件名。
- 可选上下文文本。
- 规则模板名称。

## 5. 当前请求与响应示例

请求形式：

```http
POST /api/samples/analyze
Content-Type: multipart/form-data

image=<上传图片>
context_text=可选文本
rule_profile=default_v_channelization
```

当前响应结构大致为：

```json
{
  "task_id": "sample_xxxxxxxx",
  "filename": "road.jpg",
  "rule_profile": "default_v_channelization",
  "analysis": {
    "model_output": {
      "has_channelization": false,
      "reason": "当前结果来自占位流程，尚未接入 V 形导流区微调模型，不能确认存在完整 V 形导流区。"
    },
    "review_signals": {
      "contour_complete": false,
      "v_shape_visible": true,
      "y_or_multi_fork_risk": false,
      "evidence_sufficient": true,
      "reason_quality_pass": true,
      "extracted_evidence": ["v_shape_visible", "diversion_evidence_sufficient"],
      "risk_hints": []
    },
    "model_confidence": 0.3
  },
  "validation": {
    "schema_valid": true,
    "rule_pass": false,
    "rule_violations": ["confidence_below_default_threshold"]
  },
  "risk": {
    "risk_level": "medium",
    "reasons": ["confidence_below_default_threshold"]
  },
  "filter_decision": {
    "action": "review",
    "reasons": ["confidence_below_default_threshold"]
  },
  "review_status": "pending",
  "metadata": {
    "context_text": "可选文本"
  }
}
```

## 6. 当前设计优点

### 6.1 API 层保持轻量

`samples.py` 没有写模型推理、规则核验或风险判定逻辑。

这符合后端分层原则：

- API 层负责 HTTP。
- service 层负责业务。
- schema 层负责数据结构。

### 6.2 响应结构清晰

`AnalyzeSampleResponse` 明确表达了单样本分析闭环中的关键结果：

- `analysis`
- `validation`
- `risk`
- `filter_decision`
- `review_status`

后续前端页面和批量评测脚本可以直接围绕这些字段开发。

### 6.3 图片上传方式合理

FastAPI 中使用：

```python
image: UploadFile = File(...)
```

适合处理上传图片，比直接把图片放在 JSON body 中更合适。

### 6.4 默认规则模板明确

当前默认规则模板是：

```python
default_v_channelization
```

这与项目当前目标一致：围绕现有 V 形导流区微调规范构建外部增强框架。

## 7. 当前不足

### 7.1 尚未保存图片

当前 API 只使用了：

```python
image.filename
```

还没有把图片保存到 `data/uploads`。

后续需要增加：

- 文件保存路径。
- 文件唯一命名。
- 文件大小限制。
- 上传失败处理。

### 7.2 尚未校验文件类型

目前接口没有限制上传内容类型。

后续应校验：

- `image/jpeg`
- `image/png`
- `image/webp`

避免非图片文件进入模型流程。

### 7.3 尚未接入真实模型

当前调用的是：

```python
analyze_sample_mock()
```

后续需要替换或扩展为：

```text
真实微调模型推理
-> 解析 has_channelization + reason
-> 外部规则增强
```

### 7.4 尚未接入持久化

当前没有保存：

- 样本记录。
- 上传图片路径。
- 模型输出。
- 规则核验结果。
- 人工复核状态。

后续应接入 `backend/app/storage`。

### 7.5 尚未提供任务查询接口

当前只有同步分析接口。

后续建议增加：

```text
GET /api/samples/{task_id}
```

用于查看某个样本的历史分析结果。

### 7.6 错误处理还不完整

后续需要处理：

- 文件为空。
- 文件格式不支持。
- 规则模板不存在。
- 模型调用失败。
- 模型输出不是合法 JSON。
- 数据库写入失败。

## 8. 后续扩展方向

### 8.1 样本相关接口

```text
POST /api/samples/analyze
GET  /api/samples/{task_id}
GET  /api/samples
```

### 8.2 人工复核接口

```text
GET  /api/reviews/pending
POST /api/reviews/{task_id}
```

### 8.3 批量评测接口

```text
POST /api/evaluations/runs
GET  /api/evaluations/runs/{run_id}
```

## 9. 学习重点

学习 `backend/app/api` 时，重点不是背 FastAPI 语法，而是理解 API 层的职责边界。

以 `samples.py` 为例，它做了三件事：

1. 声明接口路径：

```python
@router.post("/analyze", response_model=AnalyzeSampleResponse)
```

2. 声明请求参数：

```python
image: UploadFile = File(...)
context_text: str | None = Form(default=None)
rule_profile: str = Form(default="default_v_channelization")
```

3. 调用 service 层：

```python
return analyze_sample_mock(...)
```

这正是后端工程中的关键习惯：

```text
API 层要薄，业务逻辑要下沉到 service 层。
```
