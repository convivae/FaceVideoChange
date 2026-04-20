# Phase 2: 模型验证与优化 - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-04-20
**Phase:** 2-模型验证与优化
**Areas discussed:** Benchmark 方法论, onnxslim 优化策略, 模型版本管理

---

## Analysis Summary

**Domain:** 验证 inswapper_128_fp16 在 RTX 4060 上达到 30+ FPS 性能目标

**Prior Decisions Applied:**
- CLI framework: Typer (Phase 1)
- Config format: YAML with presets (Phase 1)
- Tech stack: ONNX Runtime + CUDA, InsightFace models (STATE.md)

**Codebase Context:**
- `src/facevidechange/` - Main code directory
- `config/presets.yaml` - Preset configurations
- `raw/face_swap_model_evaluation.md` - Model selection report
- `raw/optimization_roadmap.md` - Optimization directions

---

## Benchmark 方法论

**Gray Area:** 如何测量 FPS/VRAM？用什么测试素材？

**User's choice:** Proceeded with recommended defaults (standardized approach)

**Recommended approach captured:**
- 测试素材：标准 1080p 单脸测试图
- 测试条件：固定输入，固定次数取平均值
- 指标收集：NVML (VRAM) + Python time (FPS)

---

## onnxslim 优化策略

**Gray Area:** 优化哪些模型？如何优化？

**User's choice:** Proceeded with recommended defaults

**Recommended approach captured:**
- 优化范围：inswapper_128_fp16 + SCRFD-10GF + ArcFace ResNet50
- 优化方式：onnxslim 自动化脚本批量处理
- 优化目标：体积减少 20%+，速度提升 10%+

---

## 模型版本管理

**Gray Area:** 如何锁定版本？存储方式？

**User's choice:** Proceeded with recommended defaults

**Recommended approach captured:**
- 版本锁定在 YAML 配置文件
- 下载脚本验证 SHA256 哈希
- skip-if-missing 模式支持

---

## Claude's Discretion

- Benchmark 具体运行次数（N=100 还是 N=1000？）
- 测试图片具体来源（使用 InsightFace 示例图还是自定义？）
- VRAM 测量精度（默认峰值还是逐帧采样？）

---

## Deferred Ideas

None — discussion stayed within phase scope

