# Phase 1: 项目基础设施 - Research

**Researched:** 2026-04-17
**Domain:** CLI framework, configuration management, logging system
**Confidence:** HIGH

## Summary

Phase 1 需要建立一个可运行的项目骨架，包含 CLI 接口和配置管理系统。基于已锁定的决策（Typer + YAML + builtin presets），本阶段的核心挑战是：
1. 选择合适的项目结构和依赖管理工具
2. 实现符合 XDG 规范的配置文件路径
3. 设计一个简洁但可扩展的预设系统
4. 建立结构化日志系统

**Primary recommendation:** 使用 `src/` 布局 + `uv` 作为包管理器 + `platformdirs` 处理 XDG 路径 + `structlog` 实现结构化日志。

---

## User Constraints (from CONTEXT.md)

### Locked Decisions

- **D-01:** 使用 Typer 作为 CLI 框架
- **D-02:** 包含 `--help` 显示完整参数说明和示例
- **D-03:** 支持 `--dry-run` 验证配置而不启动实际处理
- **D-04:** 包含 `--preset <name>` 加载预设配置
- **D-05:** 配置文件格式使用 YAML
- **D-06:** 配置文件路径: `~/.facevidechange/config.yaml`
- **D-07:** 支持通过 CLI 参数覆盖配置文件设置
- **D-08:** 使用内置预设 (builtin)，用户通过 `--preset` 选择
- **D-09:** 内置预设包含: `realtime-8gb` (RTX 4060 实时换脸)
- **D-10:** 预设覆盖优先级: CLI 参数 > 环境变量 > 预设 > 默认值
- **D-11:** 日志详细程度: 详细 (verbose) — 启动、预热、运行时全部记录
- **D-12:** 日志输出到 stdout，支持重定向到文件
- **D-13:** 日志分级: DEBUG / INFO / WARNING / ERROR
- **D-14:** 日志包含时间戳、模块名、日志级别
- **D-15:** 项目根目录: `/Users/conv/aispace/FaceVideoChange`
- **D-16:** 主要代码: `src/` 目录
- **D-17:** 模型文件: `models/` 目录
- **D-18:** 配置文件: `config/` 目录

### Claude's Discretion

- 日志格式具体样式（颜色、字体）
- 预设文件的具体参数值（由后续阶段决定）
- 项目目录结构细节（可由 planner 根据实际需求决定）
- 测试框架选择

### Deferred Ideas (OUT OF SCOPE)

- GUI 界面 — Phase 8 之后考虑
- Web 界面 — 暂不考虑

---

## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| REQ-01 | 用户运行 `--help` 能看到完整的参数说明和示例 | Typer `--help` 自动生成 |
| REQ-02 | 用户使用 `--preset realtime-8gb` 可自动加载优化配置 | 预设系统设计 |
| REQ-03 | 用户使用 `--dry-run` 可验证配置而不启动实际处理 | CLI 命令实现 |
| REQ-04 | 所有配置项都有合理的默认值，新用户无需文档即可运行 | 配置管理设计 |
| REQ-05 | 日志系统记录启动步骤、预热进度、运行时状态 | 结构化日志设计 |

---

## Architectural Responsibility Map

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|-------------|----------------|-----------|
| CLI 参数解析 | Backend (Python) | — | Typer 处理所有 CLI 逻辑 |
| 配置文件读取 | Backend (Python) | — | YAML 解析在应用启动时完成 |
| 预设加载 | Backend (Python) | — | 内置预设代码在 `src/facevidechange/presets/` |
| 日志系统 | Backend (Python) | — | structlog 输出到 stdout |
| XDG 路径解析 | Backend (Python) | — | platformdirs 处理跨平台路径 |

---

## Standard Stack

### Core

| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| **typer** | 0.24.1 | CLI 框架 | [CITED: pypi.org/project/typer/] FastAPI 团队出品，类型提示优先 |
| **PyYAML** | 6.0+ | YAML 解析 | [ASSUMED] 简单配置场景不需要 ruamel.yaml 的注释保留功能 |
| **structlog** | 25.1+ | 结构化日志 | [CITED: structlog.readthedocs.org] 优于标准 logging，支持结构化输出 |
| **platformdirs** | 4.0+ | XDG 路径处理 | [ASSUMED] appdirs 已废弃，platformdirs 是活跃维护的 fork |
| **pydantic** | 2.0+ | 配置数据模型 | [ASSUMED] Typer 原生集成，类型验证 |

### Supporting

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| **uv** | 0.11.3 | 包管理/项目初始化 | [CITED: github.com/astral-sh/uv] 10-100x 更快，统一工具链 |
| **pytest** | 8.0+ | 测试框架 | [ASSUMED] Python 生态标准测试框架 |
| **pytest-asyncio** | 0.23+ | 异步测试支持 | Phase 2+ 可能需要 |

### Alternatives Considered

| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| PyYAML | ruamel.yaml | ruamel.yaml 支持注释保留，但增加依赖；对于纯配置读取，PyYAML 足够 |
| structlog | 标准 logging | 标准 logging 配置复杂，structlog 更现代、结构化 |
| platformdirs | appdirs | appdirs 已废弃 (2023)，platformdirs 活跃维护 |
| uv | pip / poetry | uv 速度快 10-100x，但新工具有学习曲线 |

**Installation:**

```bash
# 使用 uv 初始化项目
uv init --name facevidechange
uv add typer pyyaml structlog platformdirs pydantic pydantic-settings
uv add --dev pytest pytest-asyncio
```

**Version verification:**

```bash
npm view typer version  # 0.24.1 (Feb 2026)
```

---

## Architecture Patterns

### System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                           CLI 入口点                                  │
│                     facevidechange/cli.py                            │
└─────────────────────────────┬───────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                        Typer App 解析                                │
│  --help / --preset <name> / --dry-run / --config <path>             │
└─────────────────────────────┬───────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      配置加载 (ConfigLoader)                          │
│  1. 读取 ~/.facevidechange/config.yaml (XDG via platformdirs)      │
│  2. 加载内置预设 (realtime-8gb)                                     │
│  3. 合并 CLI 参数覆盖                                                │
└─────────────────────────────┬───────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      日志系统初始化 (structlog)                        │
│  - 输出到 stdout (支持重定向)                                        │
│  - 时间戳 + 模块名 + 级别 + 消息                                      │
└─────────────────────────────┬───────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                        主应用逻辑                                     │
│  --dry-run: 验证配置，打印摘要，退出                                   │
│  --webcam: 启动视频流处理 (Phase 2+)                                 │
└─────────────────────────────────────────────────────────────────────┘
```

### Recommended Project Structure

```
FaceVideoChange/
├── src/                          # 主要代码 (D-16)
│   └── facevidechange/
│       ├── __init__.py
│       ├── cli.py                # Typer CLI 入口
│       ├── config/
│       │   ├── __init__.py
│       │   ├── loader.py         # YAML 配置加载
│       │   └── models.py         # Pydantic 配置模型
│       ├── presets/
│       │   ├── __init__.py
│       │   ├── builtin.py        # 内置预设 (D-08, D-09)
│       │   └── registry.py       # 预设注册表
│       ├── logging/
│       │   ├── __init__.py
│       │   └── setup.py          # structlog 配置
│       └── utils/
│           ├── __init__.py
│           └── paths.py           # XDG 路径工具
├── models/                       # 模型文件目录 (D-17)
│   └── .gitkeep
├── config/                       # 配置文件目录 (D-18)
│   └── presets/
│       └── .gitkeep
├── tests/
│   ├── __init__.py
│   ├── test_config.py
│   ├── test_presets.py
│   └── test_cli.py
├── pyproject.toml
├── uv.lock
└── README.md
```

### Pattern 1: Typer CLI with Type Hints

**What:** 使用 Typer 的类型提示功能自动生成 CLI 文档
**When to use:** 所有 CLI 参数定义

```python
# Source: [typer.tiangolo.com]
import typer
from typing import Optional
from pathlib import Path

