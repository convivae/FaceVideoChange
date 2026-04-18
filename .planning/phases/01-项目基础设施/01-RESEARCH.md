# Phase 1: 项目基础设施 - Research

**Gathered:** 2026-04-14
**Status:** Ready for planning

## Phase Scope

Build a runnable project skeleton with CLI interface and configuration management system.

## Research Summary

### 1. CLI Framework: Typer

**Recommendation: typer[cli] + rich**

Typer 使用 RFC 7807 错误格式，基于 Click，但具有类型安全优势：

- `typer[cli]` 自动安装 rich (美化输出)
- `--help` 自动生成（基于函数签名）
- 子命令通过 `@app.command()` 实现
- 类型注解 → 参数解析和验证
- 添加 `rich` 可获得彩色输出和表格

**参考代码结构：**
```python
import typer
from typing import Optional
from rich.console import Console

app = typer.Typer(add_completion=False)
console = Console()

@app.command()
def main(
    source: str = typer.Option(..., "--source", help="Source video or camera"),
    face: str = typer.Option(..., "--face", help="Target face image"),
    preset: Optional[str] = typer.Option(None, "--preset", help="Preset name"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Validate config only"),
):
    ...
```

### 2. Configuration: YAML + ruamel.yaml

**Recommendation: ruamel.yaml (保留注释)**

PyYAML 会丢失注释，ruamel.yaml 支持保留 YAML 注释和格式：
```python
from ruamel.yaml import YAML
yaml = YAML()
yaml.preserve_quotes = True
yaml.default_flow_style = False
```

**配置覆盖优先级：**
CLI args > 环境变量 > 预设 > 默认值

**XDG 兼容路径：**
```python
from pathlib import Path
import os

config_dir = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config"))
config_file = config_dir / "facevidechange" / "config.yaml"
```

**默认配置结构：**
```yaml
# ~/.facevidechange/config.yaml
facevidechange:
  version: "1.0"
  models_dir: "~/.facevidechange/models"
  cache_dir: "~/.facevidechange/cache"
  log_level: "INFO"
  log_file: null
```

### 3. Preset System

**设计：内置预设 + 可扩展**

```python
PRESETS = {
    "realtime-8gb": {
        "fps": 30,
        "resolution": [1280, 720],
        "model": "inswapper_128_fp16",
        "quality": 75,
        "face_swap_strength": 0.85,
    },
    "quality-8gb": {
        "fps": 15,
        "resolution": [1920, 1080],
        "model": "inswapper_128_fp16",
        "quality": 90,
        "face_swap_strength": 1.0,
    },
}
```

预设覆盖机制：
1. 加载默认配置
2. 加载预设（覆盖）
3. 加载用户配置（覆盖）
4. 加载 CLI 参数（最高优先）

### 4. Logging System

**Recommendation: standard logging + rich handler**

```python
import logging
from rich.logging import RichHandler
from rich.console import Console

def setup_logging(level: str = "INFO"):
    console = Console(stderr=True)
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(console=console, rich_tracebacks=True)],
    )
```

**日志分级：**
- DEBUG: 开发调试
- INFO: 启动、预热、运行时状态
- WARNING: 非致命问题（如网络不稳定）
- ERROR: 致命错误

**日志内容要求：**
- 启动步骤：配置加载 → 模型加载 → GPU 检测
- 预热进度：每个模型加载进度条
- 运行时：FPS、GPU 利用率、处理帧数

### 5. Project Structure

**推荐结构：**
```
FaceVideoChange/
├── src/
│   └── facevidechange/
│       ├── __init__.py
│       ├── __main__.py          # python -m facevidechange
│       ├── cli.py                # Typer app + commands
│       ├── config.py             # Config loading + preset system
│       ├── logging_.py          # Logging setup
│       ├── models/               # Model management
│       │   ├── __init__.py
│       │   ├── detector.py      # Face detection
│       │   ├── embedder.py      # Face embedding
│       │   └── swaper.py        # Face swapping
│       ├── pipeline/             # Processing pipeline
│       │   ├── __init__.py
│       │   └── processor.py     # Main pipeline
│       └── io/                  # Input/Output
│           ├── __init__.py
│           ├── capture.py        # Video capture
│           └── streamer.py       # RTMP streaming
├── models/                     # Default models directory
├── config/                    # Built-in presets
│   └── presets.yaml
├── tests/
├── pyproject.toml
├── uv.lock
└── README.md
```

### 6. Dependency Management

**Recommendation: uv (Astral 工具)**

uv 是最快 Python 包管理器，兼容 pip 和 pyproject.toml：
```bash
pip install uv
uv init
uv add typer rich ruamel.yaml opencv-python onnxruntime-gpu insightface
```

**pyproject.toml 示例：**
```toml
[project]
name = "facevidechange"
version = "0.1.0"
requires-python = ">=3.10"
dependencies = [
    "typer[cli]>=0.12.0",
    "rich>=13.0.0",
    "ruamel.yaml>=0.18.0",
    "opencv-python>=4.10.0",
    "onnxruntime-gpu>=1.18.0",
    "insightface>=0.7.0",
]

[project.scripts]
facevidechange = "facevidechange.cli:main"
```

### 7. Model Directory Management

```python
from pathlib import Path
import os

def get_models_dir() -> Path:
    """Get models directory, create if not exists."""
    models_dir = Path.home() / ".facevidechange" / "models"
    models_dir.mkdir(parents=True, exist_ok=True)
    return models_dir

def ensure_models() -> list[str]:
    """Download/check required models."""
    # inswapper_128_fp16.onnx from Deep-Live-Cam
    # SCRFD-10GF from InsightFace model zoo
    pass
```

### 8. XDG Compliance

遵循 XDG Base Directory Specification：
- 配置: `$XDG_CONFIG_HOME/facevidechange/` (默认 `~/.config/facevidechange/`)
- 数据: `$XDG_DATA_HOME/facevidechange/` (默认 `~/.local/share/facevidechange/`)
- 缓存: `$XDG_CACHE_HOME/facevidechange/` (默认 `~/.cache/facevidechange/`)

## Validation Architecture

Phase 1 主要是工程基础设施，验证维度：
1. CLI --help 正常显示
2. --dry-run 不启动实际处理
3. --preset realtime-8gb 加载正确配置
4. 日志输出正常（包含时间戳/模块/级别）
5. 配置文件路径符合 XDG 规范

## Risk Assessment

| Risk | Severity | Mitigation |
|------|----------|------------|
| Typer 升级导致兼容性问题 | Low | 锁定版本 ~0.12.0 |
| CUDA 检测失败 | Medium | 日志详细提示 + fallback 说明 |
| 模型下载失败 | Medium | 提供手动下载链接 |
| XDG 路径权限问题 | Low | graceful fallback 到 ~/.facevidechange |

## Notes for Planning

- Phase 1 不包含任何换脸逻辑，只搭建基础设施
- 模型下载逻辑在 Phase 2 中实现
- 摄像头捕获在 Phase 4 中实现
- RTMP 推流在 Phase 4 中实现
