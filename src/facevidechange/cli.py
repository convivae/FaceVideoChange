from __future__ import annotations
import sys
from typing import Optional
import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from facevidechange import load_config, ensure_dirs, FaceVideoChangeConfig
from facevidechange.logging_ import setup_logging

app = typer.Typer(
    name="facevidechange",
    add_completion=False,
    no_args_is_help=True,
    help="FaceVideoChange — Real-time video stream face swapping CLI tool.\n\n用于主播/UP主的实时换脸工具，支持 RTMP 推流和本地录制。",
)
console = Console()

HELP_PANEL = """
[bold cyan]FaceVideoChange[/bold cyan] — Real-time video stream face swapping

[bold yellow]Quick Start:[/bold yellow]
  facevidechange --source webcam --face photo.jpg --preset realtime-8gb

[bold yellow]Examples:[/bold yellow]
  facevidechange --source 0 --face me.jpg --preset realtime-8gb
  facevidechange --source video.mp4 --face target.jpg --output result.mp4
  facevidechange --source webcam --face me.jpg --preset realtime-8gb --dry-run
"""

@app.command()
def main(
    source: str = typer.Option(
        ...,
        "--source",
        "-s",
        help="Source: webcam index (0-9) or video file path",
    ),
    face: str = typer.Option(
        ...,
        "--face",
        "-f",
        help="Target face image path (JPG/PNG)",
    ),
    preset: Optional[str] = typer.Option(
        None,
        "--preset",
        help="Preset name (realtime-8gb, quality-8gb, preview-only)",
    ),
    output: Optional[str] = typer.Option(
        None,
        "--output",
        "-o",
        help="Output file path for local recording",
    ),
    rtmp_url: Optional[str] = typer.Option(
        None,
        "--rtmp",
        help="RTMP URL (e.g., rtmp://live.bilibili.com/live3/xxx)",
    ),
    log_level: str = typer.Option(
        "INFO",
        "--log-level",
        help="Log level: DEBUG, INFO, WARNING, ERROR",
    ),
    dry_run: bool = typer.Option(
        False,
        "--dry-run",
        help="Validate configuration and models without starting processing",
    ),
    version: bool = typer.Option(
        False,
        "--version",
        "-v",
        help="Show version information",
    ),
):
    """FaceVideoChange — Real-time video stream face swapping CLI tool."""
    if version:
        from facevidechange import __version__
        console.print(f"[bold]FaceVideoChange[/bold] v{__version__}")
        raise typer.Exit()

    ensure_dirs()
    setup_logging(log_level)
    import logging
    log = logging.getLogger("facevidechange")

    try:
        config = load_config(
            preset=preset,
            source=source,
            face=face,
            dry_run=dry_run,
            log_level=log_level,
        )
        if output:
            config.record.enable = True
            config.record.output = output
        if rtmp_url:
            config.stream.enable = True
            config.stream.url = rtmp_url
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] Failed to load configuration: {e}")
        raise typer.Exit(1)

    _display_config(config)

    if config.dry_run:
        console.print("\n[bold green]DRY RUN MODE[/bold green] — Configuration validated successfully.")
        console.print("[dim]No processing started (--dry-run).[/dim]")
        raise typer.Exit(0)

    console.print("\n[yellow]Note:[/yellow] Face processing will be implemented in Phase 3.")
    console.print(f"[dim]Source: {config.source}, Face: {config.face}, Preset: {config.preset_name}[/dim]")
    raise typer.Exit(0)

def _display_config(config: FaceVideoChangeConfig) -> None:
    """显示配置摘要表。"""
    table = Table(title="[bold]Configuration Summary[/bold]", show_header=True)
    table.add_column("Setting", style="cyan")
    table.add_column("Value", style="green")
    table.add_row("Preset", config.preset_name or "(none)")
    table.add_row("Source", config.source or "(none)")
    table.add_row("Face", config.face or "(none)")
    table.add_row("FPS", str(config.model.fps))
    table.add_row("Resolution", f"{config.model.resolution[0]}x{config.model.resolution[1]}")
    table.add_row("Model", config.model.model)
    table.add_row("Log Level", config.log_level)
    table.add_row("Stream", "Enabled" if config.stream.enable else "Disabled")
    table.add_row("Record", "Enabled" if config.record.enable else "Disabled")
    console.print(table)

def get_app() -> typer.Typer:
    """Return the Typer app instance."""
    return app

if __name__ == "__main__":
    app()
