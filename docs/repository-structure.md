# 仓库结构规划

这个仓库按照“后端服务、前端工作台、批量评测、样例数据、文档与配置”五块组织。第一版目标是让 MVP 能快速跑通单样本分析、规则核验、风险判定、人工复核和批量评测闭环。

```text
.
├── backend/                 # FastAPI 后端服务
│   ├── app/
│   │   ├── api/             # HTTP 路由层
│   │   ├── core/            # 配置、日志、通用基础设施
│   │   ├── schemas/         # Pydantic 请求 / 响应模型
│   │   ├── services/        # 业务服务：分析、规则、风险、复核
│   │   ├── storage/         # 数据库连接、模型、仓储层
│   │   └── workflows/       # LangGraph 状态与流程编排
│   └── tests/               # 后端测试
├── frontend/                # React 轻量工作台
│   ├── public/
│   └── src/
├── evals/                   # 批量评测与 bad case 分析
│   ├── datasets/            # 评测数据集定义或索引文件
│   ├── reports/             # 评测输出报告，默认不提交生成文件
│   └── scripts/             # 批量评测脚本
├── data/                    # 本地开发数据
│   ├── samples/             # 示例样本和轻量 fixture
│   ├── uploads/             # 本地上传文件，默认不提交
│   └── exports/             # 导出结果，默认不提交
├── configs/                 # 规则模板和运行配置
│   └── rule_profiles/
└── docs/                    # 项目规划、API 设计、实现笔记
```

## 模块边界

- `backend/app/api` 只处理 HTTP 入参、出参和状态码，不写复杂业务逻辑。
- `backend/app/schemas` 放稳定的数据契约，是后端、前端、评测脚本共同依赖的事实来源。
- `backend/app/services` 放可测试的业务逻辑，例如规则核验、风险计算、模型调用封装。
- `backend/app/workflows` 放 LangGraph 相关编排，负责把分析、核验、风险判定和人工复核串起来。
- `backend/app/storage` 放数据库相关实现，避免 API 层直接访问数据库细节。
- `evals` 独立于 Web 服务，后续可以复用后端 schema 和服务跑离线评测。
- `configs/rule_profiles` 放规则模板，便于替换不同质检任务。

## 第一阶段落地顺序

1. 完成 Pydantic schema。
2. 完成规则核验与风险判定纯函数。
3. 完成 FastAPI 路由和本地 mock 分析流程。
4. 接入 SQLite 持久化。
5. 接入多模态模型真实调用。
6. 加人工复核接口。
7. 加批量评测脚本。
8. 做 React 工作台。
