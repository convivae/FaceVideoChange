# Phase 1: 项目基础设施 - Research

**Researched:** 2026-04-17
**Domain:** Python CLI infrastructure, configuration management, logging
**Confidence:** HIGH

## Summary

Phase 1 需要建立一个可运行的项目骨架，提供 CLI 接口和配置管理系统。基于已锁定的决策（Typer + YAML + builtin presets），需要选择合适的技术方案来实现：

1. **Typer 1.1.0** 是构建 CLI 的标准选择，基于 Click 和 Rich，支持类型提示自动生成帮助文档
2. **PyYAML** 对于只读配置文件场景足够用，若需要注释保持考虑 ruamel.yaml
3. **标准 logging** vs **structlog**：考虑到用户要求"日志详细"，建议使用标准 logging + Rich 格式化输出，平衡简洁性和功能性
4. **src/ 布局** 是现代 Python 项目的推荐结构，与 `pyproject.toml` + `uv` 配合最佳

**Primary recommendation:** 使用 `src/` 布局 + `pyproject.toml` + `uv`，CLI 通过 `console_scripts` 入口点安装。

---

## User Constraints (from CONTEXT.md)

### Locked Decisions
- CLI 框架: Typer
- 配置格式: YAML
- 配置文件路径: `~/.facevidechange/config.yaml`
- 预设系统: builtin
- 日志详细程度: verbose，输出到 stdout
- 日志分级: DEBUG / INFO / WARNING / ERROR
- 日志包含时间戳、模块名、日志级别
- 项目根目录: `/Users/conv/aispace/FaceVideoChange`
- 主要代码: `src/` 目录
- 模型文件: `models/` 目录
- 配置文件: `config/` 目录

### Claude's Discretion
- 日志格式具体样式（颜色、字体）
- 预设文件的具体参数值（由后续阶段决定）
- 项目目录结构细节（可由 planner 根据实际需求决定）
- 测试框架选择

### Deferred Ideas (OUT OF SCOPE)
- GUI 界面 — Phase 8 之后考虑
- Web 界面 — 暂不考虑

---

## Architectural Responsibility Map

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|-------------|----------------|-----------|
| CLI argument parsing | CLI Layer | — | Typer handles all CLI parsing |
| Config file loading | Config Layer | — | YAML parsing, path resolution |
| Preset system | Config Layer | CLI Layer | Presets define default configs |
| Logging | Shared | All layers | Standard library, injected via module-level loggers |
| Entry point installation | Build/Packaging | — | pyproject.toml console_scripts |
| Config directory creation | CLI Layer | OS Layer | XDG compliance for `~/.facevidechange/` |

---

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| **Typer** | 1.1.0 | CLI framework | 基于 Click + Rich，类型提示即 CLI 接口，自动生成 `--help` |
| **PyYAML** | 6.0+ | YAML 解析 | 配置文件只读，无需注释保留，PyYAML 足够 |
| **Rich** | 13.0+ | 终端格式化 | Typer 依赖项，日志美化输出 |
| **click** | 8.1+ | CLI 基础 | Typer 底层依赖 |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| **ruamel.yaml** | 0.18+ | YAML 解析（可选） | 需要保留配置文件注释时 |
| **structlog** | 25.0+ | 结构化日志 | 需要 JSON 输出/日志聚合时 |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| Typer | Click | Click 需要手动参数定义，Typer 类型提示更简洁 |
| Typer | argparse | argparse API 繁琐，Typer 更现代 |
| PyYAML | ruamel.yaml | PyYAML 足够只读场景，ruamel.yaml 用于需要注释保留 |
| 标准 logging | structlog | 标准 logging 足够简单场景，structlog 用于生产环境日志聚合 |
| uv | pip | uv 快 10-100x，支持锁文件，推荐用于项目依赖管理 |
| uv | poetry | uv 性能更好，poetry 功能更成熟 |

**Installation:**
```bash
uv add typer pyyaml rich click
uv add --dev pytest pytest-asyncio
```

---

## Architecture Patterns

