"""Main organizer logic: scan directory, categorize files, move them."""

import shutil
from pathlib import Path
from typing import Dict, List, Optional

from .categories import get_extension_map
from .config import load_config
from .undo import save_undo_log
from . import logger


def organize_directory(
    directory: str,
    dry_run: bool = False,
    verbose: bool = False,
    config_path: Optional[str] = None,
) -> int:
    """Organize files in the given directory by type.

    Returns the number of files moved.
    """
    path = Path(directory).resolve()
    if not path.is_dir():
        logger.error(f"Directory not found: {directory}")
        return 0

    categories = load_config(config_path)
    ext_map = get_extension_map(categories)

    files = [f for f in path.iterdir() if f.is_file() and not f.name.startswith(".")]
    if not files:
        logger.info("No files to organize.")
        return 0

    moves: List[Dict[str, str]] = []
    moved_count = 0

    # Group files by category
    categorized: Dict[str, List[Path]] = {}
    uncategorized: List[Path] = []

    for file in files:
        ext = file.suffix.lower()
        category = ext_map.get(ext)
        if category:
            categorized.setdefault(category, []).append(file)
        else:
            uncategorized.append(file)

    # Move files into category folders
    for category, cat_files in sorted(categorized.items()):
        dest_dir = path / category
        if not dry_run:
            dest_dir.mkdir(exist_ok=True)

        if verbose or dry_run:
            logger.info(f"{category}: {len(cat_files)} file(s)")

        for file in cat_files:
            dest_file = dest_dir / file.name
            # Handle name conflicts
            dest_file = _resolve_conflict(dest_file)

            logger.file_move(file.name, str(dest_file.relative_to(path)), dry=dry_run)

            if not dry_run:
                shutil.move(str(file), str(dest_file))
                moves.append({"from": str(file), "to": str(dest_file)})

            moved_count += 1

    if uncategorized and verbose:
        logger.warning(f"Skipped {len(uncategorized)} uncategorized file(s):")
        for f in uncategorized:
            logger.info(f"  {f.name} ({f.suffix})")

    # Save undo log
    if not dry_run and moves:
        save_undo_log(directory, moves)
        logger.success("Undo log saved. Run with --undo to revert.")

    return moved_count


def _resolve_conflict(dest: Path) -> Path:
    """If a file already exists at dest, add a numeric suffix."""
    if not dest.exists():
        return dest

    stem = dest.stem
    suffix = dest.suffix
    parent = dest.parent
    counter = 1

    while True:
        new_name = f"{stem}_{counter}{suffix}"
        new_dest = parent / new_name
        if not new_dest.exists():
            return new_dest
        counter += 1