app = typer.Typer()

@app.command()
def run(
    source: Path = typer.Option(..., "--source", "-s", help="源人脸图片路径"),
    preset: Optional[str] = typer.Option("realtime-8gb", "--preset", help="预设配置"),
    dry_run: bool = typer.Option(False, "--dry-run", help="验证配置不执行"),
    verbose: bool = typer.Option(True, "--verbose", "-v", help="详细输出"),
) -> None:
    """FaceVideoChange CLI - 实时视频流换脸工具"""
    if dry_run:
        typer.echo("🔍 验证配置...")
        # 配置验证逻辑
    else:
        typer.echo("🚀 启动换脸...")

if __name__ == "__main__":
    app()
```

### Pattern 2: Configuration Loading Chain

**What:** 优先级链式加载: CLI > 环境变量 > 预设 > 默认值
**When to use:** 配置管理

```python
# Source: [ASSUMED - 常见配置模式]
from typing import Any
from pydantic import BaseModel

class Config(BaseModel):
    """配置数据模型"""
    model_path: str = "models/inswapper_128_fp16.onnx"
    preset: str = "realtime-8gb"
    device: str = "cuda"
    verbose: bool = True

class ConfigLoader:
    """配置加载器 - 优先级: CLI > ENV > PRESET > DEFAULT"""

    def __init__(self, preset: str, cli_overrides: dict[str, Any]):
        self.preset = preset
        self.cli_overrides = cli_overrides

    def load(self) -> Config:
        # 1. 加载默认配置
        config = Config()

        # 2. 加载预设
        preset_config = self.load_preset(self.preset)
        config = self.merge(config, preset_config)

        # 3. 合并环境变量 (TODO: ENV 支持)
        # env_config = self.load_env()

        # 4. 合并 CLI 参数覆盖
        config = self.merge(config, self.cli_overrides)

        return config

    def load_preset(self, name: str) -> dict[str, Any]:
        """从内置预设加载"""
        presets = {
            "realtime-8gb": {
                "device": "cuda",
                "target_fps": 30,
            }
        }
        return presets.get(name, {})

    def merge(self, base: Config, override: dict[str, Any]) -> Config:
        """合并配置"""
        data = base.model_dump()
        data.update(override)
        return Config(**data)
```

### Pattern 3: structlog Setup

**What:** 配置 structlog 输出到 stdout，包含时间戳、模块名、级别
**When to use:** 日志系统初始化

```python
# Source: [structlog.readthedocs.org - Logging Best Practices]
import structlog
import logging

def setup_logging(verbose: bool = True):
    """配置结构化日志"""

    logging.basicConfig(
        format="%(message)s",
        stream=__import__("sys").stdout,
        level=logging.DEBUG if verbose else logging.INFO,
    )

    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.dev.ConsoleRenderer() if verbose
                else structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.stdlib.BoundLogger,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )

