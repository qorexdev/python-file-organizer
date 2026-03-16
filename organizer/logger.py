"""Rich console logging with colors."""

from rich.console import Console
from rich.theme import Theme

custom_theme = Theme({
    "info": "cyan",
    "success": "bold green",
    "warning": "bold yellow",
    "error": "bold red",
    "dry": "bold magenta",
    "path": "underline blue",
})

console = Console(theme=custom_theme)


def info(message: str) -> None:
    console.print(f"[info]{message}[/info]")


def success(message: str) -> None:
    console.print(f"[success]{message}[/success]")


def warning(message: str) -> None:
    console.print(f"[warning]{message}[/warning]")


def error(message: str) -> None:
    console.print(f"[error]{message}[/error]")


def dry_run(message: str) -> None:
    console.print(f"[dry][DRY-RUN][/dry] {message}")


def file_move(src: str, dest: str, dry: bool = False) -> None:
    if dry:
        dry_run(f"[path]{src}[/path] -> [path]{dest}[/path]")
    else:
        console.print(f"  [path]{src}[/path] -> [path]{dest}[/path]")
