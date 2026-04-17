---
gsd_state_version: 1.0
milestone: v1.0
milestone_name: milestone
status: executing
last_updated: "2026-04-17T15:59:43.304Z"
last_activity: 2026-04-17
progress:
  total_phases: 8
  completed_phases: 0
  total_plans: 4
  completed_plans: 0
  percent: 0
---

# FaceVideoChange State

## Project Reference

**Project:** FaceVideoChange
**Core Value:** 实时视频流换脸CLI工具，主播能在直播/创作中实时换脸，延迟低于100ms
**Current Focus:** Phase 01 — 项目基础设施

## Current Position

Phase: 01 (项目基础设施) — EXECUTING
Plan: 1 of 4
**Milestone:** v1.0
**Phase:** 1 (Planned)
**Plan:** 4 plans in 2 waves
**Status:** Executing Phase 01

**Progress Bar:**

```
[#                         ] 1/8 phases
```

**Plans:** 4 plans created

- 01-01: 项目结构 (Wave 1)
- 01-02: 配置系统 (Wave 2, depends on 01-01)
- 01-03: CLI框架 (Wave 2, depends on 01-02)
- 01-04: 日志系统 (Wave 2, depends on 01-02)

## Performance Metrics

**Target:**

- FPS: 30+ (RTX 4060)
- Latency: < 100ms (端到端)
- VRAM: < 8GB

**RTX 4060 性能预估:**
| Stage | Model | Latency | VRAM |
|-------|-------|---------|------|
| Detection | SCRFD-10GF | ~4ms | ~200MB |
| Alignment | 5pt landmarks | ~1ms | ~50MB |
| Feature | ArcFace ResNet50 | ~5ms | ~300MB |
| Swapping | inswapper_128_fp16 | ~10ms | ~1.5GB |
| **Total** | — | **~20ms** | **~2.1GB** |

## Accumulated Context

### Key Decisions

| Date | Decision | Rationale |
|------|----------|-----------|
| 2026-04-14 | inswapper_128_fp16 | RTX 4060最优选择，380MB FP16 |
| 2026-04-14 | SCRFD-10GF | 精度/速度平衡最佳 |
| 2026-04-14 | ONNX Runtime 1.18+ | CUDA 12.x支持，FP16 |
| 2026-04-14 | CLI优先 | 功能先行，GUI次要 |

### Tech Stack

```
inswapper_128_fp16.onnx (Deep-Live-Cam)
    └─ InsightFace SCRFD-10GF (人脸检测)
    └─ InsightFace ArcFace ResNet50 (特征提取)
    └─ ONNX Runtime 1.18+ (推理)
    └─ OpenCV 4.10+ + FFmpeg 6.x (视频)
    └─ python-ofiq 0.1.0 (质量评估)
```

### Blockers

None (planning phase)

### Notes

- 2026-04-14: 项目初始化，路线图创建
- ARCHITECTURE.md 待创建（在Phase 2期间）
- RTX 4060 实际FPS数据待实测（在Phase 2期间）

## Session Continuity

**Last Session:** 2026-04-14T14:39:48.276Z
**Last Activity:** 2026-04-17
**Next Action:** `/gsd-execute-phase 1` — 执行 Phase 1 实现

---

*State file for GSD workflow tracking*
*Format version: 1.0*
