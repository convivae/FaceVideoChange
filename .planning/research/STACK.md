# Stack Research

**Domain:** Real-time video stream face swapping
**Researched:** 2026-04-13
**Confidence:** HIGH

## 推荐技术栈

### 核心技术

| 技术 | 版本 | 用途 | 推荐理由 |
|------|------|------|----------|
| **Deep-Live-Cam** | Latest (GitHub main) | 核心换脸推理引擎 | 基于 ONNX Runtime，支持 CUDA/CoreML/DirectML，单图换脸，无需训练，RTX 4060 可流畅运行 |
| **inswapper_128_fp16.onnx** | FP16 版本 | 换脸模型 | 128x128 输入分辨率，~380MB，FP16 精度专为 NVIDIA GPU 优化，显存占用低 |
| **InsightFace** | 0.7.3+ | 人脸检测/对齐/识别 | SCRFD 检测器精度高 (Easy 96.06%)，推理快 (11.7ms @ SCRFD-34GF)，支持 ArcFace 特征提取 |
| **ONNX Runtime** | 1.18+ | 推理框架 | 跨平台支持 CUDA 12.x，支持 FP16，自动选择最优执行 provider |
| **OpenCV** | 4.10+ | 视频捕获/显示 | VideoCapture 支持摄像头/视频文件，Python API 成熟稳定 |

### 支持库

| 库 | 版本 | 用途 | 使用场景 |
|----|------|------|----------|
| **onnxslim** | Latest | ONNX 模型优化 | 精简模型体积，提升推理速度 (inswapper_128_fp16.onnx 优化) |
| **FFmpeg** | 6.x / 7.x | 音视频处理/RTMP 推流 | 帧提取、音视频合成、RTMP 输出、文件录制 |
| **NumPy** | 1.26+ | 数组运算 | 人脸处理管线数据转换 |
| **Pillow** | 10.x | 图像处理 | 读取/保存人脸图片，格式转换 |
| **python-ofiq** | 0.1.0 | 人脸质量评估 | 基于 ISO/IEC 29794-5 标准，输出 0-100 质量分数 |
| **scikit-learn** | 1.5+ | 人脸相似度计算 | 特征向量余弦相似度判断 |
| **mss** / **PyGetWindow** | Latest | 屏幕捕获/窗口管理 | 实时预览/虚拟摄像头输出 |

### 开发工具

| 工具 | 用途 | 配置说明 |
|------|------|----------|
| **CUDA Toolkit** | GPU 加速 | CUDA 12.1+ (RTX 4060 必需)，配合 cuDNN 8.9+ |
| **PyTorch** (仅开发用) | 模型转换/调试 | 训练环境，非运行时必需 |
| **pip / conda** | 依赖管理 | 推荐 conda 管理 CUDA 版本，避免库冲突 |
| **pytest** | 单元测试 | 换脸效果验证、人脸质量评估测试 |

---

## 1. 换脸模型/框架

### 1.1 Deep-Live-Cam

**GitHub:** https://github.com/hacksider/Deep-Live-Cam

**技术架构:**
- ONNX Runtime 推理引擎
- inswapper_128_fp16.onnx 换脸模型 (380MB)
- GFPGAN v1.4 增强后处理
- 支持 CUDA/CoreML/DirectML/OpenVINO 多后端

**RTX 4060 性能:**
- 摄像头管线: ~25-35 FPS (单脸，1080p 输入)
- 解耦检测管线优化后: ~55 FPS (同上硬件)
- 预览加载延迟: 10-30 秒 (首次加载模型)
- RTX 3080 对比 CPU: 2.3x 加速

**显存占用:**
- inswapper_128_fp16: ~1.5-2 GB VRAM
- 加上 SCRFD 检测 + ArcFace 特征: 总计 ~3-4 GB VRAM
- 满足 8GB VRAM 约束，有余量给系统/显示

**推荐程度:** ⭐⭐⭐⭐⭐ **Must Use**

**优势:**
- 单图换脸，无需训练，开箱即用
- ONNX 模型便于优化和量化
- 社区活跃，持续更新
- 支持多人脸同时换脸

**劣势:**
- 128x128 分辨率，细节有损失
- GFPGAN 后处理增加延迟 (~5-10ms/帧)

---

### 1.2 FaceFusion 3.0

**GitHub:** https://github.com/facefusion/facefusion