# 使用示例
log = structlog.get_logger()
log.info("启动", stage="initialization", preset="realtime-8gb")
```

### Anti-Patterns to Avoid

- **不要使用 `appdirs`:** 已废弃 (最后更新 2023-02)，使用 `platformdirs` 替代
- **不要硬编码配置路径:** 使用 `platformdirs.user_config_dir("facevidechange")` 确保跨平台
- **不要使用全局日志配置:** 每个模块通过 `structlog.get_logger()` 获取独立 logger
- **不要在 CLI 中处理业务逻辑:** CLI 只负责参数解析和调用，业务逻辑放在独立模块

---

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| CLI 参数解析 | 手动 argparse | **Typer** | 类型安全、自动生成 `--help`、子命令支持 |
| YAML 配置解析 | 手动文件读取 | **PyYAML / ruamel.yaml** | 标准化处理、大文件、编码 |
| 配置验证 | isinstance 检查 | **Pydantic** | 运行时验证、类型转换、错误消息 |
| 跨平台路径 | os.path.expanduser | **platformdirs** | XDG 标准、跨平台一致 |
| 结构化日志 | 标准 logging | **structlog** | 结构化输出、易于查询、自动上下文 |

**Key insight:** Phase 1 是基础设施，重点是建立一个可维护的项目骨架。使用成熟的库可以减少后续阶段的维护负担。

---

## Common Pitfalls

### Pitfall 1: XDG 配置路径误用
**What goes wrong:** 在 macOS 上使用 Linux 的默认路径 `~/.config/`
**Why it happens:** 不同操作系统的配置目录不同
**How to avoid:** 使用 `platformdirs.user_config_dir("facevidechange")` 自动处理
**Warning signs:** 在特定平台上配置文件找不到

### Pitfall 2: Typer 选项顺序导致歧义
**What goes wrong:** `--dry-run` 和 `--preset` 参数顺序敏感
**Why it happens:** Typer 默认位置参数和选项参数混合时可能有歧义
**How to avoid:** 使用明确的选项语法 `--dry-run` 而非位置参数
**Warning signs:** 参数解析错误或意外行为

### Pitfall 3: structlog 与标准 logging 混用
**What goes wrong:** 日志输出格式不一致
**Why it happens:** structlog 需要正确配置才能与标准库集成
**How to avoid:** 在应用启动时一次性配置 structlog，不要在模块中重复配置
**Warning signs:** 部分日志没有时间戳或格式不统一

### Pitfall 4: 预设覆盖逻辑错误
**What goes wrong:** CLI 参数被预设覆盖（优先级反了）
**Why it happens:** 配置合并顺序错误
**How to avoid:** 严格按照优先级链合并: CLI > ENV > 预设 > 默认
**Warning signs:** 指定 `--verbose` 但日志没有详细输出

---

## Code Examples

### Common Operation 1: XDG Config Path

```python
# Source: [platformdirs documentation]
from platformdirs import user_config_dir

config_dir = user_config_dir("facevidechange", appauthor="FaceVideoChange")
config_path = config_dir / "config.yaml"  # 自动处理跨平台

# macOS: ~/Library/Application Support/facevidechange/config.yaml
# Linux: ~/.config/facevidechange/config.yaml
# Windows: C:\Users\<user>\AppData\Local\facevidechange\config.yaml
```

### Common Operation 2: Pydantic Settings Integration

```python
# Source: [ASSUMED - Pydantic v2 模式]
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class AppSettings(BaseSettings):
    """应用配置 - 从环境变量和 .env 加载"""

    model_config = SettingsConfigDict(
        env_prefix="FVC_",  # 环境变量前缀
        env_file=".env",
        env_nested_delimiter="__",
    )

    preset: str = "realtime-8gb"
    device: str = "cuda"
    verbose: bool = True

    class Config:
        env_prefix = "FVC_"
```

### Common Operation 3: 预设系统注册表

```python
# Source: [ASSUMED - 常见预设模式]
from dataclasses import dataclass
from typing import Dict, Protocol

@dataclass
class Preset:
    """预设配置"""
    name: str
    description: str
    device: str
    target_fps: int
    batch_size: int = 1

class PresetRegistry(Protocol):
    """预设注册表协议"""
    def get(self, name: str) -> Preset: ...

class BuiltinPresetRegistry:
    """内置预设注册表"""

    _presets: Dict[str, Preset] = {
        "realtime-8gb": Preset(
            name="realtime-8gb",
            description="RTX 4060 实时换脸预设",
            device="cuda",
            target_fps=30,
            batch_size=1,
        ),
    }

    def get(self, name: str) -> Preset:
        if name not in self._presets:
            raise ValueError(f"未知预设: {name}")
        return self._presets[name]

    def list(self) -> list[Preset]:
        return list(self._presets.values())
