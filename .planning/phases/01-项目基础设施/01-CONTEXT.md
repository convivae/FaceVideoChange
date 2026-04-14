# Phase 1: 项目基础设施 - Context

**Gathered:** 2026-04-14
**Status:** Ready for planning

<domain>
## Phase Boundary

建立可运行的项目骨架，提供CLI接口和配置管理系统。CLI工具支持 `--help`、`--preset`、`--dry-run`，有完善的日志系统记录启动、预热和运行状态。

</domain>

<decisions>
## Implementation Decisions

### CLI 框架
- **D-01:** 使用 Typer 作为 CLI 框架
- **D-02:** 包含 `--help` 显示完整参数说明和示例
- **D-03:** 支持 `--dry-run` 验证配置而不启动实际处理
- **D-04:** 包含 `--preset <name>` 加载预设配置

### 配置文件格式
- **D-05:** 配置文件格式使用 YAML
- **D-06:** 配置文件路径: `~/.facevidechange/config.yaml`
- **D-07:** 支持通过 CLI 参数覆盖配置文件设置

### 预设系统
- **D-08:** 使用内置预设 (builtin)，用户通过 `--preset` 选择
- **D-09:** 内置预设包含: `realtime-8gb` (RTX 4060 实时换脸)
- **D-10:** 预设覆盖优先级: CLI 参数 > 环境变量 > 预设 > 默认值

### 日志系统
- **D-11:** 日志详细程度: 详细 (verbose) — 启动、预热、运行时全部记录
- **D-12:** 日志输出到 stdout，支持重定向到文件
- **D-13:** 日志分级: DEBUG / INFO / WARNING / ERROR
- **D-14:** 日志包含时间戳、模块名、日志级别

### 项目结构
- **D-15:** 项目根目录: `/Users/conv/aispace/FaceVideoChange`
- **D-16:** 主要代码: `src/` 目录
- **D-17:** 模型文件: `models/` 目录
- **D-18:** 配置文件: `config/` 目录

### Claude's Discretion
- 日志格式具体样式（颜色、字体）
- 预设文件的具体参数值（由后续阶段决定）
- 项目目录结构细节（可由 planner 根据实际需求决定）
- 测试框架选择

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### 项目
- `.planning/ROADMAP.md` — Phase 1 目标、依赖、成功标准
- `.planning/STATE.md` — 项目状态、技术栈决策
- `.planning/PROJECT.md` — 项目愿景、约束条件

### 技术栈 (已锁定)
- `raw/face_swap_model_evaluation.md` — 模型评测报告，inswapper_128_fp16 选型
- `raw/optimization_roadmap.md` — 优化方向路线图

</canonical_refs>

<specifics>
## Specific Ideas

- "CLI 越简单越好，只要实现功能，UI都是次要的"
- "新用户无需文档即可运行"
- 所有配置项都有合理的默认值

</specifics>

<deferred>
## Deferred Ideas

- GUI 界面 — Phase 8 之后考虑
- Web 界面 — 暂不考虑

</deferred>

---

*Phase: 01-项目基础设施*
*Context gathered: 2026-04-14*