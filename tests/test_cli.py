from pathlib import Path
from changelog_maker import cli


def test_cli_rejects_non_repo(tmp_path, capsys):
    assert cli.main([str(tmp_path)]) == 2
    assert "not a Git repository" in capsys.readouterr().err


def test_cli_writes_output(monkeypatch, tmp_path):
    (tmp_path / ".git").mkdir()
    monkeypatch.setattr(cli, "git_history", lambda *args: [("abcdef123456", "feat: useful feature")])
    output = tmp_path / "CHANGELOG.md"
    assert cli.main([str(tmp_path), "--version", "1.0.0", "--date", "2026-09-21", "-o", str(output)]) == 0
    assert "### Added" in output.read_text(encoding="utf-8")
    assert cli.main([str(tmp_path), "-o", str(output)]) == 2


def test_max_count_validation(tmp_path):
    assert cli.main([str(tmp_path), "--max-count", "0"]) == 2
