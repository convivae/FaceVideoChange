from __future__ import annotations
import os
import copy
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Optional, Any

from ruamel.yaml import YAML

# XDG Base Directory Specification
def _xdg_path(env_var: str, default: Path) -> Path:
    """Get XDG-compliant path."""
    if path := os.environ.get(env_var):
        return Path(path) / "facevidechange"
    return Path.home() / default

CONFIG_DIR = _xdg_path("XDG_CONFIG_HOME", ".config/facevidechange")
DATA_DIR = _xdg_path("XDG_DATA_HOME", ".local/share/facevidechange")
CACHE_DIR = _xdg_path("XDG_CACHE_HOME", ".cache/facevidechange")
CONFIG_FILE = CONFIG_DIR / "config.yaml"

yaml = YAML()

@dataclass
class ModelConfig:
    """Model configuration."""
    fps: int = 30
    resolution: list[int] = field(default_factory=lambda: [1280, 720])
    model: str = "inswapper_128_fp16"
    quality: int = 75
    face_swap_strength: float = 0.85

@dataclass
class StreamConfig:
    """RTMP streaming configuration."""
    enable: bool = True
    codec: str = "h264"
    bitrate: str = "2500k"

@dataclass
class RecordConfig:
    """Local recording configuration."""
    enable: bool = False

@dataclass
class FaceVideoChangeConfig:
    """Main configuration."""
    version: str = "1.0"
    models_dir: Path = field(default_factory=lambda: DATA_DIR / "models")
    cache_dir: Path = field(default_factory=lambda: CACHE_DIR)
    log_level: str = "INFO"
    log_file: Optional[Path] = None
    log_verbose: bool = True
    preset_name: Optional[str] = None
    model: ModelConfig = field(default_factory=ModelConfig)
    stream: StreamConfig = field(default_factory=StreamConfig)
    record: RecordConfig = field(default_factory=RecordConfig)
    source: Optional[str] = field(default=None, repr=False)
    face: Optional[str] = field(default=None, repr=False)
    output: Optional[str] = field(default=None, repr=False)
    rtmp_url: Optional[str] = field(default=None, repr=False)
    dry_run: bool = False

    def load_presets(self, preset_name: str) -> None:
        """Load preset from config/presets.yaml."""
        import facevidechange
        preset_file = Path(facevidechange.__file__).parent.parent / "config" / "presets.yaml"
        if not preset_file.exists():
            preset_file = Path(__file__).parent.parent.parent / "config" / "presets.yaml"
        if preset_file.exists():
            with open(preset_file) as f:
                data = yaml.load(f)
            presets = data.get("presets", {})
            if preset_name in presets:
                p = presets[preset_name]
                for key, value in p.items():
                    if not hasattr(self, key):
                        continue
                    sub = getattr(self, key)
                    # If existing field is a dataclass instance, only update nested fields from dict values
                    if hasattr(sub, "__dataclass_fields__"):
                        if isinstance(value, dict):
                            for sk, sv in value.items():
                                if hasattr(sub, sk):
                                    setattr(sub, sk, sv)
                        # Don't replace dataclass instances with non-dict values
                        continue
                    # For non-dataclass fields, set directly only if value is not a dict
                    if not isinstance(value, dict):
                        setattr(self, key, value)

    def merge_user_config(self, user_config: dict) -> None:
        """Merge user config file (~/.config/facevidechange/config.yaml)."""
        for key, value in user_config.get("facevidechange", {}).items():
            if hasattr(self, key):
                if isinstance(value, dict):
                    sub = getattr(self, key)
                    if hasattr(sub, "__dataclass_fields__"):
                        for sk, sv in value.items():
                            if hasattr(sub, sk):
                                setattr(sub, sk, sv)
                else:
                    setattr(self, key, value)

def load_config(
    preset: Optional[str] = None,
    source: Optional[str] = None,
    face: Optional[str] = None,
    dry_run: bool = False,
    log_level: Optional[str] = None,
    **overrides,
) -> FaceVideoChangeConfig:
    """
    加载配置，优先级: CLI参数 > 环境变量 > 预设 > 默认值
    
    Per D-10: CLI args > env vars > presets > defaults
    """
    config = FaceVideoChangeConfig()
    
    if preset:
        config.load_presets(preset)
        config.preset_name = preset
    
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE) as f:
            user_data = yaml.load(f)
        if user_data:
            config.merge_user_config(user_data)
    
    if source is not None:
        config.source = source
    if face is not None:
        config.face = face
    if dry_run:
        config.dry_run = True
    if log_level is not None:
        config.log_level = log_level.upper()
    
    for key, value in overrides.items():
        if hasattr(config, key):
            setattr(config, key, value)
    
    return config

def ensure_dirs() -> None:
    """Ensure all required directories exist."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