**技术架构:**
- 多模型支持: InSwapper, SimSwap, UniFace, BlendSwap, GHOST
- Live Portrait 表情恢复
- ESRGAN 帧增强
- 支持 TensorRT 10.4 / CUDA 12.4 / OpenVINO 2024.1

**推荐程度:** ⭐⭐⭐⭐ **Recommended (备选)**

**优势:**
- 模型选择丰富 (GHOST 256 高分辨率)
- 增强管线完善
- 支持多角度人脸处理

**劣势:**
- 架构较复杂，实时调优难度高
- 高分辨率模型 (GHOST 256) 需要更多 VRAM
- FaceFusion 许可证需确认

---

### 1.3 SimSwap

**GitHub:** https://github.com/neuralchen/SimSwap

**技术规格:**
- SimSwap 224: 标准分辨率
- SimSwap 512 beta: 高分辨率
- 最低 GPU: 3GB VRAM
- 推荐 InsightFace 版本: 0.2.1 → 0.7.3

**RTX 4060 性能:**
- 预估 FPS: 15-25 (取决于分辨率和批大小)
- VRAM 占用: 3-5 GB (512 版本更高)

**推荐程度:** ⭐⭐⭐ **Alternative**

**适用场景:**
- 需要高分辨率换脸 (512)
- 对细节质量有更高要求
- 接受低于实时 FPS

---

### 1.4 DeepFaceLab

**官网:** https://deepfakes.ai/

**技术规格:**
- 最低 VRAM: 4GB
- RTX 30/40 系列: 使用 dfl_rtx3000_series 版本
- 必需训练，推理速度依赖模型

**推荐程度:** ⭐⭐ **Avoid (对于实时场景)**

**原因:**
- 需要预先训练模型，不适合单图换脸场景
- 推理管线复杂，集成难度大
- 主要用于离线视频处理

---

### 1.5 Roop (roop-unleashed)

**GitHub:** https://github.com/that-guy-jaff/roop-unleashed

**技术规格:**
- CUDA 12.1 要求
- 最低 VRAM: 8GB (声明值，实际更低)
- Windows 10/11 优化

**推荐程度:** ⭐⭐⭐ **Alternative**

**适用场景:**
- 离线视频处理为主
- 追求易用性 (一键换脸)
- 不强求实时性能

---

### 换脸模型对比

| 模型 | 分辨率 | VRAM | FPS 预估 (RTX 4060) | 换脸质量 | 推荐程度 |
|------|--------|------|---------------------|----------|----------|
| inswapper_128_fp16 | 128x128 | ~2GB | 25-35 | 中等 | ⭐⭐⭐⭐⭐ |
| SimSwap 224 | 224x224 | ~3GB | 15-25 | 较好 | ⭐⭐⭐ |
| SimSwap 512 | 512x512 | ~5GB | 8-15 | 好 | ⭐⭐ |
| GHOST 256 | 256x256 | ~4GB | 15-20 | 好 | ⭐⭐⭐ |
| DeepFaceLab | 可变 | 4GB+ | 取决于模型 | 最好 | ⭐⭐ |

**结论:** 对于 RTX 4060 实时换脸，**inswapper_128_fp16 + Deep-Live-Cam** 是最优选择。

---

## 2. 推理框架

### 2.1 ONNX Runtime

**版本:** 1.18+ (CUDA 12.x 支持)

**RTX 4060 性能:**
- inswapper_128_fp16 推理: ~10-15ms/帧
- ArcFace 特征提取: ~5-8ms/帧
- RetinaFace 检测 (备选): ~20-30ms/帧

**显存占用:**
- 动态显存分配，按需使用
- FP16 模型自动启用混合精度

**配置示例:**
```python
import onnxruntime as ort

sess_options = ort.SessionOptions()
sess_options.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
sess_options.intra_op_num_threads = 4

providers = [
    ('CUDAExecutionProvider', {
        'device_id': 0,
        'cudnn_conv_algo_search': 'DEFAULT',
        'do_copy_in_default_stream': True,
    }),
    'CPUExecutionProvider',
]

session = ort.InferenceSession('inswapper_128_fp16.onnx', sess_options, providers=providers)
```

**推荐程度:** ⭐⭐⭐⭐⭐ **Must Use**

**优势:**
- 跨平台支持完善
- 自动选择最优执行 provider
- ONNX 模型生态丰富
- 支持 FP16/INT8 量化
- 生产级稳定性

