# 项目开发规划

## 一、项目最终定位

### 项目名称

面向自动驾驶 / 道路场景的多模态质检、评测与人工复核工作台

### 一句话介绍

这是一个面向道路导流场景数据挖掘的多模态 AI 工作台：系统接收道路场景图像 / 图文样本后，使用微调后的多模态模型作为前置过滤器，判断样本是否属于分流导流或合流导流场景，并自动完成结构化结果生成、规则核验、风险判定和筛选决策；低置信度或高风险样本进入人工复核，同时支持批量评测、bad case 分析和结果回流。

### 项目范围

- 目标岗位：Applied AI / LLM 应用开发工程师、Multimodal AI Engineer / 多模态应用工程师
- 项目范围：只做求职可用版
- 能力重点：多模态输入、结构化输出、规则核验、风险判定、人工复核、批量评测、轻量前端
- 暂不做：复杂多 Agent、重前后端平台、推理基础设施、自研训练体系

### 为什么适合求职展示

项目把三类能力接在一起：

- 自动驾驶 / 道路导流场景理解
- 多模态模型微调与应用基础
- 工程化系统实现

它直接对应应用岗常见能力要求：多模态输入、tool / function calling、structured outputs、workflow orchestration、evaluation、service API。

## 二、岗位地图

### 1. Applied AI / LLM 应用开发工程师

这个项目最强对应的是这类岗位，因为它本质上是一个业务化的 LLM 工作流系统，而不是单纯模型实验。

项目可展示的能力点：

- 把模型封装成服务
- 设计结构化输出
- 编排多步骤工作流
- 做规则核验和错误回退
- 接入人工复核
- 构建批量评测与 bad case 闭环

### 2. Multimodal AI Engineer / 多模态应用工程师

项目天然是“图像 + 文本 + 规则”的多模态应用，而不是普通聊天系统。

项目可展示的能力点：

- 图像 / 图文输入处理
- 场景理解与字段抽取
- 视觉结果到结构化任务结果的映射
- 多模态错误分析

## 三、项目核心目标

这个项目不是“做一个能看图说话的系统”，而是要做一个可用于质检和复核的工作流系统。

最终要交付的能力：

1. 多模态输入：接收图像或图文样本。
2. 结构化输出：输出固定 schema，而不是自由文本。
3. 导流筛选：区分分流导流、合流导流、非导流和不确定样本。
4. 规则核验：用显式规则检查模型结果是否合规。
5. 风险判定：对不确定、冲突、缺字段、违规结果打风险标签。
6. 人工复核：高风险样本进入复核队列，由人工确认或修正。
7. 批量评测：支持离线样本集跑数，统计指标和 bad case。
8. 轻量前端：能上传样本、查看结果、复核样本、浏览批量统计。

## 四、推荐问题范围

问题要定义得足够窄，项目才会强。

### A. 分流导流场景筛选

给定道路场景图像，判断是否存在车流从主路径分离、车道被引导分叉、车辆被临时设施或道路结构导向不同方向的场景。

### B. 合流导流场景筛选

给定道路场景图像，判断是否存在多股车流合并、车道收束、入口匝道并入或临时导流设施引导车辆汇入的场景。

### C. 图像 + 规则联合审查

给定图像、任务文本和规则模板，输出结构化筛选结果、视觉证据、风险项和最终 keep / review / discard 决策。

## 五、架构选型

总体原则：工作流优先，模型嵌入其中；前端轻量，后端清晰；结构化优先，而不是聊天优先。

最终推荐选型：

- 编排层：LangGraph
- 模型接口层：Responses API
- 服务层：FastAPI + Pydantic
- 前端：轻量 React 工作台
- 存储层：SQLite 或 PostgreSQL，第一版优先 SQLite

### 模型接口层：Responses API

第一版最需要：

- 图像 + 文本输入
- function calling
- 多轮 / 状态化交互
- 统一接口

### 输出约束：Structured Outputs

这个项目如果没有结构化输出，价值会大幅下降。Structured Outputs 用于让结果符合定义好的 JSON Schema，避免缺 key、非法枚举、字段漂移。

### 编排层：LangGraph

项目不是单步问答，而是流程系统：

- 分析
- 校验
- 风险判定
- 中断到人工
- 恢复执行
- 写回状态

LangGraph 的 durable execution、human-in-the-loop、persistence 和 interrupts 适合这个形态。

### 服务层：FastAPI + Pydantic

FastAPI 适合这类 AI 服务，因为它支持 request body JSON 读取、类型转换、校验和清晰错误提示；Pydantic 字段还能直接补充额外验证和 JSON Schema 元数据。

### 前端：轻量 React 工作台

React 是工程形态选择，不是“前端主导”。第一版只需要 3 到 4 个核心页面，保留系统感，同时避免耗费过多时间在 UI 平台化上。

## 六、系统模块拆分

### 1. 样本接入模块

负责：

- 上传图像 / 图文样本
- 生成任务 ID
- 保存原始样本和元信息
- 选择单样本模式或批量模式

输入：

- image
- optional text / context
- optional reference label / rule set

输出：

- task_id
- sample metadata

### 2. 多模态分析模块

负责：

- 调用模型做场景理解
- 抽取结构化字段
- 输出候选结果与解释

典型字段：

- is_diversion_scene
- diversion_type
- key_objects
- visual_evidence
- negative_evidence
- confidence
- explanation

关键要求：必须输出固定 schema，而不是自由文本。

### 3. 规则核验模块

负责：

- 用显式规则检查模型输出
- 检查字段完整性
- 检查逻辑一致性
- 检查枚举值是否合法
- 检查与业务规范是否冲突

规则例子：

- 必填字段缺失
- 导流标记与导流类型冲突
- 分流 / 合流判断缺少视觉证据
- 风险等级与解释不一致
- 结果不符合规则模板

