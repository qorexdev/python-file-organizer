"""Watchdog observer for auto-organizing new files."""

import time
from pathlib import Path
from typing import Optional

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileCreatedEvent

from .core import organize_directory
from . import logger


class FileOrganizerHandler(FileSystemEventHandler):
    """Handle new file creation events by organizing them."""

    def __init__(
        self,
        directory: str,
        verbose: bool = False,
        config_path: Optional[str] = None,
    ) -> None:
        super().__init__()
        self.directory = directory
        self.verbose = verbose
        self.config_path = config_path

    def on_created(self, event: FileCreatedEvent) -> None:  # type: ignore[override]
        if event.is_directory:
            return

        file_path = Path(event.src_path)

        # Skip hidden files and files in subdirectories
        if file_path.name.startswith("."):
            return
        if file_path.parent != Path(self.directory).resolve():
            return

        logger.info(f"New file detected: {file_path.name}")

        # Small delay to ensure file is fully written
        time.sleep(0.5)

        organize_directory(
            self.directory,
            dry_run=False,
            verbose=self.verbose,
            config_path=self.config_path,
        )


def watch_directory(
    directory: str,
    verbose: bool = False,
    config_path: Optional[str] = None,
) -> None:
    """Start watching a directory for new files and auto-organize them."""
    path = Path(directory).resolve()
    if not path.is_dir():
        logger.error(f"Directory not found: {directory}")
        return

    handler = FileOrganizerHandler(
        directory=str(path),
        verbose=verbose,
        config_path=config_path,
    )
    observer = Observer()
    observer.schedule(handler, str(path), recursive=False)
    observer.start()

    logger.success(f"Watching directory: {path}")
    logger.info("Press Ctrl+C to stop.")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        logger.info("Stopped watching.")

    observer.join()