---

### 2.2 TensorRT

**版本:** 10.x (CUDA 12.x)

**RTX 4060 性能:**
- 理论加速比 ONNX Runtime 高 20-50%
- 需要手动转换 ONNX → TensorRT
- INT8/FP16 量化支持

**RTX 4060 性能预估:**
- FP16 推理: ~5-10ms/帧 (inswapper)
- INT8 推理: ~3-7ms/帧 (需校准)

**推荐程度:** ⭐⭐⭐⭐ **Recommended (进阶优化)**

**适用场景:**
- 极致性能追求
- 愿意投入转换/调试时间
- 8GB VRAM 紧张时使用 INT8

**注意:**
- ONNX → TensorRT 转换可能有兼容性问题 (如 INT64 运算符)
- 转换后模型与特定 TensorRT 版本绑定
- 调试难度高于 ONNX Runtime

**转换命令:**
```bash
# FP16 转换
trtexec --onnx=inswapper_128_fp16.onnx \
        --fp16 \
        --saveEngine=inswapper_128_fp16.trt \
        --workspace=4096

# INT8 转换 (需要校准数据)
trtexec --onnx=inswapper_128_fp16.onnx \
        --int8 \
        --calib=calib_data/ \
        --saveEngine=inswapper_128_int8.trt
```

---

### 2.3 PyTorch (FP16/INT8)

**用途:** 模型调试/转换，不作为推理引擎

**推荐程度:** ⭐⭐ **Avoid (作为推理引擎)**

**原因:**
- 推理性能不如 ONNX Runtime/TensorRT
- 部署复杂
- 仅用于模型转换/调试阶段

---

## 3. 视频捕获/推流

### 3.1 OpenCV VideoCapture

**版本:** 4.10+

**摄像头捕获:**
```python
import cv2

cap = cv2.VideoCapture(0, cv2.CAP_V4L2)  # Linux
cap = cv2.VideoCapture(0)  # Windows

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
cap.set(cv2.CAP_PROP_FPS, 30)
```

**延迟分析:**
- 摄像头 → OpenCV: ~30-50ms (取决于摄像头硬件)
- OpenCV 处理: ~10ms/帧
- 端到端延迟目标: <100ms

**推荐程度:** ⭐⭐⭐⭐⭐ **Must Use**

---

### 3.2 GStreamer

**用途:** RTSP 流捕获、高级视频管线

**延迟问题:**
- 默认配置: 500ms-1s 延迟
- 优化后 (latency=0): <100ms

**推荐程度:** ⭐⭐⭐ **Recommended (用于 RTSP)**

**Pipeline 示例:**
```bash
# 低延迟 RTSP 捕获
gst-launch-1.0 rtspsrc location=rtsp://... latency=0 ! \
  rtph264depay ! h264parse ! avdec_h264 ! videoconvert ! appsink
```

---

### 3.3 FFmpeg RTMP 推流

**版本:** 6.x / 7.x

**RTMP 推流命令:**
```bash
# 摄像头捕获 + 换脸处理 + RTMP 输出
ffmpeg -f v4l2 -i /dev/video0 \
       -vf "PROCESSED_VIDEO_FILTER" \
       -c:v libx264 -preset ultrafast -tune zerolatency \
       -f flv rtmp://live.bilibili.com/live/STREAM_KEY
```

**Windows 摄像头推流:**
```bash
ffmpeg -f dshow -i video="USB Camera" \
       -c:v libx264 -preset ultrafast -tune zerolatency \
       -f flv rtmp://stream.example.com/live
```

**推荐程度:** ⭐⭐⭐⭐⭐ **Must Use**

**优势:**
- RTMP 输出支持所有主流直播平台
- 支持文件录制
- 命令行灵活配置
- 音视频同步处理成熟

---

### 3.4 虚拟摄像头 (OBS Virtual Camera)

**用途:** 输出到视频会议软件

**方案:**
- OBS Studio + Virtual Camera
- Unity Capture (Windows)
- dshow_vcam (DirectShow 虚拟摄像头)

**推荐程度:** ⭐⭐⭐⭐ **Recommended**

---

## 4. 人脸检测/对齐

### 4.1 SCRFD (InsightFace)

**模型规格 (WIDER FACE):**

