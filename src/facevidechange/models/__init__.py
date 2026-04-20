"""Face detection, embedding, and swapping models."""

from facevidechange.models.download import (
    ModelInfo,
    MODEL_REGISTRY,
    download_model,
    download_all_models,
    calculate_sha256,
    get_model_path,
    model_exists,
)

from facevidechange.models.loader import load_model, get_input_info

from facevidechange.models.benchmark import (
    BenchmarkResult,
    VRAMMonitor,
    benchmark_inference,
    benchmark_with_vram,
    measure_warmup_time,
    generate_benchmark_report,
)

from facevidechange.models.optimizer import (
    OptimizationResult,
    optimize_model,
    batch_optimize,
    compare_speed,
    save_optimization_report,
)

__all__ = [
    # download
    "ModelInfo",
    "MODEL_REGISTRY",
    "download_model",
    "download_all_models",
    "calculate_sha256",
    "get_model_path",
    "model_exists",
    # loader
    "load_model",
    "get_input_info",
    # benchmark
    "BenchmarkResult",
    "VRAMMonitor",
    "benchmark_inference",
    "benchmark_with_vram",
    "measure_warmup_time",
    "generate_benchmark_report",
    # optimizer
    "OptimizationResult",
    "optimize_model",
    "batch_optimize",
    "compare_speed",
    "save_optimization_report",
]
