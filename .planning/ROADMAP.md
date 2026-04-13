# FaceVideoChange Roadmap

**项目:** FaceVideoChange - 实时视频流换脸CLI工具
**版本:** v1.0
**创建:** 2026-04-14
**Granularity:** Standard (6-8 phases, 3-5 plans each)

## 项目目标

在 RTX 4060 (8GB VRAM) 上实现实时视频流换脸，端到端延迟 < 100ms，支持 RTMP 推流和本地录制。

## 技术栈

| 组件 | 技术 | 说明 |
|------|------|------|
| 换脸模型 | inswapper_128_fp16.onnx | 128x128, ~380MB, FP16 |
| 人脸检测 | SCRFD-10GF | InsightFace, ~4ms@GPU |
| 特征提取 | ArcFace ResNet50 | 512维向量, ~5ms@GPU |
| 推理框架 | ONNX Runtime 1.18+ | CUDA 12.x, FP16 |
| 视频捕获 | OpenCV 4.10+ | VideoCapture |
| 推流/录制 | FFmpeg 6.x | RTMP/MP4 |

## Phases

- [ ] **Phase 1: 项目基础设施** - CLI框架、配置管理、日志系统
- [ ] **Phase 2: 模型验证与优化** - Deep-Live-Cam集成、模型性能验证
- [ ] **Phase 3: 核心换脸管线** - 人脸检测→对齐→融合→输出全链路
- [ ] **Phase 4: 输入输出系统** - 摄像头捕获、RTMP推流、本地录制
- [ ] **Phase 5: 人脸管理系统** - 人脸库、相似度检测、强度控制
- [ ] **Phase 6: 质量与稳定性** - 人脸质量评估、边缘融合、内存优化
- [ ] **Phase 7: 高级功能** - 多人脸追踪、推流断线恢复
- [ ] **Phase 8: 优化与交付** - TensorRT优化、打包、文档

---

## Phase Details

### Phase 1: 项目基础设施

**Goal:** 建立可运行的项目骨架，提供CLI接口和配置管理系统

**Depends on:** None (第一个阶段)

**Requirements:** 基础设施搭建

**Success Criteria** (what must be TRUE):

1. 用户运行 `--help` 能看到完整的参数说明和示例
2. 用户使用 `--preset realtime-8gb` 可自动加载优化配置
3. 用户使用 `--dry-run` 可验证配置而不启动实际处理
4. 所有配置项都有合理的默认值，新用户无需文档即可运行
5. 日志系统记录启动步骤、预热进度、运行时状态

**Plans**: TBD

---

### Phase 2: 模型验证与优化

**Goal:** 验证 inswapper_128_fp16 在 RTX 4060 上的性能可达 30+ FPS

**Depends on:** Phase 1

**Requirements:** CORE-01 (inswapper_128_fp16模型), CORE-02 (SCRFD-10GF检测), CORE-03 (ArcFace特征提取)

**Success Criteria** (what must be TRUE):

1. RTX 4060 单脸 1080p 输入达到 30+ FPS
2. VRAM 峰值占用 < 4GB，预留足够缓冲
3. 模型版本锁定，相同图片产生一致的检测/特征结果
4. 模型预热时间 < 3秒
5. onnxslim 优化后模型体积减少 20%+，速度提升 10%+

**Plans**: TBD

---

### Phase 3: 核心换脸管线

**Goal:** 实现人脸检测→对齐→融合的完整流水线，支持单人脸实时换脸

**Depends on:** Phase 2

**Requirements:** CORE-01, CORE-02, CORE-03

**Success Criteria** (what must be TRUE):

1. 摄像头输入 → 换脸输出端到端延迟 < 100ms
2. 换脸区域边缘自然，无明显锯齿或色差
3. Pipeline 解耦优化：检测不必每帧执行，复用已检测结果
4. 特征缓存：已提取人脸特征在帧间复用
5. 支持本地预览窗口实时显示效果

**Plans**: TBD

---

### Phase 4: 输入输出系统

**Goal:** 实现摄像头/视频文件输入、RTMP推流、本地录制的完整I/O系统

**Depends on:** Phase 3

**Requirements:** IO-01 (摄像头捕获), IO-02 (RTMP推流), IO-03 (本地录制)

**Success Criteria** (what must be TRUE):

1. 摄像头实时捕获支持 1080p30fps，无丢帧
2. RTMP 推流可连接到 B站/抖音/YouTube 等平台
3. 本地录制生成 MP4 文件，音视频同步误差 < 100ms
4. 推流和录制同时进行时无丢帧
5. 音视频时间戳正确，使用 PTS 管理帧顺序

**Plans**: TBD

---

### Phase 5: 人脸管理系统

**Goal:** 实现人脸库存储、相似度检测、换脸强度控制

**Depends on:** Phase 4

**Requirements:** FACE-01 (人脸库管理), FACE-02 (相似度检测), FACE-03 (强度控制)