| 模型 | Easy | Medium | Hard | 推理时间 (VGA) | 参数量 |
|------|------|--------|------|----------------|--------|
| SCRFD-34GF | 96.06% | 94.92% | 85.29% | 11.7ms | 9.80M |
| SCRFD-10GF | 95.16% | 93.87% | 83.05% | 4.9ms | 3.86M |
| SCRFD-2.5GF | 93.78% | 92.16% | 77.87% | 4.2ms | 0.67M |

**RTX 4060 性能 (GPU):**
- SCRFD-34GF: ~100-150 FPS
- SCRFD-10GF: ~200-250 FPS

**推荐程度:** ⭐⭐⭐⭐⭐ **Must Use**

**优势:**
- 精度/速度平衡最佳
- InsightFace 生态完整 (检测+对齐+识别)
- ONNX 模型可用
- 支持多脸检测

---

### 4.2 RetinaFace

**精度:** 高 (22,738 faces @ WIDER FACE 3,226 images)

**性能:**
- RetinaFace-MNet0.25: 44 FPS @ RTX 4090
- RetinaFace-R50: 39 FPS @ RTX 4090

**推荐程度:** ⭐⭐⭐ **Alternative**

**适用场景:**
- 需要极高检测召回率
- 复杂场景 (遮挡、侧脸)
- 愿意牺牲速度

---

### 4.3 YOLOv8-Face

**精度 (WIDER FACE):**

| 模型 | Easy | Medium | Hard | FPS @ RTX 4090 |
|------|------|--------|------|----------------|
| YOLOv8N | 94.6% | 92.3% | 79.6% | 169 |
| YOLOv8M | 95.3% | 93.8% | 85.3% | 117 |

**推荐程度:** ⭐⭐⭐⭐ **Recommended**

**优势:**
- Ultralytics 生态成熟
- 训练/微调灵活
- 速度极快

**劣势:**
- 需额外集成人脸对齐
- 默认不支持关键点检测

---

### 4.4 MediaPipe Face Detection

**性能:**
- CPU: ~25 FPS (0.04s/face)
- GPU: ~100+ FPS

**推荐程度:** ⭐⭐⭐ **Alternative**

**适用场景:**
- 跨平台部署 (iOS/Android/Web)
- CPU 推理场景
- 快速原型开发

---

### 4.5 MTCNN

**性能:** 较慢，不推荐实时场景

**推荐程度:** ⭐ **Avoid**

---

## 5. 人脸特征提取

### 5.1 ArcFace

**模型规格:**

| 模型 | 特征维度 | 精度 | 推理时间 |
|------|----------|------|----------|
| ResNet50-ArcFace | 512 | 高 | ~5ms @ GPU |
| ResNet100-ArcFace | 512 | 更高 | ~10ms @ GPU |
| MobileFaceNet | 512 | 中等 | ~2ms @ GPU |

**RTX 4060 性能:**
- ArcFace ResNet50: ~5-8ms/帧
- 批处理可加速 (4-8 脸/批)

**推荐程度:** ⭐⭐⭐⭐⭐ **Must Use**

**优势:**
- 人脸识别 SOTA 模型
- 特征向量标准化
- InsightFace 集成

**ONNX 转换注意事项:**
- IR 版本: 3
- Opset 版本: 8 或更高
- PReLU 支持: TensorRT 6.0+

---

### 5.2 FaceNet

**推荐程度:** ⭐⭐⭐ **Alternative**

**适用场景:**
- 已有 FaceNet 模型
- 需要不同特征空间

---

### 5.3 CurricularFace

**推荐程度:** ⭐⭐⭐ **Alternative**

**适用场景:**
- 需要更先进的人脸识别
- 对识别精度有更高要求

---

### 人脸质量评估

**python-ofiq (推荐):**

```python
from python_ofiq import FaceImageQuality

fiq = FaceImageQuality()
quality_score = fiq.assess(face_image)  # 返回 0-100 分数

# 包含指标:
# - Sharpness (清晰度)
# - IlluminationUniformity (光照均匀度)
# - BackgroundUniformity (背景一致性)
# - LuminanceMean (平均亮度)
```

**推荐程度:** ⭐⭐⭐⭐⭐ **Must Use**

---

## 6. 模型量化/优化工具

### 6.1 ONNX Runtime FP16

**方法:** 使用 FP16 精度模型

**效果:**
- 显存减少: 50% (FP32 → FP16)
- 速度提升: ~1.5-2x
- 精度损失: 可忽略

**推荐程度:** ⭐⭐⭐⭐⭐ **Must Use**

