# API 设计草案

第一版 API 以单样本闭环为主，批量评测和人工复核随后补齐。

## Health

```http
GET /api/health
```

用于检查后端服务是否启动。

## Samples

```http
POST /api/samples/analyze
Content-Type: multipart/form-data
```

请求字段：

- `image`: 道路场景图片。
- `context_text`: 可选，上下文、任务说明或已有模型输出。
- `rule_profile`: 可选，规则模板名称，默认 `default_driving_scene`。

响应字段：

- `task_id`
- `analysis`
- `validation`
- `risk`
- `filter_decision`
- `review_status`

`analysis.diversion_type` 使用粗粒度导流分类：

- `split`: 分流导流
- `merge`: 合流导流
- `non_diversion`: 非导流
- `uncertain`: 疑似或无法判断

`filter_decision.action` 用于数据挖掘前置过滤：

- `keep`: 高置信导流样本，进入后续挖掘结果。
- `review`: 低置信、冲突或证据不足，进入人工复核。
- `discard`: 高置信非导流样本，过滤掉。

## Reviews

```http
GET /api/reviews/pending
POST /api/reviews/{task_id}
```

复核动作：

- `approve`
- `edit`
- `reject`
- `send_back_for_analysis`

## Evaluations

```http
POST /api/evaluations/runs
GET /api/evaluations/runs/{run_id}
```

用于创建批量评测任务和查询评测结果。
