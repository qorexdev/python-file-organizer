from organizer.core import organize_directory, _resolve_conflict
from organizer.categories import get_extension_map


class TestExtensionMap:
    def test_jpg_maps_to_images(self):
        ext_map = get_extension_map()
        assert ext_map[".jpg"] == "Images"

    def test_pdf_maps_to_documents(self):
        ext_map = get_extension_map()
        assert ext_map[".pdf"] == "Documents"

    def test_py_maps_to_code(self):
        ext_map = get_extension_map()
        assert ext_map[".py"] == "Code"

    def test_custom_categories(self):
        cats = {"Stuff": [".foo", ".bar"]}
        ext_map = get_extension_map(cats)
        assert ext_map[".foo"] == "Stuff"
        assert ext_map[".bar"] == "Stuff"
        assert ".jpg" not in ext_map


class TestOrganize:
    def test_moves_files_to_correct_dirs(self, sample_dir):
        count = organize_directory(str(sample_dir))
        assert count == 7  # all except unknown.xyz
        assert (sample_dir / "Images" / "photo.jpg").exists()
        assert (sample_dir / "Documents" / "report.pdf").exists()
        assert (sample_dir / "Music" / "song.mp3").exists()
        assert (sample_dir / "Code" / "script.py").exists()

    def test_dry_run_doesnt_move(self, sample_dir):
        count = organize_directory(str(sample_dir), dry_run=True)
        assert count == 7
        assert (sample_dir / "photo.jpg").exists()
        assert not (sample_dir / "Images").exists()

    def test_uncategorized_stays(self, sample_dir):
        organize_directory(str(sample_dir))
        assert (sample_dir / "unknown.xyz").exists()

    def test_hidden_files_skipped(self, tmp_path):
        (tmp_path / ".hidden.jpg").write_bytes(b"x")
        (tmp_path / "visible.jpg").write_bytes(b"x")
        count = organize_directory(str(tmp_path))
        assert count == 1
        assert (tmp_path / ".hidden.jpg").exists()

    def test_empty_dir_returns_zero(self, tmp_path):
        assert organize_directory(str(tmp_path)) == 0

    def test_nonexistent_dir_returns_zero(self, tmp_path):
        assert organize_directory(str(tmp_path / "nope")) == 0

    def test_with_custom_config(self, sample_dir, config_file):
        count = organize_directory(str(sample_dir), config_path=config_file)
        assert count == 8  # now .xyz maps to Custom
        assert (sample_dir / "Custom" / "unknown.xyz").exists()

    def test_creates_undo_log(self, sample_dir):
        organize_directory(str(sample_dir))
        assert (sample_dir / ".organize_undo.json").exists()

    def test_no_undo_log_on_dry_run(self, sample_dir):
        organize_directory(str(sample_dir), dry_run=True)
        assert not (sample_dir / ".organize_undo.json").exists()


class TestRecursive:
    def test_recursive_organizes_subdirs(self, tmp_path):
        (tmp_path / "photo.jpg").write_bytes(b"x")
        sub = tmp_path / "stuff"
        sub.mkdir()
        (sub / "track.mp3").write_bytes(b"x")
        (sub / "notes.pdf").write_bytes(b"x")

        count = organize_directory(str(tmp_path), recursive=True)
        assert count == 3
        assert (tmp_path / "Images" / "photo.jpg").exists()
        assert (sub / "Music" / "track.mp3").exists()
        assert (sub / "Documents" / "notes.pdf").exists()

    def test_recursive_skips_category_dirs(self, sample_dir):
        organize_directory(str(sample_dir))
        # run again with recursive — shouldn't re-sort files inside category dirs
        count = organize_directory(str(sample_dir), recursive=True)
        assert count == 0

    def test_non_recursive_ignores_subdirs(self, tmp_path):
        sub = tmp_path / "nested"
        sub.mkdir()
        (sub / "pic.png").write_bytes(b"x")
        count = organize_directory(str(tmp_path))
        assert count == 0
        assert (sub / "pic.png").exists()

    def test_recursive_dry_run(self, tmp_path):
        sub = tmp_path / "sub"
        sub.mkdir()
        (sub / "doc.pdf").write_bytes(b"x")
        count = organize_directory(str(tmp_path), recursive=True, dry_run=True)
        assert count == 1
        assert (sub / "doc.pdf").exists()
        assert not (sub / "Documents").exists()


class TestResolveConflict:
    def test_no_conflict(self, tmp_path):
        dest = tmp_path / "file.txt"
        assert _resolve_conflict(dest) == dest

    def test_adds_counter_on_conflict(self, tmp_path):
        (tmp_path / "file.txt").write_text("first")
        dest = tmp_path / "file.txt"
        resolved = _resolve_conflict(dest)
        assert resolved == tmp_path / "file_1.txt"

    def test_increments_counter(self, tmp_path):
        (tmp_path / "file.txt").write_text("first")
        (tmp_path / "file_1.txt").write_text("second")
        resolved = _resolve_conflict(tmp_path / "file.txt")
        assert resolved == tmp_path / "file_2.txt"
