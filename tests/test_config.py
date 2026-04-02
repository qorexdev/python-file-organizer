from organizer.config import load_config, save_example_config
from organizer.categories import DEFAULT_CATEGORIES


class TestLoadConfig:
    def test_default_when_no_path(self):
        cats = load_config(None)
        assert cats == DEFAULT_CATEGORIES
        assert "Images" in cats

    def test_default_when_file_missing(self, tmp_path):
        cats = load_config(str(tmp_path / "nope.yaml"))
        assert cats == DEFAULT_CATEGORIES

    def test_custom_adds_new_category(self, config_file):
        cats = load_config(config_file)
        assert "Custom" in cats
        assert ".xyz" in cats["Custom"]

    def test_custom_merges_existing(self, config_file):
        cats = load_config(config_file)
        assert ".webp" in cats["Images"]
        assert ".jpg" in cats["Images"]

    def test_normalizes_dot_prefix(self, tmp_path):
        cfg = tmp_path / "cfg.yaml"
        cfg.write_text("categories:\n  Test:\n    - txt\n    - .md\n")
        cats = load_config(str(cfg))
        assert ".txt" in cats["Test"]
        assert ".md" in cats["Test"]


class TestSaveExampleConfig:
    def test_creates_valid_yaml(self, tmp_path):
        out = tmp_path / "example.yaml"
        save_example_config(str(out))
        assert out.exists()
        cats = load_config(str(out))
        assert set(cats.keys()) == set(DEFAULT_CATEGORIES.keys())
        for k in DEFAULT_CATEGORIES:
            assert set(cats[k]) == set(DEFAULT_CATEGORIES[k])