**Success Criteria** (what must be TRUE):

1. 用户上传人脸图片后自动提取并缓存特征
2. 人脸库支持增删改查，人脸列表可枚举
3. 多张相似人脸上传时自动检测并提示
4. 用户可调节换脸强度 (0-100%)，实时预览效果
5. 相同人脸不重复提取特征，缓存命中 > 95%

**Plans**: TBD

---

### Phase 6: 质量与稳定性

**Goal:** 提升换脸质量，优化内存管理，确保长时间稳定运行

**Depends on:** Phase 5

**Requirements:** QUAL-01 (质量评估), QUAL-02 (边缘融合), QUAL-03 (内存优化)

**Success Criteria** (what must be TRUE):

1. 人脸质量评估过滤低质量输入（模糊、遮挡、角度过大）
2. 换脸边缘使用高斯模糊+泊松融合，效果自然
3. 2小时连续运行内存稳定，无泄漏
4. GPU 利用率 > 70%，无 CPU 瓶颈
5. 推流 FPS 稳定，无间歇性掉帧

**Plans**: TBD

---

### Phase 7: 高级功能

**Goal:** 实现多人脸追踪、推流断线恢复等高级功能

**Depends on:** Phase 6

**Requirements:** ADV-01 (多人脸追踪), ADV-02 (目标选择), ADV-03 (断线恢复)

**Success Criteria** (what must be TRUE):

1. 5人场景下正确追踪每个人脸ID，不混淆
2. 用户可指定替换画面中的特定人脸
3. 推流断网后 10 秒内自动重连恢复
4. 断线重连后音视频同步保持
5. DeepSort 追踪算法集成，人脸ID漂移率 < 5%

**Plans**: TBD

---

### Phase 8: 优化与交付

**Goal:** 性能极限优化、文档完善、发布打包

**Depends on:** Phase 7

**Requirements:** REL-01 (TensorRT优化), REL-02 (打包发布), REL-03 (文档)

**Success Criteria** (what must be TRUE):

1. TensorRT INT8 优化后 FPS 提升 20%+（可选）
2. 提供 conda/pip 安装方式，一键环境配置
3. 完整 README 文档，包含快速开始和故障排除
4. PyInstaller 打包生成可执行文件（Windows）
5. 发布检查清单全部通过

**Plans**: TBD

---

## Phase Progress

| Phase | Name | Plans Complete | Status | Completed |
|-------|------|----------------|--------|-----------|
| 1 | 项目基础设施 | 0/4 | Not started | - |
| 2 | 模型验证与优化 | 0/5 | Not started | - |
| 3 | 核心换脸管线 | 0/5 | Not started | - |
| 4 | 输入输出系统 | 0/5 | Not started | - |
| 5 | 人脸管理系统 | 0/5 | Not started | - |
| 6 | 质量与稳定性 | 0/5 | Not started | - |
| 7 | 高级功能 | 0/5 | Not started | - |
| 8 | 优化与交付 | 0/5 | Not started | - |

---

## Dependencies Graph

```
Phase 1 ──┬── Phase 2 ──┬── Phase 3 ──┬── Phase 4 ──┬── Phase 5 ──┬── Phase 6 ──┬── Phase 7 ──┬── Phase 8
          │             │             │             │             │             │             │
          │             │             │             │             │             │             │
CLI框架   │ 模型验证    │ 核心管线    │ I/O系统     │ 人脸管理    │ 质量稳定    │ 高级功能    │ 优化交付
配置管理  │ 性能优化    │             │             │             │             │             │
日志系统  │             │             │             │             │             │             │
```

---

## Pitfall Coverage

| Pitfall | Phase | Verification |
|---------|-------|-------------|
| 模型过大无法实时 | Phase 2 | RTX 4060 达到 30+ FPS |
| 检测对齐不兼容 | Phase 2 | 固定版本测试一致性 |
| CLI参数复杂 | Phase 1 | 新用户无需文档即可运行 |
| 视频编解码瓶颈 | Phase 4 | GPU 利用率 > 70% |
| 内存泄漏 | Phase 6 | 2小时运行内存稳定 |
| 边缘融合问题 | Phase 6 | 主观质量评估通过 |
| 推流丢帧 | Phase 4 | 30分钟推流无丢帧 |
| 音视频不同步 | Phase 4 | 5分钟录制同步误差 < 100ms |
| 模型预热慢 | Phase 2 | 启动到首帧 < 3秒 |
| 多人脸识别错误 | Phase 7 | 5人场景测试通过 |
| 推流断线 | Phase 7 | 断网 10 秒内自动恢复 |

---

## Coverage Summary

- **Total Phases:** 8
- **Total Requirements:** 8 (infrastructure, CORE, IO, FACE, QUAL, ADV, REL)
- **Coverage:** 100% ✓

---

*Last updated: 2026-04-14*
*Next: `/gsd-plan-phase 1`*
