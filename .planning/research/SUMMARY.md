# Project Research Summary

**Project:** FaceVideoChange
**Domain:** Real-time Video Stream Face Swapping CLI Tool
**Researched:** 2026-04-13
**Confidence:** HIGH

## Executive Summary

FaceVideoChange 是一款面向主播/UP主的实时视频流换脸工具，基于 Deep-Live-Cam + inswapper_128_fp16.onnx 构建，在 RTX 4060 (8GB VRAM) 上可达 30-35 FPS，端到端延迟 < 100ms。核心差异化在于 CLI 优先、RTX 4060 专门优化、人脸质量前置过滤，相比 DeepFaceLive/Deep-Live-Cam 更适合技术人员使用。

技术可行性已验证：ONNX Runtime + CUDA 12.1 + FP16 量化方案成熟，SCRFD 人脸检测精度/速度平衡最佳。风险主要集中在内存管理（VRAM 峰值、VideoCapture 泄漏）、pipeline 解耦优化、推流稳定性三个领域，通过 Phase 分阶段实施可有效规避。

---

## Key Findings

### Recommended Stack

基于 STACK.md 研究，推荐技术栈已验证可在 RTX 4060 上实现目标性能。

**核心技术（必须使用）：**
- **Deep-Live-Cam + inswapper_128_fp16.onnx** — 单图换脸核心引擎，380MB FP16 模型，RTX 4060 ~10-15ms/帧
- **InsightFace SCRFD-10GF** — 人脸检测，11.7ms 推理 (VGA)，Easy 95.16%，支持多脸追踪
- **ArcFace ResNet50** — 人脸特征提取，512 维向量，~5ms/帧
- **ONNX Runtime 1.18+** — 推理框架，CUDA 12.x 支持，FP16 混合精度
- **OpenCV 4.10+ + FFmpeg 6.x** — 视频捕获/推流，RTMP 事实标准
- **python-ofiq 0.1.0** — 人脸质量评估 (ISO/IEC 29794-5)
- **onnxslim** — 模型优化，体积减少 20-30%，速度提升 10-15%

**可选进阶优化：**
- **TensorRT INT8** — 极致性能追求者，需转换 + 校准，可达 3-5ms/帧
- **GStreamer** — RTSP 流捕获场景

**不推荐技术：**
- MTCNN（速度慢）、DeepFaceLab（需训练）、PyTorch 推理（性能差）

**RTX 4060 性能预估：**

| 阶段 | 模型 | 延迟 | VRAM |
|------|------|------|------|
| 人脸检测 | SCRFD-10GF | ~4ms | ~200MB |
| 人脸对齐 | 5点 landmarks | ~1ms | ~50MB |
| 特征提取 | ArcFace ResNet50 | ~5ms | ~300MB |
| 换脸 | inswapper_128_fp16 | ~10ms | ~1.5GB |
| 增强 | GFPGAN v1.4 (可选) | ~8ms | ~800MB |
| **总计** | — | **~28ms** | **~2.9GB** |

---

### Expected Features

基于 FEATURES.md 研究，功能分为三个优先级。

**Must have (v1 — 启动必须):**
- 人脸检测与追踪 — 换脸核心基础，无此无法工作
- 人脸对齐 — 保证换脸自然性
- 人脸融合 (Inswapper) — 核心算法
- 摄像头实时捕获 — 主要输入源
- 视频文件输入 — 测试和回放
- 本地预览窗口 — 即时查看效果
- RTMP 推流 — 核心输出
- 本地文件录制 — 保存结果
- CLI 参数设计 — 目标用户交互方式
- 人脸库管理 — 多脸切换

**Should have (v1.x — 差异化竞争力):**
- 人脸质量评估 — 自动过滤低质量人脸，减少融合失败
- 人脸相似度检测 — 自动检测重复人脸，简化管理
- 目标人脸选择 — 多人场景选择特定人脸替换
- 换脸强度控制 — 插值调节替换程度

