"""Default file categories mapping extensions to folder names."""

from typing import Dict, List

# Extension -> category folder name
DEFAULT_CATEGORIES: Dict[str, List[str]] = {
    "Images": [
        ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp",
        ".ico", ".tiff", ".tif", ".raw", ".heic", ".heif",
    ],
    "Documents": [
        ".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx",
        ".txt", ".rtf", ".odt", ".ods", ".odp", ".csv", ".tex",
    ],
    "Videos": [
        ".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv", ".webm",
        ".m4v", ".mpg", ".mpeg", ".3gp",
    ],
    "Music": [
        ".mp3", ".wav", ".flac", ".aac", ".ogg", ".wma", ".m4a",
        ".opus", ".aiff",
    ],
    "Archives": [
        ".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".xz",
        ".tar.gz", ".tar.bz2", ".tar.xz",
    ],
    "Code": [
        ".py", ".js", ".ts", ".jsx", ".tsx", ".java", ".c", ".cpp",
        ".h", ".hpp", ".cs", ".go", ".rs", ".rb", ".php", ".swift",
        ".kt", ".scala", ".r", ".m", ".sh", ".bash", ".ps1",
        ".html", ".css", ".scss", ".sass", ".less", ".sql",
        ".json", ".xml", ".yaml", ".yml", ".toml", ".ini", ".cfg",
    ],
    "Executables": [
        ".exe", ".msi", ".dmg", ".app", ".deb", ".rpm", ".apk",
    ],
    "Fonts": [
        ".ttf", ".otf", ".woff", ".woff2", ".eot",
    ],
    "3D Models": [
        ".obj", ".stl", ".fbx", ".blend", ".3ds",
    ],
}


def get_extension_map(categories: Dict[str, List[str]] | None = None) -> Dict[str, str]:
    """Build a reverse map: extension -> category folder name."""
    cats = categories or DEFAULT_CATEGORIES
    ext_map: Dict[str, str] = {}
    for folder, extensions in cats.items():
        for ext in extensions:
            ext_map[ext.lower()] = folder
    return ext_map