### System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         User CLI Input                           │
│  (facevidechange --preset realtime-8gb --dry-run)              │
└──────────────────────────────┬──────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Typer CLI Layer                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐ │
│  │ --help      │  │ --preset    │  │ --dry-run               │ │
│  │ 显示帮助    │  │ 加载预设    │  │ 验证配置不启动处理      │ │
│  └─────────────┘  └─────────────┘  └─────────────────────────┘ │
└──────────────────────────────┬──────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Config Layer                                  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │ 1. 加载 ~/.facevidechange/config.yaml                   │    │
│  │ 2. 应用 --preset 预设（builtin/realtime-8gb）          │    │
│  │ 3. 应用 CLI 参数覆盖                                    │    │
│  │ 4. 环境变量覆盖                                         │    │
│  │ 5. 最终配置合并                                         │    │
│  └─────────────────────────────────────────────────────────┘    │
└──────────────────────────────┬──────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Logging Layer                                 │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │ 详细日志: 启动步骤、预热进度、运行时状态                │    │
│  │ 格式: [TIMESTAMP] [LEVEL] [module] Message              │    │
│  │ 输出: stdout (可重定向)                                 │    │
│  └─────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
```

### Recommended Project Structure
```
FaceVideoChange/
├── src/
│   └── facevidechange/
│       ├── __init__.py
│       ├── __main__.py          # 支持 python -m facevidechange
│       ├── cli.py               # Typer CLI 定义
│       ├── config/
│       │   ├── __init__.py
│       │   ├── loader.py        # YAML 配置加载
│       │   ├── presets.py       # 预设系统
│       │   └── defaults.py     # 默认配置
│       ├── logging/
│       │   ├── __init__.py
│       │   └── setup.py         # 日志配置
│       └── models/              # Phase 2+ 填入
├── tests/
│   ├── __init__.py
│   ├── test_cli.py
│   ├── test_config.py
│   └── test_logging.py
├── config/
│   └── presets.yaml             # 内置预设定义
├── models/                      # Phase 2+ 下载模型
├── pyproject.toml
├── uv.lock
└── README.md
```

### Pattern 1: Typer CLI with Type Hints
**What:** 使用类型提示定义 CLI 参数
**When to use:** 所有 CLI 命令定义
**Example:**
```python
# Source: https://typer.tiangolo.com/
import typer

app = typer.Typer()

@app.command()
def run(
    source: str = typer.Option(..., help="源图片路径"),
    webcam: bool = typer.Option(False, help="启用摄像头"),
    preset: str = typer.Option("default", help="预设名称"),
    dry_run: bool = typer.Option(False, help="仅验证配置"),
):
    """运行换脸程序"""
    if dry_run:
        typer.echo("Dry run mode - 配置验证通过")
    else:
        typer.echo(f"使用预设: {preset}")

if __name__ == "__main__":
    app()
```

### Pattern 2: YAML Config with Override Priority
**What:** 配置分层加载，CLI 参数 > 环境变量 > 预设 > 默认值
**When to use:** 配置管理系统
**Example:**
```python
# Source: [ASSUMED]
import yaml
from pathlib import Path
from typing import Any

class Config:
    """配置管理，按优先级合并: CLI > ENV > preset > defaults"""

    def __init__(self, defaults_path: Path, preset_path: Path, config_dir: Path):
        self.defaults = self._load_yaml(defaults_path)
        self.presets = self._load_yaml(preset_path)
        self.user_config = self._load_user_config(config_dir)

    def get(self, key: str, preset: str = "default") -> Any:
        # 优先级: user_config > preset > defaults
        base = self.defaults.copy()
        base.update(self.presets.get(preset, {}))
        base.update(self.user_config.get(key, {}))
        return base.get(key)

    def _load_user_config(self, config_dir: Path) -> dict:
        config_file = config_dir / "config.yaml"
        if config_file.exists():
            return self._load_yaml(config_file)
        return {}

    @staticmethod
    def _load_yaml(path: Path) -> dict:
        with open(path) as f:
            return yaml.safe_load(f) or {}
```

### Pattern 3: XDG-Compliant Config Directory
**What:** 遵循 XDG 基本目录规范创建配置目录
**When to use:** 首次运行配置目录创建
**Example:**
```python
# Source: [ASSUMED]
from pathlib import Path
import os

def get_config_dir() -> Path:
    """获取配置目录，遵循 XDG 规范"""
    xdg_config = os.environ.get("XDG_CONFIG_HOME")
    if xdg_config:
        return Path(xdg_config) / "facevidechange"

    # 回退到 ~/.facevidechange
    return Path.home() / ".facevidechange"

