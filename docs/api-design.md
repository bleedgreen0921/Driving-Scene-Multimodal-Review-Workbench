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
- `rule_profile`: 可选，规则模板名称，默认 `default_v_channelization`。

响应字段：

- `task_id`
- `analysis`
- `validation`
- `risk`
- `filter_decision`
- `review_status`

`analysis.model_output` 保持和既有微调标注规范一致：

- `has_channelization`: 是否存在严格意义上的 V 形导流区。
- `reason`: 模型基于图像可见内容给出的判断理由。

`analysis.review_signals` 是外部增强框架派生的复核信号，不要求模型直接输出：

- `contour_complete`: reason 是否支撑轮廓完整可见。
- `v_shape_visible`: reason 是否明确说明 V 形、楔形或三角夹角结构。
- `y_or_multi_fork_risk`: reason 是否暗示 Y 形、三叉或多分叉风险。
- `evidence_sufficient`: reason 是否提供足够导流关系和视觉证据。

`filter_decision.action` 用于数据挖掘前置过滤：

- `keep`: 通过外部核验的 V 形导流区正样本，进入后续挖掘结果。
- `review`: 低置信、reason 不充分、疑似 Y 形/多分叉或规则冲突样本，进入人工复核。
- `discard`: 明确不满足 V 形导流区规范的负样本，过滤掉。

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
