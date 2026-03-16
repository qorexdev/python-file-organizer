"""Undo functionality using a JSON log of file moves."""

import json
import os
import shutil
from pathlib import Path
from typing import Dict, List

from . import logger

UNDO_LOG_FILE = ".organize_undo.json"


def get_undo_log_path(directory: str) -> Path:
    return Path(directory) / UNDO_LOG_FILE


def save_undo_log(directory: str, moves: List[Dict[str, str]]) -> None:
    """Save the list of moves to the undo log file."""
    log_path = get_undo_log_path(directory)
    with open(log_path, "w", encoding="utf-8") as f:
        json.dump({"moves": moves}, f, indent=2, ensure_ascii=False)


def load_undo_log(directory: str) -> List[Dict[str, str]]:
    """Load the undo log from the directory."""
    log_path = get_undo_log_path(directory)
    if not log_path.exists():
        return []
    with open(log_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("moves", [])


def undo_moves(directory: str) -> int:
    """Undo the last organization by moving files back.

    Returns the number of files restored.
    """
    moves = load_undo_log(directory)
    if not moves:
        logger.warning("No undo log found. Nothing to undo.")
        return 0

    restored = 0
    for move in reversed(moves):
        src = move["from"]
        dest = move["to"]
        if os.path.exists(dest):
            dest_dir = os.path.dirname(src)
            os.makedirs(dest_dir, exist_ok=True)
            shutil.move(dest, src)
            logger.file_move(dest, src)
            restored += 1
        else:
            logger.warning(f"File not found, skipping: {dest}")

    # Clean up empty directories created during organization
    _cleanup_empty_dirs(directory)

    # Remove the undo log
    log_path = get_undo_log_path(directory)
    if log_path.exists():
        log_path.unlink()

    return restored


def _cleanup_empty_dirs(directory: str) -> None:
    """Remove empty subdirectories."""
    for dirpath, dirnames, filenames in os.walk(directory, topdown=False):
        if dirpath == directory:
            continue
        if not dirnames and not filenames:
            try:
                os.rmdir(dirpath)
                logger.info(f"Removed empty directory: {dirpath}")
            except OSError:
                pass
