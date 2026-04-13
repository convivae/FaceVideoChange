# Feature Research

**Domain:** Real-time Video Stream Face Swapping Tools
**Researched:** 2026-04-13
**Confidence:** HIGH

## Feature Landscape

### Table Stakes (Users Expect These)

Features users assume exist. Missing these = product feels incomplete.

| Feature | Why Expected | Complexity | Notes |
|---------|--------------|------------|-------|
| 人脸检测与追踪 (Face Detection & Tracking) | 换脸的核心基础，无此功能无法工作 | MEDIUM | InsightFace 方案成熟，支持多脸追踪 |
| 人脸对齐 (Face Alignment) | 保证换脸效果的自然性 | MEDIUM | 依赖检测结果，68点 landmarks |
| 人脸融合 (Face Blending/Swapping) | 核心功能，替换人脸 | HIGH | Inswapper_128 等模型，需 GPU |
| 摄像头实时捕获 (Webcam Capture) | 输入源的主要方式 | LOW | OpenCV/V4L2/VideoCapture |
| 视频文件输入 (Video File Input) | 测试和录制回放需要 | LOW | OpenCV 支持主流格式 |
| 本地预览窗口 (Local Preview) | 即时查看效果 | LOW | 可用 PyQt/OpenCV/window |
| RTMP 推流 (RTMP Streaming) | 输出到直播平台 | MEDIUM | ffmpeg/rtmp-dummy 支持抖音/B站/YouTube |
| 本地文件录制 (Local Recording) | 保存换脸结果 | LOW | ffmpeg 录制 MP4 |
| CLI 参数设计 (CLI Interface) | 核心用户是技术人员 | LOW | argparse/click |
| 人脸库管理 (Face Library) | 管理多个人脸切换 | MEDIUM | SQLite/JSON 存储特征 |

### Differentiators (Competitive Advantage)

Features that set the product apart. Not required, but valuable.

| Feature | Value Proposition | Complexity | Notes |
|---------|-------------------|------------|-------|
| 人脸质量评估 (Face Quality Score) | 自动过滤低质量人脸图，减少失败 | MEDIUM | 检测遮挡、模糊、角度 |
| 人脸相似度检测 (Deduplication) | 自动检测重复人脸，简化管理 | MEDIUM | ArcFace 特征比对 |
| 目标人脸选择 (Multi-face Targeting) | 多人场景中选择替换特定人脸 | MEDIUM | 需 UI/快捷键支持 |
| 换脸强度控制 (Blend Ratio) | 用户可调节替换程度 | LOW | 插值控制，简单实现 |
| RTX 4060 优化 (GPU Optimization) | 8GB VRAM 流畅运行 vs 竞品卡顿 | HIGH | INT8量化、pipeline 解耦 |
| 开源 + CLI 优先 | 透明可控 vs 闭源黑盒 | LOW | 差异化定位 |

### Anti-Features (Commonly Requested, Often Problematic)

Features that seem good but create problems.

| Feature | Why Requested | Why Problematic | Alternative |
|---------|---------------|-----------------|-------------|
| 表情迁移 (Expression Transfer) | 更生动的换脸效果 | 计算量大，RTX 4060 无法实时；当前模型效果不稳定 | Inswapper 已包含表情学习，够用 |
| 口型同步 (Lip Sync) | 解决音视频不同步 | 需要独立音频处理 pipeline；延迟敏感 | ffmpeg 音频同步即可 |
| 实时美颜/滤镜叠加 | 提升画面质量 | 引入额外延迟；与换脸效果可能冲突 | 后处理阶段可选 |
| 图形界面 (GUI) | 降低使用门槛 | 开发成本高；目标用户是技术人员 | 先 CLI，v1 后考虑 Web UI |
| 移动端支持 | 扩大用户群 | 性能不足；与 RTX 4060 场景冲突 | 专注桌面端 |
| WebRTC 方案 | 低延迟传输 | 复杂度高；RTMP 已覆盖需求 | RTMP 为主，WebRTC v2 |
| 视频会议 SDK 集成 | 无缝对接 Zoom/腾讯会议 | 依赖平台 API；维护成本高 | OBS 虚拟摄像头中转 |

## Feature Dependencies

