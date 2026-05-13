- 目标岗位：Applied AI / LLM 应用开发工程师、Multimodal AI Engineer / 多模态应用工程师
- 项目范围：只做求职可用版
- 能力重点：多模态输入、结构化输出、规则核验、风险判定、人工复核、批量评测、轻量前端
- 暂不做：复杂多 Agent、重前后端平台、推理基础设施、自研训练体系

---
一、项目最终定位
项目名称
面向自动驾驶/道路场景的多模态质检、评测与人工复核工作台
一句话介绍
这是一个面向道路场景图像/图文样本的多模态 AI 工作台：系统接收样本后，自动完成场景分析、结构化结果生成、规则核验、风险判定，并将低置信度或高风险样本送入人工复核；同时支持批量评测、bad case 分析和结果回流。
这个项目为什么适合你
它把你已有的三类积累接在一起：
- 自动驾驶 / 道路场景理解
- 多模态 / 大模型微调基础
- 工程化系统实现
而且它直接对应当前应用岗最看重的几项能力：多模态输入、tool/function calling、structured outputs、workflow orchestration、evaluation、service API。OpenAI 当前把 Responses API 定位为用于文本、图像、工具调用和多轮状态交互的统一接口；Structured Outputs 用于保证输出符合你定义的 JSON Schema；LangGraph 则明确主打 durable execution、human-in-the-loop、persistence 和 interrupts。(OpenAI开发者)

---
二、岗位地图
1. 主目标岗位：Applied AI / LLM 应用开发工程师
这个项目最强对应的是这类岗位，因为它本质上是一个业务化的 LLM 工作流系统，而不是单纯模型实验。你做出来的能力点会是：
- 把模型封装成服务
- 设计结构化输出
- 编排多步骤工作流
- 做规则核验和错误回退
- 接入人工复核
- 构建批量评测与 bad case 闭环
这些恰好对应当前官方能力栈：Responses API 支持多模态输入、function calling、内置工具和 stateful interactions；Structured Outputs 能让模型输出严格遵守 JSON Schema。(OpenAI开发者)
2. 主目标岗位：Multimodal AI Engineer / 多模态应用工程师
你的项目天然是“图像 + 文本 + 规则”的多模态应用，而不是普通聊天系统。它会体现：
- 图像/图文输入处理
- 场景理解与字段抽取
- 视觉结果到结构化任务结果的映射
- 多模态错误分析
Responses API 官方明确支持 text 和 image 输入，这使你的项目在技术叙事上非常自然。(OpenAI开发者)

---
三、项目核心目标
这个项目不是“做一个能看图说话的系统”，而是要做一个可用于质检和复核的工作流系统。
你最终要交付的能力
1. 多模态输入
接收图像或图文样本。
2. 结构化输出
不是自由文本，而是固定 schema 的结果。
3. 规则核验
用显式规则检查模型结果是否合规。
4. 风险判定
对不确定、冲突、缺字段、违规结果打风险标签。
5. 人工复核
高风险样本进入复核队列，由人工确认或修正。
6. 批量评测
支持离线样本集跑数，统计指标和 bad case。
7. 轻量前端
能上传样本、查看结果、复核样本、浏览批量统计。

---
四、项目适合解决的具体问题
你要把问题定义得足够窄，项目才会强。
推荐场景
A. 场景标签/事件质检
例如：给定道路场景图像，判断模型输出的场景标签是否合理，是否缺失关键对象，是否存在明显误判。
B. 标注结果核验
例如：给定图像和标注结果，判断字段是否完整、是否符合规范、是否存在逻辑冲突。
C. 图像 + 规则联合审查
例如：给定图像、任务文本和规则模板，输出结构化审查结果和风险项。

---
五、最终项目架构选型建议
总体原则
工作流优先，模型嵌入其中；前端轻量，后端清晰；结构化优先，而不是聊天优先。
最终推荐选型
- 编排层：LangGraph
- 模型接口层：Responses API
- 服务层：FastAPI + Pydantic
- 前端：轻量 React 工作台
- 存储层：SQLite 或 PostgreSQL（二选一，第一版优先 SQLite）
为什么这么选
2.1 模型接口层：Responses API
因为你的项目第一版最需要的是：
- 图像 + 文本输入
- function calling
- 多轮/状态化交互
- 统一接口
Responses API 当前官方定义就是统一的多模态与工具调用接口。(OpenAI开发者)
2.2 输出约束：Structured Outputs
你这个项目如果没有结构化输出，价值会大幅下降。
Structured Outputs 可以确保结果符合你定义的 JSON Schema，避免缺 key、非法枚举、字段漂移。(OpenAI开发者)
2.3 编排层：LangGraph
因为你不是做单步问答，而是做：
- 分析
- 校验
- 风险判定
- 中断到人工
- 恢复执行
- 写回状态
LangGraph 官方能力正好就是 durable execution、human-in-the-loop、persistence 和 interrupts。(LangChain 文档)
2.4 服务层：FastAPI + Pydantic
FastAPI 非常适合这类 AI 服务，因为它直接支持 request body JSON 读取、类型转换、校验和清晰错误提示；依赖声明还能自动进入 OpenAPI；Pydantic 字段还能直接补充额外验证和 JSON Schema 元数据。(FastAPI)
2.5 前端：轻量 React 工作台
这里 React 是工程形态选择，不是“前端主导”。
你只需要 3–4 个核心页面，不做复杂平台。这样既保留系统感，也不至于把时间耗死在 UI 上。