def ensure_config_dir() -> Path:
    """确保配置目录存在"""
    config_dir = get_config_dir()
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir
```

### Anti-Patterns to Avoid
- **硬编码配置路径**: 使用 `~/.facevidechange/config.yaml`，但应支持 `XDG_CONFIG_HOME` 环境变量
- **全局单例日志**: 应使用模块级 logger，通过 `logging.getLogger(__name__)` 获取
- **配置文件缺少默认值**: 所有配置项必须有合理的默认值，新用户无需配置文件即可运行

---

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| CLI 参数解析 | argparse 手动定义 | Typer | 类型提示自动生成帮助，代码简洁 |
| YAML 解析 | 正则解析 YAML | PyYAML/ruamel.yaml | 已优化处理边缘情况 |
| 日志格式化 | 自定义格式字符串 | Rich + logging | Rich 提供专业终端美化 |
| 依赖解析 | requirements.txt | uv + pyproject.toml | uv 快 10-100x，支持锁文件 |

---

## Common Pitfalls

### Pitfall 1: Config Directory Not Created
**What goes wrong:** 用户首次运行报错 `FileNotFoundError: ~/.facevidechange/config.yaml`
**Why it happens:** 配置目录不存在，代码未自动创建
**How to avoid:** CLI 入口点检查并创建配置目录
**Warning signs:** `FileNotFoundError` 在首次运行时报出

### Pitfall 2: Preset Not Found
**What goes wrong:** `--preset unknown-preset` 无提示继续运行
**Why it happens:** 预设加载失败静默回退到默认值
**How to avoid:** 预设加载时验证名称，存在时明确报错
**Warning signs:** 用户不知使用了哪个预设

### Pitfall 3: Log Level Not Respected
**What goes wrong:** DEBUG 日志在生产环境输出过多
**Why it happens:** 默认日志级别设置不当
**How to avoid:** 默认 INFO，通过 `--verbose` 或 `--debug` 提升
**Warning signs:** 输出过于冗长或过于简略

### Pitfall 4: Config Override Priority Wrong
**What goes wrong:** CLI 参数未生效，用户困惑
**Why it happens:** 配置合并顺序错误
**How to avoid:** 严格按 D-10 顺序合并：CLI > ENV > preset > defaults
**Warning signs:** 配置文件值覆盖 CLI 参数

---

## Code Examples

### CLI Entry Point (pyproject.toml)
```toml
# Source: https://packaging.python.org/guides/writing-pyproject-toml/
[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "facevidechange"
version = "0.1.0"
description = "Real-time video face swapping CLI tool"
requires-python = ">=3.10"
dependencies = [
    "typer>=1.1.0",
    "pyyaml>=6.0",
    "rich>=13.0",
]

[project.scripts]
facevidechange = "facevidechange.cli:app"

[project.optional-dependencies]
dev = [
    "pytest>=8.0",
    "pytest-asyncio>=0.23",
]
```

### Logging Setup with Rich
```python
# Source: [ASSUMED]
import logging
from rich.logging import RichHandler
from rich.console import Console

def setup_logging(verbose: bool = False):
    """配置日志系统"""
    level = logging.DEBUG if verbose else logging.INFO

    logging.basicConfig(
        level=level,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(console=Console(stderr=True), rich_tracebacks=True)]
    )

    # 返回根 logger
    return logging.getLogger("facevidechange")
```

### Preset Loading
```python
# Source: [ASSUMED]
import yaml
from pathlib import Path
from typing import Optional

def load_preset(preset_name: str, preset_file: Path) -> dict:
    """加载内置预设"""
    with open(preset_file) as f:
        all_presets = yaml.safe_load(f)

    if preset_name not in all_presets:
        raise ValueError(f"未知预设: {preset_name}. 可用预设: {list(all_presets.keys())}")

    return all_presets[preset_name]
