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
- `review_status`

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