**inswapper_128_fp16.onnx:**
- 官方已提供 FP16 版本
- 直接使用，无需转换

---

### 6.2 onnxslim

**用途:** ONNX 模型无损压缩

```bash
pip install onnxslim
onnxslim inswapper_128_fp16.onnx slim_inswapper.onnx
```

**效果:**
- 模型体积减少: ~20-30%
- 推理速度提升: ~10-15%

**推荐程度:** ⭐⭐⭐⭐⭐ **Must Use**

---

### 6.3 TensorRT INT8

**方法:** INT8 量化 + 校准

**效果:**
- 显存减少: 75% (FP32 → INT8)
- 速度提升: ~2-3x
- 精度损失: 中等 (需校准数据集)

**RTX 4060 预估:**
- inswapper_128 INT8: ~3-5ms/帧
- VRAM 占用: ~1GB

**推荐程度:** ⭐⭐⭐ **Recommended (进阶)**

**校准要求:**
- 1000+ 张人脸图片
- 代表性强 (角度、光照、表情)

---

### 6.4 ONNX Dynamic Shapes

**用途:** 支持动态输入尺寸

**配置:**
```python
sess_options = ort.SessionOptions()
sess_options.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL

# 动态 batch
session = ort.InferenceSession(
    'model.onnx',
    sess_options,
    providers=['CUDAExecutionProvider']
)
```

**推荐程度:** ⭐⭐⭐⭐ **Recommended**

---

## 7. 音频处理

### 7.1 需求分析

**实时换脸场景:**
- 摄像头输入通常无音频
- 纯视觉处理，无需音频管线

**文件处理场景:**
- 需保留原视频音频
- FFmpeg 处理

### 7.2 FFmpeg 音频处理

```bash
# 提取原视频音频
ffmpeg -i input.mp4 -vn -acodec copy audio.aac

# 合成换脸后视频 + 原音频
ffmpeg -i swapped_video.mp4 -i audio.aac -c:v copy -c:a copy output.mp4
```

### 7.3 音视频同步

**关键点:**
- 帧级别时间戳对应
- FFmpeg `-vsync cfr` 保持帧率
- `-async 1` 音频同步

**推荐程度:** ⭐⭐⭐⭐ **Recommended**

---

## 8. 部署工具

### 8.1 pip install

**用途:** Python 包管理

```bash
pip install onnxruntime-gpu==1.18.0
pip install opencv-python==4.10.0.84
pip install insightface==0.7.3
pip install python-ofiq==0.1.0
```

**CUDA 版本对应:**

| CUDA | cuDNN | ONNX Runtime GPU | TensorRT |
|------|-------|------------------|----------|
| 12.1 | 8.9+ | 1.18+ | 8.6+ |
| 12.4 | 9.0+ | 1.18+ | 10.x |

**推荐程度:** ⭐⭐⭐⭐⭐ **Must Use**

---

### 8.2 PyInstaller

**用途:** 打包 CLI 工具为可执行文件

```bash
pip install pyinstaller==6.5.0
pyinstaller --onefile --name FaceVideoChange \
            --add-data "models;models" \
            --hidden-import=onnxruntime \
            --hidden-import=cv2 \
            facevidechange/cli.py
```

**注意:**
- 需在目标 OS 上打包 (Windows → Windows)
- 包含 CUDA 运行时 (~2GB)
- 模型文件单独分发

**推荐程度:** ⭐⭐⭐⭐ **Recommended**

---

### 8.3 conda 环境

**用途:** 隔离 CUDA 依赖

```bash
conda create -n facevideo python=3.10
conda activate facevideo
conda install cudatoolkit=12.1 cudnn=8.9
pip install onnxruntime-gpu insightface opencv-python
```

**推荐程度:** ⭐⭐⭐⭐⭐ **Must Use**

---

## 推荐技术栈总结

### 实时换脸管线架构

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

### RTX 4060 性能预估

| 阶段 | 模型 | 延迟 | VRAM |
|------|------|------|------|
| 人脸检测 | SCRFD-10GF | ~4ms | ~200MB |
| 人脸对齐 | 5点 landmarks | ~1ms | ~50MB |
| 特征提取 | ArcFace ResNet50 | ~5ms | ~300MB |
| 换脸 | inswapper_128_fp16 | ~10ms | ~1.5GB |
| 增强 | GFPGAN v1.4 (可选) | ~8ms | ~800MB |
| **总计** | — | **~28ms** | **~2.9GB** |

