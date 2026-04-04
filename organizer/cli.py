import click

from . import __version__
from .core import organize_directory
from .undo import undo_moves
from .watcher import watch_directory
from . import logger

@click.command()
@click.argument("path", default=".", type=click.Path(exists=True))
@click.option("--dry-run", "-d", is_flag=True, help="Preview changes without moving files.")
@click.option("--verbose", "-v", is_flag=True, help="Show detailed output.")
@click.option("--watch", "-w", is_flag=True, help="Watch directory and auto-organize new files.")
@click.option("--undo", "-u", is_flag=True, help="Undo the last organization.")
@click.option("--recursive", "-r", is_flag=True, help="Organize files in subdirectories too.")
@click.option("--config", "-c", type=click.Path(), default=None, help="Path to YAML config file.")
@click.version_option(version=__version__, prog_name="organize")
def cli(
    path: str,
    dry_run: bool,
    verbose: bool,
    watch: bool,
    undo: bool,
    recursive: bool,
    config: str | None,
) -> None:

    if undo:
        logger.info(f"Undoing last organization in: {path}")
        restored = undo_moves(path)
        if restored:
            logger.success(f"Restored {restored} file(s).")
        return

    if watch:
        logger.info(f"Starting watch mode for: {path}")
        watch_directory(path, verbose=verbose, config_path=config)
        return

    if dry_run:
        logger.info(f"Dry run for: {path}")
    else:
        logger.info(f"Organizing: {path}")

    count = organize_directory(
        directory=path,
        dry_run=dry_run,
        verbose=verbose,
        config_path=config,
        recursive=recursive,
    )

    if count:
        logger.success(f"{'Would move' if dry_run else 'Moved'} {count} file(s).")
    else:
        logger.info("Nothing to organize.")

def main() -> None:
    cli()

if __name__ == "__main__":
    main()