这一步会把项目从“模型输出系统”升级成“AI + 规则共治系统”。

### 4. 风险判定模块

负责：

- 计算风险等级
- 标记低置信度样本
- 标记规则冲突样本
- 标记需人工复核样本

推荐风险分级：

- low
- medium
- high
- needs_human_review

风险来源：

- 低置信度
- 规则冲突
- 字段缺失
- 模型解释过短或异常
- 多次分析不一致

### 5. 人工复核模块

负责：

- 展示高风险样本
- 允许人工批准、修改、驳回
- 记录复核意见
- 将修正结果写回

复核动作：

- approve
- edit
- reject
- send_back_for_analysis

当样本被判定为需要人工复核时，图流程可以暂停，等待外部操作后恢复。

### 6. 批量评测模块

负责：

- 跑一批样本
- 统计字段级正确率
- 统计风险命中率
- 统计人工介入率
- 汇总 bad case

第一版建议指标：

- schema 合规率
- 字段完整率
- 规则冲突率
- 高风险样本占比
- 人工复核率
- 人工修正率
- keep / review / discard 占比

如果有人工标注或真值，再加：

- precision / recall / F1
- 漏检率
- 有效样本提升率
- 误报 / 漏报统计

### 7. 轻量前端工作台

建议只做 4 个页面：

1. 样本上传页
   - 上传图像
   - 填上下文
   - 发起分析
2. 结果详情页
   - 原图
   - 结构化结果
   - 模型解释
   - 风险标签
   - 规则核验结果
3. 人工复核页
   - 待复核队列
   - 批准 / 修改 / 驳回
   - 复核历史
4. 批量评测页
   - 样本总数
   - 指标卡片
   - 风险分桶
   - bad case 列表

这已经足够支撑“求职可用版”。

## 七、技术栈清单

### 必须会

后端与服务：

- Python
- FastAPI
- Pydantic
- REST API 设计
- 基础异步请求处理

模型与输出：

- Responses API
- 多模态输入组织
- Structured Outputs
- JSON Schema 设计
- tool / function calling 基础

工作流：

- LangGraph 基础
- graph state 设计
- 节点编排
- interrupt / resume
- persistence 基础用法

数据与评测：

- 样本集组织
- 指标脚本
- bad case 分类
- 结果回流设计

### 应该会

前端与展示：

- React 基础
- 与 FastAPI 的接口联调
- 结果卡片展示
- 表格 / 过滤 / 状态展示

工程化：

- 配置管理
- 日志
- 错误处理
- README 和 API 文档
- Git 项目组织

## 八、建议数据结构

第一版至少需要 4 类 schema。

### 1. 输入 schema

```json
{
  "sample_id": "string",
  "image_path": "string",
  "context_text": "string | null",
  "rule_profile": "string | null"
}
```

### 2. 模型输出 schema

```json
{
  "is_diversion_scene": true,
  "diversion_type": "split | merge | non_diversion | uncertain",
  "key_objects": ["string"],
  "visual_evidence": ["string"],
  "negative_evidence": ["string"],
  "confidence": 0.0,
  "explanation": "string"
}
```

### 3. 核验与筛选输出 schema

```json
{
  "schema_valid": true,
  "rule_pass": false,
  "rule_violations": ["string"],
  "risk_level": "low | medium | high | needs_human_review",
  "filter_decision": {
    "action": "keep | review | discard",
    "reasons": ["string"]
  }
}
```

### 4. 人工复核 schema

```json
{
  "review_status": "approved | edited | rejected",
  "review_comment": "string",
  "final_result": {}
}
```

## 九、推荐主流程

上传样本 -> 多模态分析 -> 分流 / 合流 / 非导流 / 不确定结构化输出 -> 规则核验 -> 风险判定 -> keep / review / discard 筛选决策 -> 高风险进入人工复核 -> 写回结果 -> 更新批量评测

## 十、MVP 路线

### Phase 1：后端骨架与 schema

- 建立 FastAPI 项目结构。
- 定义 Pydantic 输入、模型输出、核验输出、人工复核 schema。
- 实现本地 SQLite 存储任务、样本、模型结果和复核记录。
- 提供基础健康检查和任务查询接口。

### Phase 2：单样本分析闭环

- 实现图片上传和任务创建。
- 接入多模态模型分析。
- 使用结构化输出生成固定字段。
- 实现规则核验和风险判定。
- 返回完整分析结果。

### Phase 3：人工复核

- 实现待复核队列接口。
- 支持 approve、edit、reject、send_back_for_analysis。
- 保存复核意见与最终结果。
- 打通高风险样本进入复核队列的流程。

### Phase 4：批量评测

- 设计样本集目录或 CSV / JSONL 输入格式。
- 批量执行分析与核验。
- 统计 schema 合规率、字段完整率、规则冲突率、高风险占比、人工复核率。
- 导出 bad case 报告。

### Phase 5：轻量前端

- 样本上传页。
- 结果详情页。
- 人工复核页。
- 批量评测页。
- 与 FastAPI 接口联调。

### Phase 6：作品集完善

- 补充 README 快速启动。
- 添加 API 文档和示例请求。
- 添加前端截图。
- 准备简历描述、面试讲解稿和项目架构图。

## 十一、项目介绍写法

可以先用这版作为项目总述：

设计并实现面向自动驾驶 / 道路场景的多模态质检、评测与人工复核工作台。系统支持图像 / 图文输入、结构化结果生成、规则核验、风险分级、人工复核与批量评测，采用 LangGraph 编排工作流、FastAPI 提供服务接口，并通过 Structured Outputs 保证结果 schema 合规。项目重点体现多模态应用开发、工作流编排、质量评测与 human-in-the-loop 工程能力。
