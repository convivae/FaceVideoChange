# FaceVideoChange State

## Project Reference

**Project:** FaceVideoChange
**Core Value:** 实时视频流换脸CLI工具，主播能在直播/创作中实时换脸，延迟低于100ms
**Current Focus:** Phase 1 - 项目基础设施

## Current Position

**Milestone:** v1.0
**Phase:** 1 (Not started)
**Plan:** N/A
**Status:** Planning

**Progress Bar:**
```
[                          ] 0/8 phases
```

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

**Last Session:** 2026-04-14 - 项目初始化
**Last Activity:** ROADMAP.md 创建完成
**Next Action:** `/gsd-plan-phase 1` - 规划Phase 1实现

---

*State file for GSD workflow tracking*
*Format version: 1.0*
