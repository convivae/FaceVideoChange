---
phase: 02
slug: 模型验证与优化
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-04-21
---

# Phase 02 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest 7.x |
| **Config file** | tests/conftest.py — shared fixtures |
| **Quick run command** | `pytest tests/test_benchmark.py -v --tb=short` |
| **Full suite command** | `pytest tests/ -v --tb=short -k "not slow"` |
| **Estimated runtime** | ~60 seconds (models mocked) |

---

## Sampling Rate

- **After every task commit:** Run `pytest tests/test_benchmark.py -v --tb=short`
- **After every plan wave:** Run `pytest tests/ -v --tb=short -k "not slow"`
- **Before `/gsd-verify-work`:** Full suite must be green
- **Max feedback latency:** 30 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| 02-01-01 | 01 | 1 | CORE-01 | T-02-01 | N/A | unit | `pytest tests/test_benchmark.py::test_inswapper_onnx_loads -v` | ✅ W0 | ⬜ pending |
| 02-02-01 | 02 | 1 | CORE-02 | — | N/A | unit | `pytest tests/test_benchmark.py::test_scrfd_loads -v` | ✅ W0 | ⬜ pending |
| 02-03-01 | 03 | 1 | CORE-03 | — | N/A | unit | `pytest tests/test_benchmark.py::test_arcface_loads -v` | ✅ W0 | ⬜ pending |
| 02-04-01 | 04 | 1 | CORE-01,02,03 | — | N/A | unit | `pytest tests/test_benchmark.py::test_benchmark_fps -v` | ⬜ W1 | ⬜ pending |
| 02-04-02 | 04 | 1 | CORE-01,02,03 | — | N/A | unit | `pytest tests/test_benchmark.py::test_vram_usage -v` | ⬜ W1 | ⬜ pending |
| 02-05-01 | 05 | 1 | CORE-01,02,03 | — | N/A | unit | `pytest tests/test_benchmark.py::test_onnxslim_optimization -v` | ⬜ W1 | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `tests/test_benchmark.py` — benchmark tests for FPS, VRAM, warmup
- [ ] `tests/conftest.py` — shared fixtures for model paths, mock configs
- [ ] `pytest` install — if not detected

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Actual FPS on RTX 4060 | SC-01: 30+ FPS | Requires real GPU | Run `facevidechange benchmark --gpu` on RTX 4060 machine |
| Actual VRAM peak < 4GB | SC-02: VRAM < 4GB | Requires real GPU | Monitor nvidia-smi during benchmark |
| Model warmup < 3s | SC-04: Warmup < 3s | Requires real GPU | Check benchmark output warmup time |
| Model consistency | SC-03: Same input → same output | Requires real models | Compare SHA256 of outputs |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 30s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending

---

## Success Criteria Mapping

| Criterion | Validation Method | Pass Threshold |
|-----------|-------------------|----------------|
| SC-01: 30+ FPS | timeit-based FPS counter | ≥30 FPS |
| SC-02: VRAM < 4GB | pynvml peak tracking | <4096 MB |
| SC-03: Model consistency | SHA256 hash comparison | Deterministic |
| SC-04: Warmup < 3s | Cold-start timing | <3 seconds |
| SC-05: Size -20%, Speed +10% | onnxslim comparison | Verified |
