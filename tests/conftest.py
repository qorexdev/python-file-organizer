import pytest


@pytest.fixture
def sample_dir(tmp_path):
    files = {
        "photo.jpg": b"fake jpg",
        "report.pdf": b"fake pdf",
        "song.mp3": b"fake mp3",
        "script.py": b"print('hi')",
        "archive.zip": b"fake zip",
        "video.mp4": b"fake mp4",
        "readme.txt": b"hello",
        "unknown.xyz": b"mystery",
    }
    for name, content in files.items():
        (tmp_path / name).write_bytes(content)
    return tmp_path


@pytest.fixture
def config_file(tmp_path):
    cfg = tmp_path / "custom_cfg" / "config.yaml"
    cfg.parent.mkdir()
    cfg.write_text(
        "categories:\n"
        "  Custom:\n"
        "    - .xyz\n"
        "    - .abc\n"
        "  Images:\n"
        "    - .webp\n"
    )
    return str(cfg)