```

---

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| requirements.txt | pyproject.toml + uv | 2024+ | 标准化依赖声明，支持锁文件 |
| argparse | Typer (基于 Click) | 2020+ | 类型提示即 CLI 接口 |
| 手动日志格式 | Rich 美化输出 | 2020+ | 专业终端体验 |
| pip | uv | 2024+ | 性能提升 10-100x |

**Deprecated/outdated:**
- `setup.py`: 已被 `pyproject.toml` 取代
- `pipenv`: uv 性能优势明显
- `Click` 直接使用: Typer 在 Click 基础上提供更简洁 API

---

## Assumptions Log

| # | Claim | Section | Risk if Wrong |
|---|-------|---------|---------------|
| A1 | Typer 1.1.0 稳定可用 | Standard Stack | 低 - 官方文档确认 |
| A2 | PyYAML 足够只读配置场景 | Standard Stack | 低 - ruamel.yaml 可作为备选 |
| A3 | src/ 布局适合本项目 | Architecture Patterns | 低 - 行业推荐结构 |
| A4 | uv 0.11.6 满足需求 | Environment | 低 - 已验证 |

---

## Open Questions

1. **预设参数值具体内容**
   - What we know: 预设包含 `realtime-8gb`，用于 RTX 4060 实时换脸
   - What's unclear: 具体参数名和值（如 batch_size、max_faces 等）
   - Recommendation: Phase 2 期间根据模型需求确定

2. **测试框架选择**
   - What we know: 用户提到 CLI's Discretion 可由 planner 决定
   - What's unclear: pytest vs pytest-asyncio vs 其他
   - Recommendation: 使用 pytest + pytest-asyncio（STACK.md 已推荐）

---

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|------------|------------|-----------|---------|----------|
| Python | 项目运行 | ✓ | 3.14.4 | Python 3.10+ 需要 |
| uv | 依赖管理 | ✓ | 0.11.6 | pip 可用但较慢 |
| pip | 备选包管理 | ✓ | 26.0.1 | — |
| CUDA | GPU 推理 | ? | 未检查 | Phase 2 检查 |

**Missing dependencies with no fallback:**
- CUDA Toolkit 12.1+ (Phase 2 模型推理必需)

**Missing dependencies with fallback:**
- None identified for Phase 1

---

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | pytest 8.0+ |
| Config file | pytest.ini 或 pyproject.toml [tool.pytest] |
| Quick run command | `pytest tests/test_cli.py -x -v` |
| Full suite command | `pytest tests/ -v` |

### Phase Requirements → Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| REQ-P1-01 | `--help` 显示完整参数说明和示例 | CLI smoke | `facevidechange --help` | Wave 0 |
| REQ-P1-02 | `--preset realtime-8gb` 加载预设 | CLI unit | `pytest tests/test_cli.py::test_preset_loading` | Wave 0 |
| REQ-P1-03 | `--dry-run` 验证配置不启动 | CLI unit | `pytest tests/test_cli.py::test_dry_run` | Wave 0 |
| REQ-P1-04 | 配置项有合理默认值 | Config unit | `pytest tests/test_config.py::test_defaults` | Wave 0 |
| REQ-P1-05 | 日志记录启动/预热/运行状态 | Logging unit | `pytest tests/test_logging.py` | Wave 0 |

### Sampling Rate
- **Per task commit:** `pytest tests/test_cli.py -x -q`
- **Per wave merge:** `pytest tests/ -v`
- **Phase gate:** Full suite green before `/gsd-verify-work`

### Wave 0 Gaps
- [ ] `tests/test_cli.py` — covers REQ-P1-01, REQ-P1-02, REQ-P1-03
- [ ] `tests/test_config.py` — covers REQ-P1-04
- [ ] `tests/test_logging.py` — covers REQ-P1-05
- [ ] `tests/conftest.py` — shared fixtures
- [ ] Framework install: `uv add --dev pytest pytest-asyncio`

---

## Security Domain

### Applicable ASVS Categories
| ASVS Category | Applies | Standard Control |
|---------------|---------|-----------------|
| V2 Authentication | No | N/A - CLI 工具无需认证 |
| V3 Session Management | No | N/A - 无会话概念 |
| V4 Access Control | No | N/A - 本地工具 |
| V5 Input Validation | Yes | Typer 类型提示 + pydantic (可选) |
| V6 Cryptography | No | 无加密需求 |

### Known Threat Patterns for Python CLI
| Pattern | STRIDE | Standard Mitigation |
|---------|--------|---------------------|
| Config injection | Tampering | PyYAML safe_load，避免 eval |
| Path traversal | Information Disclosure | 使用 Path.resolve() 规范化路径 |
| Env var injection | Tampering | 环境变量值需要验证 |

---

## Sources

### Primary (HIGH confidence)
- [Typer Official Docs](https://typer.tiangolo.com/) - CLI 框架用法
- [Python Packaging User Guide - pyproject.toml](https://packaging.python.org/guides/writing-pyproject-toml/) - 打包配置
- [Python Packaging User Guide - src layout](https://packaging.python.org/discussions/src-layout-vs-flat-layout/) - 项目结构

### Secondary (MEDIUM confidence)
- [Real Python - Python YAML](https://www.realpython.com/python-yaml/) - YAML 配置
- [Medium - Python Logging](https://medium.com/@dhruvshirar/structured-logging-in-python-a-practical-guide-for-production-systems-9659f461fa93) - 日志最佳实践

### Tertiary (LOW confidence)
- [Medium - Python Project Structure 2026](https://medium.com/the-pythonworld/the-cleanest-way-to-structure-a-python-project-in-2026-7cb1baee6ca6) - 项目结构趋势
- [Medium - UV Dependency Management](https://levelup.gitconnected.com/modern-python-development-with-pyproject-toml-and-uv-405dfb8b6ec8) - uv 使用

---

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - 基于官方文档和验证的工具版本
- Architecture: HIGH - 遵循行业最佳实践
- Pitfalls: MEDIUM - 基于常见 CLI 项目问题模式

**Research date:** 2026-04-17
**Valid until:** 2026-05-17 (30 days for stable stack)
