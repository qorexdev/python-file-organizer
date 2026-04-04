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
    recursive: bool = False,
) -> int:

    path = Path(directory).resolve()
    if not path.is_dir():
        logger.error(f"Directory not found: {directory}")
        return 0

    categories = load_config(config_path)
    ext_map = get_extension_map(categories)

    all_moves: List[Dict[str, str]] = []
    total = 0

    dirs_to_process = [path]
    if recursive:
        for p in path.rglob("*"):
            if p.is_dir() and not p.name.startswith("."):
                # skip dirs that match a category name so we don't re-sort already sorted stuff
                if p.name not in categories:
                    dirs_to_process.append(p)

    for target in dirs_to_process:
        moved, moves = _organize_single_dir(
            target, path, ext_map, categories, dry_run, verbose,
        )
        total += moved
        all_moves.extend(moves)

    if not dry_run and all_moves:
        save_undo_log(directory, all_moves)
        logger.success("Undo log saved. Run with --undo to revert.")

    return total


def _organize_single_dir(
    target: Path,
    root: Path,
    ext_map: Dict[str, str],
    categories: Dict[str, List[str]],
    dry_run: bool,
    verbose: bool,
) -> tuple[int, List[Dict[str, str]]]:

    files = [f for f in target.iterdir() if f.is_file() and not f.name.startswith(".")]
    if not files:
        return 0, []

    moves: List[Dict[str, str]] = []
    count = 0

    categorized: Dict[str, List[Path]] = {}
    uncategorized: List[Path] = []

    for file in files:
        ext = file.suffix.lower()
        cat = ext_map.get(ext)
        if cat:
            categorized.setdefault(cat, []).append(file)
        else:
            uncategorized.append(file)

    for cat, cat_files in sorted(categorized.items()):
        dest_dir = target / cat
        if not dry_run:
            dest_dir.mkdir(exist_ok=True)

        if verbose or dry_run:
            prefix = f"{target.relative_to(root)}/" if target != root else ""
            logger.info(f"{prefix}{cat}: {len(cat_files)} file(s)")

        for file in cat_files:
            dest_file = _resolve_conflict(dest_dir / file.name)
            logger.file_move(file.name, str(dest_file.relative_to(root)), dry=dry_run)

            if not dry_run:
                shutil.move(str(file), str(dest_file))
                moves.append({"from": str(file), "to": str(dest_file)})

            count += 1

    if uncategorized and verbose:
        logger.warning(f"Skipped {len(uncategorized)} uncategorized file(s):")
        for f in uncategorized:
            logger.info(f"  {f.name} ({f.suffix})")

    return count, moves

def _resolve_conflict(dest: Path) -> Path:

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
