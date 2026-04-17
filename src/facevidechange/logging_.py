from __future__ import annotations
import sys
import logging
from pathlib import Path
from typing import Optional
from rich.console import Console
from rich.logging import RichHandler
from rich.theme import Theme

custom_theme = Theme({
    "info": "cyan",
    "warning": "yellow",
    "error": "bold red",
    "debug": "dim",
})

_console = Console(stderr=True)
_current_level = "INFO"

def setup_logging(
    level: str = "INFO",
    log_file: Optional[Path] = None,
    verbose: bool = True,
) -> None:
    """设置日志系统。"""
    global _current_level
    _current_level = level.upper()
    
    handlers: list[logging.Handler] = []
    
    rich_handler = RichHandler(
        console=_console,
        rich_tracebacks=True,
        tracebacks_show_locals=False,
        show_time=True,
        show_path=False,
        markup=True,
    )
    rich_handler.setFormatter(
        logging.Formatter(
            fmt="%(message)s",
            datefmt="[%X]",
        )
    )
    handlers.append(rich_handler)
    
    if log_file:
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setFormatter(
            logging.Formatter(
                fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )
        )
        handlers.append(file_handler)
    
    logging.basicConfig(
        level=getattr(logging, _current_level),
        format="%(message)s",
        datefmt="[%X]",
        handlers=handlers,
        force=True,
    )
    
    logging.getLogger("PIL").setLevel(logging.WARNING)
    logging.getLogger("matplotlib").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)

def get_logger(name: str) -> logging.Logger:
    """获取带模块名前缀的 logger。"""
    return logging.getLogger(f"facevidechange.{name}")

class LogCapture:
    """上下文管理器，捕获日志输出用于测试。"""
    def __init__(self, logger_name: str = "facevidechange"):
        self.logger_name = logger_name
        self.records: list[logging.LogRecord] = []
        self.handler: Optional[logging.Handler] = None
    
    def __enter__(self):
        self.handler = logging.Handler()
        self.handler.setLevel(logging.DEBUG)
        self.handler.emit = lambda record: self.records.append(record)
        logging.getLogger(self.logger_name).addHandler(self.handler)
        return self
    
    def __exit__(self, *args):
        if self.handler:
            logging.getLogger(self.logger_name).removeHandler(self.handler)

def log_stage(stage: str, message: str, level: str = "INFO") -> None:
    """记录启动/预热/运行时阶段日志。"""
    logger = get_logger(stage)
    getattr(logger, level.lower())(message)
