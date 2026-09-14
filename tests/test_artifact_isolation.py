"""A reproducibility check must not repair or overwrite the evidence it checks."""
import sys

import check_artifacts as A


def prepare(tmp_path, monkeypatch, body):
    (tmp_path / "main.step").write_text("published")
    (tmp_path / "other.step").write_text("other published part")
    (tmp_path / "builder.py").write_text("from pathlib import Path\n" + body)
    monkeypatch.setattr(A, "ROOT", str(tmp_path))
    monkeypatch.setattr(A, "REGENERATORS", {"main.step": [sys.executable, "builder.py"]})


def test_changed_output_cannot_become_its_own_reference(tmp_path, monkeypatch):
    prepare(tmp_path, monkeypatch, "Path('main.step').write_text('new bytes')\n")
    assert not A._regenerates_identically("main.step")
    assert not A._regenerates_identically("main.step")
    assert (tmp_path / "main.step").read_text() == "published"


def test_unchanged_sentinel_cannot_hide_another_changed_part(tmp_path, monkeypatch):
    prepare(tmp_path, monkeypatch, "Path('other.step').write_text('changed part')\n")
    assert not A._regenerates_identically("main.step")
    assert (tmp_path / "other.step").read_text() == "other published part"


def test_failed_builder_leaves_published_files_intact(tmp_path, monkeypatch):
    prepare(tmp_path, monkeypatch, "Path('main.step').unlink()\nraise SystemExit(1)\n")
    assert not A._regenerates_identically("main.step")
    assert (tmp_path / "main.step").read_text() == "published"


def test_identical_build_passes_without_touching_source(tmp_path, monkeypatch):
    prepare(tmp_path, monkeypatch, "Path('main.step').write_text('published')\n")
    before = (tmp_path / "main.step").stat().st_mtime_ns
    assert A._regenerates_identically("main.step")
    assert (tmp_path / "main.step").stat().st_mtime_ns == before
