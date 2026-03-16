"""Load and save YAML config with custom rules."""

from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml

from .categories import DEFAULT_CATEGORIES

DEFAULT_CONFIG_NAME = "config.yaml"


def load_config(config_path: Optional[str] = None) -> Dict[str, List[str]]:
    """Load categories from a YAML config file.

    Falls back to DEFAULT_CATEGORIES if no config is found.
    """
    if config_path is None:
        return DEFAULT_CATEGORIES.copy()

    path = Path(config_path)
    if not path.exists():
        return DEFAULT_CATEGORIES.copy()

    with open(path, "r", encoding="utf-8") as f:
        data: Dict[str, Any] = yaml.safe_load(f) or {}

    categories = DEFAULT_CATEGORIES.copy()

    custom: Dict[str, List[str]] = data.get("categories", {})
    if custom:
        for folder, extensions in custom.items():
            normalized = [ext if ext.startswith(".") else f".{ext}" for ext in extensions]
            if folder in categories:
                existing = set(categories[folder])
                existing.update(normalized)
                categories[folder] = sorted(existing)
            else:
                categories[folder] = normalized

    return categories


def save_example_config(output_path: str) -> None:
    """Save the default config as an example YAML file."""
    data = {
        "categories": {
            folder: extensions
            for folder, extensions in DEFAULT_CATEGORIES.items()
        }
    }
    with open(output_path, "w", encoding="utf-8") as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=False)