**预估 FPS:** 30-35 FPS (单脸，1080p)
**端到端延迟:** <100ms (满足目标)

---

## 版本兼容性矩阵

| 组件 | 推荐版本 | 兼容性说明 |
|------|----------|------------|
| Python | 3.10 / 3.11 | 3.12 可能存在依赖问题 |
| CUDA | 12.1 / 12.4 | RTX 4060 必需 |
| cuDNN | 8.9+ | 与 CUDA 版本匹配 |
| ONNX Runtime | 1.18+ | CUDA 12.x 支持 |
| TensorRT | 8.6 / 10.x | 可选进阶优化 |
| OpenCV | 4.10+ | VideoCapture 稳定性 |
| InsightFace | 0.7.3+ | SCRFD/ArcFace 集成 |
| FFmpeg | 6.x / 7.x | RTMP/音视频处理 |

---

## 备选方案

| 场景 | 推荐方案 | 备选方案 |
|------|----------|----------|
| 换脸模型 | Deep-Live-Cam + inswapper_128_fp16 | FaceFusion 3.0 |
| 推理框架 | ONNX Runtime | TensorRT (进阶) |
| 人脸检测 | SCRFD-10GF (InsightFace) | YOLOv8-face |
| 人脸识别 | ArcFace ResNet50 | CurricularFace |
| 视频捕获 | OpenCV VideoCapture | GStreamer (RTSP) |
| 推流/录制 | FFmpeg | OBS + virtual camera |
| 模型优化 | onnxslim | TensorRT INT8 |
| 人脸质量 | python-ofiq | CLIB-FIQA |

---

## 不推荐技术

| 技术 | 原因 | 推荐替代 |
|------|------|----------|
| MTCNN | 速度慢，不适合实时 | SCRFD / YOLOv8-face |
| DeepFaceLab | 需训练，不适合单图换脸 | Deep-Live-Cam |
| PyTorch (推理) | 性能/部署不如 ONNX | ONNX Runtime |
| TensorFlow | 换脸领域生态弱 | ONNX + 任意后端 |

---

## 安装命令

```bash
# 1. 创建 conda 环境
conda create -n facevideo python=3.10 -y
conda activate facevideo

# 2. 安装 CUDA 依赖
conda install cudatoolkit=12.1 cudnn=8.9 -y

# 3. 安装核心库
pip install onnxruntime-gpu==1.18.0
pip install insightface==0.7.3
pip install opencv-python==4.10.0.84
pip install python-ofiq==0.1.0
pip install onnxslim

# 4. 安装视频处理
pip install pillow numpy

# 5. 安装推流工具 (系统级)
# Ubuntu/Debian:
sudo apt install ffmpeg

# macOS:
brew install ffmpeg

# Windows:
# 下载 ffmpeg: https://ffmpeg.org/download.html

# 6. 克隆 Deep-Live-Cam
git clone https://github.com/hacksider/Deep-Live-Cam.git
cd Deep-Live-Cam

# 7. 下载模型文件
# inswapper_128_fp16.onnx (Hugging Face)
# SCRFD 模型 (InsightFace 自动下载)

# 8. 运行
python run.py --source face.jpg --webcam
```

---

## 资料来源

- [Deep-Live-Cam GitHub](https://github.com/hacksider/Deep-Live-Cam) — 核心换脸引擎
- [InsightFace SCRFD](https://github.com/deepinsight/insightface) — 人脸检测基准
- [WIDER FACE Benchmark](https://link.springer.com/content/pdf/10.1007/978-3-031-93103-1_11.pdf) — 检测精度对比
- [ONNX Runtime CUDA](https://onnxruntime.ai/docs/execution-providers/CUDA-ExecutionProvider.html) — 推理配置
- [TensorRT Model Optimizer](https://nvidia.github.io/TensorRT-Model-Optimizer/guides/_choosing_quant_methods.html) — 量化指南
- [FaceFusion 3.0](https://github.com/facefusion/facefusion/releases/tag/3.0.0) — 备选框架
- [python-ofiq](https://pypi.org/project/python-ofiq/0.1.0/) — 人脸质量评估
- [ONNX Slim](https://github.com/onnx/onnxruntime-tools) — 模型优化

---
*Stack research for: Real-time video stream face swapping*
*Researched: 2026-04-13*