---
六、系统模块拆分
1. 样本接入模块
负责：
- 上传图像/图文样本
- 生成任务 ID
- 保存原始样本和元信息
- 选择单样本模式或批量模式
输入
- image
- optional text/context
- optional reference label / rule set
输出
- task_id
- sample metadata

---
2. 多模态分析模块
负责：
- 调用模型做场景理解
- 抽取结构化字段
- 输出候选结果与解释
典型字段
可以根据你的场景定义，例如：
- scene_type
- key_objects
- violations
- missing_labels
- confidence
- explanation
这里的关键
必须输出固定 schema，而不是自由文本。
这一步建议完全依赖 Structured Outputs。(OpenAI开发者)

---
3. 规则核验模块
负责：
- 用显式规则检查模型输出
- 检查字段完整性
- 检查逻辑一致性
- 检查枚举值是否合法
- 检查与业务规范是否冲突
举例
- 必填字段缺失
- 场景标签与关键对象冲突
- 风险等级与解释不一致
- 结果不符合规则模板
这里的价值
这一步会把你的项目从“模型输出系统”升级成“AI + 规则共治系统”。

---
4. 风险判定模块
负责：
- 计算风险等级
- 标记低置信度样本
- 标记规则冲突样本
- 标记需人工复核样本
推荐风险分级
- low
- medium
- high
- needs_human_review
风险来源建议
- 低置信度
- 规则冲突
- 字段缺失
- 模型解释过短或异常
- 多次分析不一致

---
5. 人工复核模块
负责：
- 展示高风险样本
- 允许人工批准/修改/驳回
- 记录复核意见
- 将修正结果写回
LangGraph 的 interrupt/resume 和 persistence 很适合这个节点：当样本被判定为需要人工复核时，图流程可以暂停，等待外部操作后恢复。(LangChain 文档)
复核动作建议
- approve
- edit
- reject
- send_back_for_analysis

---
6. 批量评测模块
负责：
- 跑一批样本
- 统计字段级正确率
- 统计风险命中率
- 统计人工介入率
- 汇总 bad case
第一版建议指标
- schema 合规率
- 字段完整率
- 规则冲突率
- 高风险样本占比
- 人工复核率
- 人工修正率
如果你有人工标注或真值
再加：
- 准确率 / F1
- 关键字段正确率
- 误报/漏报统计

---
7. 轻量前端工作台
建议只做 4 个页面：
页面 1：样本上传页
- 上传图像
- 填上下文
- 发起分析
页面 2：结果详情页
- 原图
- 结构化结果
- 模型解释
- 风险标签
- 规则核验结果
页面 3：人工复核页
- 待复核队列
- 批准/修改/驳回
- 复核历史
页面 4：批量评测页
- 样本总数
- 指标卡片
- 风险分桶
- bad case 列表
这已经足够“求职可用版”。

---
七、技术栈清单
必须会
后端与服务
- Python
- FastAPI
- Pydantic
- REST API 设计
- 基础异步请求处理
模型与输出
- Responses API
- 
- 多模态输入组织
- Structured Outputs
- JSON Schema 设计
- tool/function calling 基础
工作流
- LangGraph 基础
- graph state 设计
- 节点编排
- interrupt / resume
- persistence 基础用法
数据与评测
- 样本集组织
- 指标脚本
- bad case 分类
- 结果回流设计
应该会
前端与展示
- React 基础
- 与 FastAPI 的接口联调
- 结果卡片展示
- 表格/过滤/状态展示
工程化
- 配置管理
- 日志
- 错误处理
- README 和 API 文档
- Git 项目组织

---
八、建议的数据结构
你第一版至少要有 4 类 schema。
1. 输入 schema
{
  "sample_id": "string",
  "image_path": "string",
  "context_text": "string | null",
  "rule_profile": "string | null"
}
2. 模型输出 schema
{
  "scene_type": "string",
  "key_objects": ["string"],
  "issues": ["string"],
  "confidence": 0.0,
  "explanation": "string"
}
3. 核验输出 schema
{
  "schema_valid": true,
  "rule_pass": false,
  "rule_violations": ["string"],
  "risk_level": "low | medium | high | needs_human_review"
}
4. 人工复核 schema
{
  "review_status": "approved | edited | rejected",
  "review_comment": "string",
  "final_result": {}
}

---
九、推荐的项目主流程
上传样本 → 多模态分析 → 结构化输出 → 规则核验 → 风险判定 → 低风险直接归档 / 高风险进入人工复核 → 写回结果 → 更新批量评测

---
十、建议的项目介绍写法
你可以先用这版作为项目总述：
设计并实现面向自动驾驶/道路场景的多模态质检、评测与人工复核工作台。系统支持图像/图文输入、结构化结果生成、规则核验、风险分级、人工复核与批量评测，采用 LangGraph 编排工作流、FastAPI 提供服务接口，并通过 Structured Outputs 保证结果 schema 合规。项目重点体现多模态应用开发、工作流编排、质量评测与 human-in-the-loop 工程能力。