"""FaceVideoChange — Real-time video stream face swapping CLI tool."""
__version__ = "0.1.0"

from facevidechange.config import (
    load_config,
    FaceVideoChangeConfig,
    ensure_dirs,
    CONFIG_DIR,
    DATA_DIR,
    CACHE_DIR,
    CONFIG_FILE,
)