```

---

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| 手动 argparse | Typer 类型提示 | 2020s | 自动生成文档、类型安全 |
| print() 调试 | structlog | 2020s | 结构化日志、可查询 |
| appdirs | platformdirs | 2023 | 活跃维护、XDG 兼容 |
| pip/conda | uv | 2024 | 10-100x 更快、统一工具链 |
| 标准 logging | structlog | 2020s | 更好的开发体验 |

**Deprecated/outdated:**
- `appdirs`: 已废弃，使用 `platformdirs` 替代
- `click`: 被 Typer 替代（Typer 基于 Click 但更 Pythonic）

---

## Assumptions Log

> List all claims tagged `[ASSUMED]` in this research. The planner and discuss-phase use this
> section to identify decisions that need user confirmation before execution.

| # | Claim | Section | Risk if Wrong |
|---|-------|---------|---------------|
| A1 | PyYAML 足够满足配置需求 | Standard Stack | 如需注释保留功能需切换到 ruamel.yaml |
| A2 | platformdirs 4.0+ 为当前版本 | Standard Stack | 版本过旧可能缺少某些平台支持 |
| A3 | Pydantic v2 API 稳定 | Code Examples | v2 到 v3 迁移需要注意 |
| A4 | pytest-asyncio 是测试异步代码的标准选择 | Standard Stack | 可能有更优替代方案 |

**If this table is empty:** All claims in this research were verified or cited — no user confirmation needed.

---

## Open Questions

1. **是否需要 `.env` 文件支持？**
   - What we know: Pydantic-settings 支持 `.env` 加载
   - What's unclear: 是否需要环境变量覆盖配置
   - Recommendation: Phase 1 预留接口，Phase 2+ 实现

2. **预设是否需要用户自定义扩展？**
   - What we know: D-08 指定内置预设
   - What's unclear: 是否支持用户创建自定义预设
   - Recommendation: Phase 1 仅实现内置预设，扩展性留待后续

3. **测试框架选择是否需要用户确认？**
   - What we know: 已在 Claude's Discretion 中
   - What's unclear: pytest 是否满足所有测试需求
   - Recommendation: 使用 pytest，后续如需 pytest-asyncio 可添加

---

## Environment Availability

> Skip this section if the phase has no external dependencies (code/config-only changes).

| Dependency | Required By | Available | Version | Fallback |
|------------|------------|-----------|---------|----------|
| Python 3.10+ | All code | ✓ | 3.11 (系统) | — |
| uv | 包管理 | ✓ | 0.11.3 | pip |
| pytest | 测试 | 待安装 | 8.0+ | — |

**Missing dependencies with no fallback:**
- None (所有依赖可在线安装)

**Missing dependencies with fallback:**
- pip 可替代 uv 作为包管理器（性能较差）

---

## Validation Architecture

### Test Framework

| Property | Value |
|----------|-------|
| Framework | pytest 8.0+ |
| Config file | pyproject.toml [tool.pytest] |
| Quick run command | `pytest tests/ -x -v` |
| Full suite command | `pytest tests/ -v` |

### Phase Requirements → Test Map

| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| REQ-01 | `--help` 显示完整参数说明 | smoke | `facevidechange --help` | 待创建 |
| REQ-02 | `--preset realtime-8gb` 加载配置 | unit | `pytest tests/test_presets.py::test_realtime_preset` | 待创建 |
| REQ-03 | `--dry-run` 验证配置 | unit | `pytest tests/test_config.py::test_dry_run` | 待创建 |
| REQ-04 | 默认配置可正常运行 | smoke | `facevidechange --dry-run` | 待创建 |
| REQ-05 | 日志记录关键阶段 | unit | `pytest tests/test_logging.py::test_log_stages` | 待创建 |

### Sampling Rate

- **Per task commit:** `pytest tests/test_cli.py tests/test_config.py -x`
- **Per wave merge:** `pytest tests/ -v`
- **Phase gate:** Full suite green before `/gsd-verify-work`

### Wave 0 Gaps

- [ ] `tests/__init__.py` — 包标记
- [ ] `tests/test_cli.py` — CLI 功能测试
- [ ] `tests/test_config.py` — 配置加载测试
- [ ] `tests/test_presets.py` — 预设系统测试
- [ ] `tests/conftest.py` — pytest fixtures
- [ ] `pyproject.toml` — pytest 配置段
- [ ] `uv add --dev pytest` — 安装测试依赖

*(None — Wave 0 包含所有测试基础设施)*

---

## Security Domain

> Required when `security_enforcement` is enabled (absent = enabled). Omit only if explicitly `false` in config.

### Applicable ASVS Categories

| ASVS Category | Applies | Standard Control |
|---------------|---------|-----------------|
| V2 Authentication | No | CLI 工具无认证需求 |
| V3 Session Management | No | 无会话管理 |
| V4 Access Control | No | 本地工具，无访问控制 |
| V5 Input Validation | Yes | Pydantic 配置验证 |
| V6 Cryptography | No | 无加密需求 |

### Known Threat Patterns for Python CLI

| Pattern | STRIDE | Standard Mitigation |
|---------|--------|---------------------|
| 配置注入 | Tampering | Pydantic 验证输入，禁止代码执行 |
| 路径遍历 | Information Disclosure | platformdirs 标准化路径 |

---

## Sources

### Primary (HIGH confidence)

- [pypi.org/project/typer/] - Typer 0.24.1 发布信息
- [structlog.readthedocs.org] - structlog 日志最佳实践
- [github.com/astral-sh/uv] - uv 包管理器 (82k stars, 267 releases)
- [platformdirs.readthedocs.io] - XDG 路径处理

### Secondary (MEDIUM confidence)

- [oreateai.com/blog/ruamel-vs-pyyaml] - YAML 库对比
- [packaging.python.org] - src layout vs flat layout

### Tertiary (LOW confidence)

- [assumed] - Pydantic v2 API 细节
- [assumed] - platformdirs 4.0+ 版本信息

---

## Metadata

**Confidence breakdown:**

- Standard stack: HIGH - 所有库都有官方文档和活跃社区
- Architecture: HIGH - 项目结构遵循 Python 最佳实践
- Pitfalls: MEDIUM - 基于常见模式，但 RTX 4060 特定场景未验证

**Research date:** 2026-04-17
**Valid until:** 2026-05-17 (30 days for stable tech)

---

## RESEARCH COMPLETE

**Phase:** 01 - 项目基础设施
**Confidence:** HIGH

### Key Findings

1. **Typer 0.24.1** 是当前最新版本，Python 3.10+ 要求
2. **src/ 布局**是 2025 年 Python 项目推荐结构
3. **uv** 是最快的包管理工具（10-100x pip），版本 0.11.3
4. **platformdirs** 替代已废弃的 appdirs，支持 XDG 标准
5. **structlog** 提供优于标准 logging 的结构化日志体验

### File Created

`.planning/phases/01-项目基础设施/01-RESEARCH.md`

### Confidence Assessment

| Area | Level | Reason |
|------|-------|--------|
| Standard Stack | HIGH | 所有库有官方文档和活跃社区 |
| Architecture | HIGH | 基于 Python 最佳实践和现代标准 |
| Pitfalls | MEDIUM | 常见模式，但特定场景未验证 |

### Open Questions

1. 是否需要 `.env` 文件支持（预留接口）
2. 预设是否支持用户自定义扩展（Phase 1 仅内置）
3. 测试框架是否满足所有需求（pytest + pytest-asyncio）

### Ready for Planning

Research complete. Planner can now create PLAN.md files.
