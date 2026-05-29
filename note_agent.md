# 学习路径规划

阶段 1｜基础能力
    └── OpenAI / Claude API + Tool Use
        学会：调模型、定义工具 Schema、处理 tool_call 响应
        产出：一个能调 2-3 个工具的最简 Agent
        - Pydantic + JSON Mode 输出约束
        - OpenAI 的 response_format，输出校验 + 重试

  阶段 2｜编排模式
    └── 手写不同 Workflow
        ├── Simple Loop（自由循环）
        ├── ReAct（思考-行动-观察）
        ├── Plan-and-Execute（先规划后执行）
        ├── Router（意图路由）
        └── Reflection（自我反思）
        产出：同一个问题跑 5 种 workflow，对比报告

  阶段 3｜协议与互操作
    └── MCP / A2A
        学会：写 MCP Server，让 Agent 通过标准协议调外部系统
        产出：一个 MCP Server（比如接你的 Bangumi API）

  阶段 4｜Harness 工程
    └── Agent 的"身体"
        ├── Memory：对话历史管理 + 上下文压缩
        ├── Perception：输入预处理、意图识别
        ├── Controller：循环控制、终止条件、错误恢复
        ├── Safety：权限系统、输入过滤
        └── Observability：调用链追踪、token 统计

  阶段 5｜外部工程知识
    └── 服务化和基建
        ├── FastAPI —— Agent 对外暴露 API
        ├── 异步编程 —— asyncio，并发调多工具
        ├── 向量数据库 —— RAG 场景才需要
        └── Docker —— 部署
    
    - LiteLLM 技术栈
    - Caching & Cost Control（缓存与成本控制）
    - Streaming（流式输出），SSE（Server-Sent Events），流式 Tool Call 处理
    - Code Agent（沙箱代码执行能力）

# 学习进展记录

## 2026-5-25 - 2026-5-29

### Agent 项目架构设计

### OpenAI API + Tool Use + Workflow

### MCP (Server & Client)


## 2026-6-1 - 2026-6-5

### Harness 工程结构与相关技术栈

### OpenAI SDK 项目学习与理解


## 2026-6-8 - 2026-6-12

### 服务化与基建技术栈学习

### Letta 项目学习与理解

### Idea 实现与实验情况


## 2026-6-15 - 2026-6-19

### Agent 架构服务技术栈，Code Agent 与沙箱实现逻辑

### 并行与延迟优化逻辑

### Idea 细化与实验结果


## 2026-6-22 - 2026-6-26

### Agent 架构知识全面收尾总结

### 开源项目复现，工程思维训练


## 2026-6-29 - 2026-7-3