```
[人脸检测与追踪]
    └──requires──> [人脸对齐]
                        └──requires──> [人脸融合]

[摄像头实时捕获]
    └──requires──> [帧率控制]

[RTMP 推流]
    └──requires──> [FFmpeg 集成]

[人脸质量评估] ──enhances──> [人脸融合]
    └──requires──> [人脸特征提取]

[人脸相似度检测]
    └──requires──> [人脸特征提取]
    └──requires──> [人脸质量评估]
```

### Dependency Notes

- **人脸检测与追踪 requires 人脸对齐：** 检测提供 bounding box，对齐提供关键点 landmarks，二者顺序处理
- **人脸对齐 requires 人脸融合：** 对齐的结果直接送入融合网络
- **摄像头实时捕获 requires 帧率控制：** 需协调捕获、处理、输出的帧率同步
- **RTMP 推流 requires FFmpeg 集成：** ffmpeg 是 RTMP 的事实标准
- **人脸质量评估 enhances 人脸融合：** 提前过滤低质量输入，减少融合失败
- **人脸相似度检测 requires 人脸特征提取：** 复用特征提取管线
- **表情迁移 conflicts 实时性能：** 额外计算量会导致 RTX 4060 无法维持 30+ FPS

## MVP Definition

### Launch With (v1)

Minimum viable product — what's needed to validate the concept.

- [ ] 人脸检测与追踪 — 核心中的核心，无此无法工作
- [ ] 人脸对齐 — 保证换脸自然性的必要步骤
- [ ] 人脸融合 (Inswapper) — 换脸核心算法
- [ ] 摄像头实时捕获 — 主要输入源
- [ ] 视频文件输入 — 测试和回放支持
- [ ] 本地预览窗口 — 即时查看效果
- [ ] RTMP 推流 — 核心输出，直播平台支持
- [ ] 本地文件录制 — 保存结果
- [ ] CLI 参数设计 — 目标用户的核心交互方式
- [ ] 人脸库管理 — 多脸切换需求

### Add After Validation (v1.x)

Features to add once core is working.

- [ ] 人脸质量评估 — 用户反馈"换脸效果不稳定"时添加
- [ ] 人脸相似度检测 — 用户反馈"人脸库管理混乱"时添加
- [ ] 目标人脸选择 (多人场景) — 多人直播需求出现时添加
- [ ] 换脸强度控制 — 用户反馈"效果太假"时添加
- [ ] 配置文件管理 — CLI 参数过多时添加

### Future Consideration (v2+)

Features to defer until product-market fit is established.

- [ ] 表情迁移 — RTX 4060 性能瓶颈，需等待更小模型
- [ ] 口型同步 — 音频 pipeline 复杂，v2 考虑
- [ ] 光照自适应 (Color Matching) — 后期质量提升
- [ ] 边缘羽化 (Seamless Blending) — 后处理质量优化
- [ ] Web UI — 用户群扩大后降低门槛
- [ ] WebRTC 方案 — 企业用户需求出现时

## Feature Prioritization Matrix

| Feature | User Value | Implementation Cost | Priority |
|---------|------------|---------------------|----------|
| 人脸检测与追踪 | HIGH | MEDIUM | P1 |
| 人脸对齐 | HIGH | MEDIUM | P1 |
| 人脸融合 | HIGH | HIGH | P1 |
| 摄像头捕获 | HIGH | LOW | P1 |
| 视频文件输入 | MEDIUM | LOW | P1 |
| 本地预览 | HIGH | LOW | P1 |
| RTMP 推流 | HIGH | MEDIUM | P1 |
| 本地录制 | HIGH | LOW | P1 |
| CLI 参数设计 | HIGH | LOW | P1 |
| 人脸库管理 | HIGH | MEDIUM | P1 |
| 人脸质量评估 | MEDIUM | MEDIUM | P2 |
| 人脸相似度检测 | MEDIUM | MEDIUM | P2 |
| 目标人脸选择 | MEDIUM | MEDIUM | P2 |
| 换脸强度控制 | MEDIUM | LOW | P2 |
| RTX 4060 优化 | HIGH | HIGH | P1 |
| 表情迁移 | LOW | HIGH | P3 |
| 口型同步 | LOW | HIGH | P3 |
| GUI/Web UI | MEDIUM | HIGH | P3 |
| 光照自适应 | LOW | MEDIUM | P3 |
| 边缘羽化 | LOW | MEDIUM | P3 |