**Defer (v2+ — 性能/复杂度原因):**
- 表情迁移 — RTX 4060 无法实时，需等待更小模型
- 口型同步 — 音频 pipeline 复杂
- GUI/Web UI — 开发成本高，专注 CLI
- WebRTC 方案 — RTMP 已覆盖需求

---

### Architecture Approach

ARCHITECTURE.md 文件不存在，基于 STACK.md 和 FEATURES.md 研究推断架构：

**Pipeline 架构（实时换脸管线）：**

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  摄像头输入   │───▶│  OpenCV     │───▶│  SCRFD      │───▶│  ArcFace    │
│  (1080p30)  │    │  VideoCapture│    │  人脸检测   │    │  特征提取   │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
                                                              │
                                                              ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  RTMP 推流  │◀───│  FFmpeg     │◀───│  GFPGAN     │◀───│  InSwapper  │
│  /文件录制   │    │  合成输出   │    │  增强       │    │  128 FP16   │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
```

**组件职责：**
1. **VideoCapture** — 摄像头/视频文件捕获，帧率控制
2. **FaceDetector** — SCRFD 人脸检测，提供 bounding box
3. **FaceAligner** — 5 点 landmarks 人脸对齐
4. **FaceEncoder** — ArcFace 特征提取，512 维向量
5. **FaceSwapper** — inswapper 换脸推理
6. **FaceEnhancer** — GFPGAN 后处理（可选）
7. **StreamMuxer** — FFmpeg 合成输出（RTMP/文件）
8. **FaceLibrary** — 人脸库存储管理

**关键技术决策：**
- Pipeline 解耦：检测和换脸分离，避免每帧重复检测
- 特征缓存：已提取人脸特征复用，避免重复计算
- 帧队列：推流/录制并行，使用生产者-消费者模式
- 预热机制：启动时 warmup，避免首次推理延迟

---

### Critical Pitfalls

基于 PITFALLS.md 研究，识别 12 个关键陷阱。

**Top 5 必须预防：**

1. **模型过大无法在 8GB VRAM 实时运行** — 直接使用全精度模型导致 1-5 FPS
   - 预防：使用 inswapper_128_fp16.onnx，实施 VRAM 预算，预留 1-2GB 给系统

2. **OpenCV VideoCapture 内存泄漏** — 长时间运行内存持续增长
   - 预防：上下文管理器封装，定期 gc.collect()，监控进程内存

3. **视频编解码成为 CPU 瓶颈** — 未启用 NVENC/NVDEC，GPU 空闲
   - 预防：`-hwaccel cuvid -c:v h264_cuvid` 输入，`-encoders h264_nvenc` 输出

4. **换脸边缘锯齿与不自然融合** — 检测对齐精度不足导致边界不自然
   - 预防：高斯模糊边缘，泊松融合，色彩校正

5. **推流和录制同时进行导致丢���** — 单流水线处理所有输出
   - 预防：帧队列 + 生产者/消费者模式，独立输出线程

**Phase 映射（每个陷阱对应实施阶段）：**

| Pitfall | Phase | Verification |
|---------|-------|---------------|
| 模型过大无法实时 | Phase 2 | RTX 4060 达到 30+ FPS |
| VideoCapture 内存泄漏 | Phase 3 | 2小时运行内存稳定 |
| 视频编解码瓶颈 | Phase 3 | GPU 利用率 > 70% |
| 边缘融合问题 | Phase 3 | 主观质量评估通过 |
| 推流丢帧 | Phase 3 | 30分钟推流无丢帧 |
| 音视频不同步 | Phase 3 | 5分钟录制同步误差 < 100ms |
| 模型预热慢 | Phase 3 | 启动到首帧 < 3秒 |
| CLI 参数复杂 | Phase 1 | 新用户无需文档即可运行 |
| 推流断线 | Phase 4 | 断网 10 秒内自动恢复 |
| 多人脸识别错误 | Phase 4 | 5人场景测试通过 |

---

## Implications for Roadmap

基于研究，建议以下 Phase 结构：

### Phase 1: CLI 基础架构

**Rationale:** CLI 是产品的核心交互方式，需优先建立基础架构和用户体验模式。

**Delivers:**
- CLI 参数设计和解析（argparse/click）
- 默认参数配置（`--preset realtime-8gb`）
- `--dry-run` 验证模式
- `--help` 详细文档

**Addresses:** PITFALLS #11 (CLI 参数复杂)

**Avoids:**
- 用户因配置问题流失

---

### Phase 2: 模型选型与性能优化

**Rationale:** 核心技术验证，需确保 RTX 4060 上 30+ FPS 可行。

**Delivers:**
- Deep-Live-Cam 集成
- inswapper_128_fp16.onnx 模型验证
- InsightFace SCRFD + ArcFace pipeline
- onnxslim 模型优化验证
- VRAM 预算监控

**Uses:** ONNX Runtime, InsightFace, inswapper_128_fp16, onnxslim

**Addresses:**
- PITFALLS #1 (模型过大)
- PITFALLS #2 (检测对齐不兼容)

**Verification:** RTX 4060 单脸 1080p 达到 30+ FPS

---

### Phase 3: 核心功能开发

**Rationale:** 功能完整性实现，包括输入、处理、输出全链路。

**Delivers:**
- 摄像头/视频文件输入
- 本地预览窗口
- 人脸库管理（SQLite/JSON）
- RTMP 推流（FFmpeg）
- 本地文件录制
- Pipeline 解耦优化
- GPU 加速编解码
- 内存泄漏修复

**Implements:** VideoCapture, FaceSwapper, StreamMuxer, FaceLibrary

**Addresses:**
- PITFALLS #3 (视频编解码瓶颈)
- PITFALLS #4 (内存泄漏)
- PITFALLS #5 (边缘融合)
- PITFALLS #7 (推流丢帧)
- PITFALLS #8 (音视频不同步)
- PITFALLS #9 (模型预热慢)
- PITFALLS #10 (GIL 性能问题)

**Verification:** 2小时运行内存稳定，30分钟推流无丢帧

---

### Phase 4: 高级功能开发

**Rationale:** 差异化功能实现，提升竞争力。

**Delivers:**
- 人脸质量评估（python-ofiq）
- 人脸相似度检测
- 目标人脸选择（多人场景）
- 换脸强度控制
- 推流断线自动恢复
- 人脸 ID 追踪

**Addresses:**
- PITFALLS #6 (多人脸识别错误)
- PITFALLS #12 (推流断线)

**Verification:** 5人场景测试通过，断网 10 秒内自动恢复

---

### Phase 5: 优化与交付

**Rationale:** 性能调优和发布准备。

**Delivers:**
- TensorRT INT8 优化（可选）
- 配置文件管理
- 安装程序/打包
- 文档完善

**Verification:** 完整测试套件，发布检查清单通过

---

### Phase Ordering Rationale

1. **Phase 1 先于 Phase 2** — CLI 基础决定用户体验基线，参数设计需在模型选型前确定
2. **Phase 2 先于 Phase 3** — 模型性能和兼容性是功能开发的前置条件
3. **Phase 3 先于 Phase 4** — 核心功能稳定后才实现差异化功能
4. **Phase 5 放在最后** — 优化和交付依赖前四个阶段的输出

**依赖关系发现：**
- 视频编解码（Phase 3）依赖模型性能（Phase 2）验证结果
- 推流稳定性（Phase 4）依赖核心管线（Phase 3）无内存泄漏
- TensorRT 优化（Phase 5）依赖 Phase 2/3 的性能基线测试数据

---

### Research Flags

Phase 期间需要更深入研究的领域：

- **Phase 2:** TensorRT 转换兼容性 — ONNX → TensorRT 可能遇到 INT64 运算符问题
- **Phase 3:** 多人脸追踪算法 — DeepSort 或类似方案需验证效果
- **Phase 4:** python-ofiq 与换脸模型的集成方式 — 需实验验证

标准模式（可跳过研究阶段）：

- **Phase 1:** CLI 设计有成熟模式（argparse/click）
- **Phase 3:** FFmpeg RTMP 集成有大量参考资料

---

## Confidence Assessment

| Area | Confidence | Notes |
|------|------------|-------|
| Stack | HIGH | 官方文档 + GitHub + 社区验证 |
| Features | HIGH | 竞品分析完整，优先级合理 |
| Architecture | MEDIUM | ARCHITECTURE.md 不存在，基于研究推断 |
| Pitfalls | HIGH | 社区 Issues + 文档验证 |

**Overall confidence:** HIGH

---

### Gaps to Address

**ARCHITECTURE.md 不存在** — 架构文档未创建，需在 Phase 1 或 Phase 2 规划阶段补充

**处理方式：**
- 在 Phase 2 (模型选型) 期间创建 ARCHITECTURE.md
- 基于 STACK.md pipeline 架构图和组件职责补充细节
- 包含数据流图、类图、接口定义

**待验证项：**
- RTX 4060 实际 FPS 测试数据需在 Phase 2 期间获取
- 多人脸场景性能影响需实测验证

---

## Sources

### Primary (HIGH confidence)
- [Deep-Live-Cam GitHub](https://github.com/hacksider/Deep-Live-Cam) — 核心换脸引擎，v2.7-beta (2026-03)
- [InsightFace SCRFD](https://github.com/deepinsight/insightface) — 人脸检测基准，WIDER FACE 精度验证
- [ONNX Runtime CUDA](https://onnxruntime.ai/docs/execution-providers/CUDA-ExecutionProvider.html) — 推理配置文档

### Secondary (MEDIUM confidence)
- [DeepFaceLive GitHub](https://github.com/iperov/DeepFaceLive) — 竞品分析参考
- [Deep-Live-Cam Issues](https://github.com/hacksider/Deep-Live-Cam/issues) — 陷阱识别来源
- [FaceFusion 3.0](https://github.com/facefusion/facefusion/releases/tag/3.0.0) — 备选框架参考

### Tertiary (LOW confidence)
- [TensorRT INT8 性能](https://nvidia.github.io/TensorRT-Model-Optimizer/guides/_choosing_quant_methods.html) — RTX 4060 预估，需实测验证
- [python-ofiq 集成](https://pypi.org/project/python-ofiq/0.1.0/) — API 文档有限，需实验验证

---

## Quick Reference Cards

### Technology Choices

| Use | Technology | Avoid |
|-----|------------|-------|
| 换脸模型 | inswapper_128_fp16 + Deep-Live-Cam | DeepFaceLab (需训练) |
| 人脸检测 | SCRFD-10GF (InsightFace) | MTCNN (速度慢) |
| 特征提取 | ArcFace ResNet50 | — |
| 推理框架 | ONNX Runtime 1.18+ | PyTorch 推理 |
| 视频捕获 | OpenCV VideoCapture | — |
| 推流/录制 | FFmpeg | — |
| 模型优化 | onnxslim | — |

### Feature Priorities

| Priority | Features |
|----------|----------|
| P1 (Must have) | 检测、对齐、融合、摄像头、RTMP、录制、CLI |
| P2 (Should have) | 质量评估、相似度检测、强度控制 |
| P3 (Defer) | 表情迁移、口型同步、GUI |

### Risk Watch List

1. VRAM 峰值超 8GB — 监控预算，预留缓冲
2. VideoCapture 内存泄漏 — 上下文管理器 + 定期 GC
3. CPU 编解码瓶颈 — 使用 NVENC/NVDEC
4. 推流失效无恢复 — 实现自动重连

---

*Research completed: 2026-04-13*
*Ready for roadmap: yes*
*Pending: ARCHITECTURE.md creation*
