from changelog_maker.core import parse_commit, render


def test_parse_conventional_commit():
    c = parse_commit("abcdef123456789", "feat(api)!: add batch endpoint")
    assert c.sha == "abcdef123456"
    assert (c.type, c.scope, c.breaking, c.subject) == ("feat", "api", True, "add batch endpoint")


def test_parse_plain_commit():
    c = parse_commit("1234567890", "Initial import")
    assert c.type == "other" and c.subject == "Initial import"


def test_render_groups_and_breaking():
    commits = [
        parse_commit("abcdef123456", "feat(cli): add JSON output"),
        parse_commit("123456789abc", "fix!: prevent overwrite"),
        parse_commit("999999999999", "docs: explain usage"),
    ]
    text = render(commits, version="1.2.0", released="2026-09-21")
    assert "## [1.2.0] - 2026-09-21" in text
    assert "### Breaking Changes" in text
    assert "### Added" in text and "**cli:** add JSON output" in text
    assert "### Fixed" in text and "prevent overwrite" in text
    assert "### Documentation" in text


def test_exclude_other_and_links():
    commits = [parse_commit("abcdef123456", "random message"), parse_commit("fedcba654321", "fix: bug")]
    text = render(commits, include_other=False, links=True, repo_url="https://github.com/acme/demo")
    assert "random message" not in text
    assert "https://github.com/acme/demo/commit/fedcba654321" in text


def test_empty_render():
    assert "_No changes._" in render([])