**Priority key:**
- P1: Must have for launch
- P2: Should have, add when possible
- P3: Nice to have, future consideration

## Competitor Feature Analysis

| Feature | DeepFaceLive | Deep-Live-Cam | Avatarify | FaceVideoChange |
|---------|--------------|---------------|-----------|-----------------|
| 实时换脸 | ✓ 30+ FPS | ✓ 30-55 FPS | ✓ 15-33 FPS | ✓ Target 30+ FPS |
| 单图换脸 | ✓ | ✓ | ✓ | ✓ |
| 摄像头输入 | ✓ | ✓ | ✓ | ✓ |
| RTMP 推流 | ✓ (OBS 集成) | ✓ | ✓ (虚拟摄像头) | ✓ |
| 本地录制 | ✓ | ✓ | ✗ | ✓ |
| CLI 优先 | ✗ (GUI 为主) | 部分 | ✗ | ✓ |
| 开源 | ✓ | ✓ | ✓ | ✓ |
| 人脸质量评估 | ✗ | ✗ | ✗ | ✓ (差异化) |
| 相似度检测 | ✗ | ✗ | ✗ | ✓ (差异化) |
| RTX 4060 优化 | 一般 | 一般 | 一般 | ✓ (差异化) |
| 人脸库管理 | 基础 | 基础 | ✗ | ✓ |
| 表情迁移 | ✗ | ✗ | ✓ | v2+ |
| 口型同步 | ✗ | ✗ | ✗ | v2+ |

### 差异化分析

**DeepFaceLive:**
- 成熟但 GUI 为主，CLI 不友好
- 模型选择多但配置复杂
- OBS 集成好但性能一般

**Deep-Live-Cam:**
- 当前最流行的开源方案
- v2.7-beta (2026-03) 最新版本
- 性能可优化但未专门针对 8GB VRAM

**Avatarify:**
- 基于 first-order motion model
- 表情驱动更强但计算量大
- 已停止维护

**FaceVideoChange 差异化策略:**
1. **CLI 优先** — 对标技术人员/开发者
2. **RTX 4060 专门优化** — 8GB VRAM 流畅运行
3. **人脸质量前置过滤** — 减少融合失败
4. **相似度检测** — 简化人脸库管理
5. **pipeline 解耦** — 降低延迟

## RTX 4060 性能可行性分析

### 关键技术要点

| 技术 | 状态 | 性能目标 |
|------|------|----------|
| 模型量化 (INT8/FP16) | 成熟 | 减少 55-70% VRAM |
| Pipeline 解耦 | 已验证 | 检测 15-30ms → 5-10ms/swap |
| 零拷贝内存 | 可行 | 避免每帧分配 |
| 模型选择 | Inswapper_128 优先 | 小模型优先 |

### 帧时间预算 (目标 30 FPS = 33ms/frame)

```
人脸检测:     10-15ms (可缓存，不必每帧)
人脸对齐:      2-5ms  (依赖检测)
特征提取:      5-8ms  (复用缓存)
人脸融合:      8-12ms (模型推理)
后处理/输出:   3-5ms  (合成、编码)

总计:         ~28-35ms (可达到 30 FPS)
```

### 内存预算

RTX 4060 8GB VRAM 分配建议:
- Inswapper_128: ~1.5GB (INT8)
- GFPGAN: ~1.2GB (可选后处理)
- InsightFace: ~500MB
- 系统开销: ~1GB
- **剩余缓冲: ~3.8GB** (足够单脸场景)

## Sources

- DeepFaceLive GitHub & Documentation (iperov/DeepFaceLive)
- Deep-Live-Cam GitHub & Community (hacksider/Deep-Live-Cam) v2.7-beta
- Avatarify Python Implementation (alievk/avatarify-python)
- ONNX Runtime Real-time Face Swap Pipeline (dev.to)
- RTX 4060 AI Inference Benchmarks (dev.to, alibaba.com)
- OBS Studio AI Overlay Integration (SimaBit)
- Project Requirements from .planning/PROJECT.md

---
*Feature research for: FaceVideoChange Real-time Face Swapping*
*Researched: 2026-04-13*
