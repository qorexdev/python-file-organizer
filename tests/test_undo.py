from organizer.core import organize_directory
from organizer.undo import undo_moves, save_undo_log, load_undo_log


class TestUndo:
    def test_undo_restores_files(self, sample_dir):
        organize_directory(str(sample_dir))
        assert (sample_dir / "Images" / "photo.jpg").exists()

        restored = undo_moves(str(sample_dir))
        assert restored > 0
        assert (sample_dir / "photo.jpg").exists()
        assert not (sample_dir / ".organize_undo.json").exists()

    def test_undo_removes_empty_dirs(self, sample_dir):
        organize_directory(str(sample_dir))
        assert (sample_dir / "Images").is_dir()

        undo_moves(str(sample_dir))
        assert not (sample_dir / "Images").exists()

    def test_undo_no_log_returns_zero(self, tmp_path):
        assert undo_moves(str(tmp_path)) == 0


class TestUndoLog:
    def test_save_and_load(self, tmp_path):
        moves = [{"from": "/a/b.txt", "to": "/a/Docs/b.txt"}]
        save_undo_log(str(tmp_path), moves)
        loaded = load_undo_log(str(tmp_path))
        assert loaded == moves

    def test_load_missing_returns_empty(self, tmp_path):
        assert load_undo_log(str(tmp_path)) == []
