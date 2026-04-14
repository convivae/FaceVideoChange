# Phase 1: 项目基础设施 - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-04-14
**Phase:** 01-项目基础设施
**Areas discussed:** CLI框架, 配置文件格式, 预设系统, 日志系统

---

## CLI框架

|| Option | Description | Selected |
|--------|--------|-------------|----------|
| Typer | 现代 Python CLI 框架，基于类型提示，自动生成帮助文档 | ✓ |
| Click | 功能丰富，社区成熟 | |
| argparse | Python 标准库，无需额外依赖 | |

**User's choice:** Typer
**Notes:** 推荐理由 — 现代、类型安全、自动生成 CLI 文档

---

## 配置文件格式

|| Option | Description | Selected |
|--------|--------|-------------|----------|
| YAML | 推荐，人类可读，支持复杂结构 | ✓ (默认推荐) |
| JSON | 标准格式，解析快，但人类可读性一般 | |
| TOML | INI 风格，配置文件友好 | |

**User's choice:** 用户跳过，默认为 YAML（推荐方案）
**Notes:** YAML 配置路径: `~/.facevidechange/config.yaml`

---

## 预设系统

|| Option | Description | Selected |
|--------|--------|-------------|----------|
| 内置预设 | realtime-8gb 等内置，--preset 加载 | ✓ |
| 自定义预设 | 用户可创建/编辑预设文件 | |
| 两者都要 | 内置预设 + 用户自定义 | |

**User's choice:** 内置预设 (builtin)
**Notes:** --preset <name> 加载预设

---

## 日志系统

|| Option | Description | Selected |
|--------|--------|-------------|----------|
| 详细 (verbose) | 启动/预热/运行时全部记录 | ✓ |
| 极简 | 只记录错误 | |
| 可配置 | 用户可选 | |

**User's choice:** 详细 (verbose)
**Notes:** 包含时间戳、模块名、日志级别，输出到 stdout

---

## Claude's Discretion

- 日志格式具体样式（颜色、字体）— 由实现者决定
- 预设文件的具体参数值 — 由后续阶段决定
- 项目目录结构细节 — 由 planner 根据实际需求决定
- 测试框架选择 — 由 planner 决定

---

## Deferred Ideas

- GUI 界面 — Phase 8 之后考虑
- Web 界面 — 暂不考虑
