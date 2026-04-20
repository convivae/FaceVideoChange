# Phase 2: 模型验证与优化 - Context

**Gathered:** 2026-04-20
**Status:** Ready for planning

<domain>
## Phase Boundary

验证 inswapper_128_fp16 在 RTX 4060 上的性能可达 30+ FPS，锁定模型版本，优化模型体积和推理速度。

此阶段不实现换脸管线，仅验证模型集成和性能基线。

</domain>

<decisions>
## Implementation Decisions

### Benchmark 方法论
- **D-01:** 使用标准 1080p 单脸测试图片进行基准测试
- **D-02:** 测试指标：FPS (timeit)、VRAM 峰值 (NVML)、模型预热时间
- **D-03:** 固定输入测试：同一图片连续 N 次推理取平均值
- **D-04:** 性能报告输出 JSON 格式 + Markdown 摘要

### onnxslim 优化策略
- **D-05:** 优化范围：inswapper_128_fp16 + SCRFD-10GF + ArcFace ResNet50
- **D-06:** 优化方式：onnxslim 自动化脚本批量处理
- **D-07:** 优化目标：体积减少 20%+，速度提升 10%+
- **D-08:** 优化后模型存储至 `models/optimized/` 目录

### 模型版本管理
- **D-09:** 模型版本锁定在 `config/presets.yaml` 或专用 `config/models.yaml`
- **D-10:** 下载脚本验证 SHA256 哈希，确保模型完整性
- **D-11:** 支持 skip-if-missing：模型不存在时跳过测试，不报错

### 集成测试方式
- **D-12:** 优先使用真实模型文件测试（模型缺失时跳过相关测试）
- **D-13:** 测试覆盖率目标：80%+（基于模型存在情况）

### Claude's Discretion
- Benchmark 具体运行次数（N=100 还是 N=1000？）
- 测试图片具体来源（使用 InsightFace 示例图还是自定义？）
- VRAM 测量精度（默认峰值还是逐帧采样？）

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### 项目
- `.planning/ROADMAP.md` — Phase 2 目标、依赖、成功标准
- `.planning/STATE.md` — 项目状态、技术栈决策
- `.planning/PROJECT.md` — 项目愿景、约束条件
- `.planning/phases/01-项目基础设施/01-CONTEXT.md` — Phase 1 决策（CLI框架、配置格式）

### 技术栈 (已锁定)
- `raw/face_swap_model_evaluation.md` — 模型评测报告，inswapper_128_fp16 选型依据
- `raw/optimization_roadmap.md` — 优化方向路线图，TensorRT/GFPGAN 等后续优化
- `config/presets.yaml` — 预设配置，realtime-8gb 预设参数

### 技术参考
- InsightFace SCRFD-10GF: 人脸检测，~4ms@GPU，95.16% WIDER FACE Easy
- InsightFace ArcFace: 特征提取，512维向量
- inswapper_128_fp16: 换脸模型，128x128，~380MB FP16
- ONNX Runtime 1.18+: 推理框架，CUDA 12.x 支持

</canonical_refs>

<codebase_context>
## Existing Code Insights

### Reusable Assets
- `config/presets.yaml` — 预设配置格式可复用
- CLI 框架 (Typer) — 集成 benchmark 命令
- 日志系统 — 用于 benchmark 结果输出

### Established Patterns
- YAML 配置格式 (PyYAML)
- XDG 路径规范 (Phase 1 决策)
- 模块化导入 (src/facevidechange/)

### Integration Points
- Benchmark 结果可被 Phase 3 (核心换脸管线) 引用
- 优化后模型路径需与 Phase 3 模型加载逻辑一致

</codebase_context>

<specifics>
## Specific Ideas

- "RTX 4060 实时换脸，延迟低于 100ms"
- Phase 1 已建立 realtime-8gb 预设，Phase 2 验证其可达性
- 模型性能数据需记录存档，供后续优化参考

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope

### Reviewed Todos (not folded)
(No pending todos matched this phase)

</deferred>

---

*Phase: 02-模型验证与优化*
*Context gathered: 2026-04-20*
