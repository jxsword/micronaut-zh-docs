"""sync_upstream 端到端单测（file:// 注入临时上游仓库）：init/check/apply。"""

import os
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS))

import sync_upstream as su  # noqa: E402
from sync_upstream import (  # noqa: E402
    SyncContext,
    compute_blob_sha,
    sync_init,
    sync_check_or_apply,
)


def _run_git(repo, *args):
    env = dict(os.environ,
               GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@t",
               GIT_COMMITTER_NAME="t", GIT_COMMITTER_EMAIL="t@t")
    result = subprocess.run(["git", *args], cwd=repo, check=True,
                            capture_output=True, env=env)
    return result.stdout.decode("utf-8")


def make_ctx(tmp_path):
    return SyncContext(
        source_dir=tmp_path / "source",
        zh_dir=tmp_path / "zh",
        reports_dir=tmp_path / "reports",
        manifest_file=tmp_path / "manifest.yml",
        workdir=tmp_path / "cache",
        repo_root=tmp_path,
    )


def make_upstream(tmp_path, files, mirror=None):
    """构建 src/main/docs 布局的本地上游仓库（分支 5.2.x）。"""
    repo = tmp_path / "upstream-repo"
    docs = repo / "src" / "main" / "docs"
    docs.mkdir(parents=True)
    for rel, content in files.items():
        p = docs / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")
    for rel, data in (mirror or {}).items():
        p = docs / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(data)
    _run_git(repo, "init", "-b", "5.2.x")
    _run_git(repo, "add", "-A")
    _run_git(repo, "commit", "-m", "init")
    return repo


FILES = {
    "guide/a.adoc": "= A\n\nalpha paragraph\n\nsecond para\n",
    "guide/b.adoc": "= B\n\nbeta paragraph\n",
    "toc.yml": "pages:\n- page: guide/a.adoc\n",
}


def _commit_all(repo, msg):
    _run_git(repo, "add", "-A")
    _run_git(repo, "commit", "-m", msg)


def _baseline(ctx):
    return (ctx.source_dir / "_upstream_commit").read_text(
        encoding="utf-8").strip()


def test_blob_sha_matches_git_hash_object(tmp_path):
    f = tmp_path / "f.txt"
    f.write_bytes(b"hello\n")
    mine = su.compute_blob_sha(f.read_bytes())
    _run_git(tmp_path, "init")
    git_sha = _run_git(tmp_path, "hash-object", "f.txt").strip()
    assert mine == git_sha


def test_init_writes_source_manifest_report(tmp_path):
    repo = make_upstream(tmp_path, FILES,
                         mirror={"resources/img.png": b"\x89PNG"})
    ctx = make_ctx(tmp_path)
    r = sync_init(ctx, "file://" + str(repo), "5.2.x", None, False)
    assert r["has_changes"]
    assert (ctx.source_dir / "_upstream_commit").exists()
    assert (ctx.source_dir / "guide" / "a.adoc").exists()
    assert (ctx.source_dir / "resources" / "img.png").exists()
    m = su.load_manifest(ctx.manifest_file)
    assert m.baseline_commit == _baseline(ctx)
    names = {f["file"] for f in m.files}
    assert names == {"guide/a.adoc", "guide/b.adoc", "toc.yml"}
    assert all(f["status"] == "missing" for f in m.files)
    assert m.entry("guide/a.adoc")["paragraphs"] == 3
    assert len(list(ctx.reports_dir.glob("sync-*.md"))) == 1


def test_init_marks_shell_file_skipped(tmp_path):
    files = dict(FILES)
    files["guide/shell.adoc"] = ("include::guide/a.adoc[]\n"
                                 "include::guide/b.adoc[]\n")
    repo = make_upstream(tmp_path, files)
    ctx = make_ctx(tmp_path)
    sync_init(ctx, "file://" + str(repo), "5.2.x", None, False)
    m = su.load_manifest(ctx.manifest_file)
    assert m.entry("guide/shell.adoc")["status"] == "skipped"
    assert m.entry("guide/a.adoc")["status"] == "missing"


def test_init_rejects_second_init(tmp_path):
    repo = make_upstream(tmp_path, FILES)
    ctx = make_ctx(tmp_path)
    sync_init(ctx, "file://" + str(repo), "5.2.x", None, False)
    with pytest.raises(RuntimeError, match="已存在"):
        sync_init(ctx, "file://" + str(repo), "5.2.x", None, False)


def test_init_dry_run_writes_nothing(tmp_path):
    repo = make_upstream(tmp_path, FILES)
    ctx = make_ctx(tmp_path)
    r = sync_init(ctx, "file://" + str(repo), "5.2.x", None, True)
    assert r["dry_run"] is True
    assert not (tmp_path / "source").exists()
    assert not ctx.manifest_file.exists()


def test_check_no_changes(tmp_path):
    repo = make_upstream(tmp_path, FILES)
    ctx = make_ctx(tmp_path)
    sync_init(ctx, "file://" + str(repo), "5.2.x", None, False)
    r = sync_check_or_apply(ctx, "file://" + str(repo), "5.2.x", None, True,
                            False)
    assert r["has_changes"] is False


def test_check_detects_modification(tmp_path):
    repo = make_upstream(tmp_path, FILES)
    ctx = make_ctx(tmp_path)
    sync_init(ctx, "file://" + str(repo), "5.2.x", None, False)
    (repo / "src/main/docs/guide/a.adoc").write_text(
        "= A\n\nalpha paragraph\n\nCHANGED para\n", encoding="utf-8")
    _commit_all(repo, "edit")
    r = sync_check_or_apply(ctx, "file://" + str(repo), "5.2.x", None, True,
                            False)
    ch = [c for c in r["changes"] if c["file"] == "guide/a.adoc"][0]
    assert ch["type"] == "M"
    assert ch["modified"] >= 1


def test_apply_updates_source_and_manifest(tmp_path, monkeypatch):
    monkeypatch.setenv("MZD_ALLOW_APPLY", "1")
    repo = make_upstream(tmp_path, FILES)
    ctx = make_ctx(tmp_path)
    sync_init(ctx, "file://" + str(repo), "5.2.x", None, False)
    zh = ctx.zh_dir / "guide" / "a.adoc"
    zh.parent.mkdir(parents=True)
    zh.write_text("译文\n", encoding="utf-8")
    (repo / "src/main/docs/guide/a.adoc").write_text(
        "= A\n\nalpha paragraph\n\nCHANGED\n", encoding="utf-8")
    _commit_all(repo, "edit")
    r = sync_check_or_apply(ctx, "file://" + str(repo), "5.2.x", None, False,
                            True)
    assert r["has_changes"] is True
    m = su.load_manifest(ctx.manifest_file)
    assert m.entry("guide/a.adoc")["status"] == "stale"
    assert (ctx.source_dir / "guide" / "a.adoc").read_text(
        encoding="utf-8").endswith("CHANGED\n")
    assert len(list(ctx.reports_dir.glob("sync-*.md"))) == 2


def test_apply_locked_without_tag_or_env(tmp_path, monkeypatch):
    monkeypatch.delenv("MZD_ALLOW_APPLY", raising=False)
    repo = make_upstream(tmp_path, FILES)
    ctx = make_ctx(tmp_path)
    sync_init(ctx, "file://" + str(repo), "5.2.x", None, False)
    (repo / "src/main/docs/guide/a.adoc").write_text("= A\n\nCHANGED\n",
                                                     encoding="utf-8")
    _commit_all(repo, "edit")
    with pytest.raises(RuntimeError, match="门控"):
        sync_check_or_apply(ctx, "file://" + str(repo), "5.2.x", None, False,
                            True)


def test_apply_unlocked_with_v1_tag(tmp_path, monkeypatch):
    monkeypatch.delenv("MZD_ALLOW_APPLY", raising=False)
    real_repo = tmp_path / "proj"
    real_repo.mkdir()
    _run_git(real_repo, "init")
    _run_git(real_repo, "commit", "--allow-empty", "-m", "c")
    _run_git(real_repo, "tag", "v1.0")
    ctx = make_ctx(tmp_path)
    ctx2 = SyncContext(source_dir=ctx.source_dir, zh_dir=ctx.zh_dir,
                       reports_dir=ctx.reports_dir,
                       manifest_file=ctx.manifest_file,
                       workdir=ctx.workdir, repo_root=real_repo)
    assert su.apply_unlocked(ctx2) is True


def test_check_detects_addition_and_deletion(tmp_path):
    files = dict(FILES)
    files["guide/c.adoc"] = "= C\n\ncharlie\n"
    repo = make_upstream(tmp_path, files)
    ctx = make_ctx(tmp_path)
    sync_init(ctx, "file://" + str(repo), "5.2.x", None, False)
    (repo / "src/main/docs/guide/c.adoc").unlink()
    (repo / "src/main/docs/guide/d.adoc").write_text("= D\n\ndelta\n",
                                                     encoding="utf-8")
    _commit_all(repo, "add-del")
    r = sync_check_or_apply(ctx, "file://" + str(repo), "5.2.x", None, True,
                            False)
    types = {c["file"]: c["type"] for c in r["changes"]}
    assert types["guide/c.adoc"] == "D"
    assert types["guide/d.adoc"] == "A"


def test_apply_archives_deleted_file(tmp_path, monkeypatch):
    monkeypatch.setenv("MZD_ALLOW_APPLY", "1")
    files = dict(FILES)
    files["guide/c.adoc"] = "= C\n\ncharlie\n"
    repo = make_upstream(tmp_path, files)
    ctx = make_ctx(tmp_path)
    sync_init(ctx, "file://" + str(repo), "5.2.x", None, False)
    zh = ctx.zh_dir / "guide" / "c.adoc"
    zh.parent.mkdir(parents=True)
    zh.write_text("译文C\n", encoding="utf-8")
    (repo / "src/main/docs/guide/c.adoc").unlink()
    _commit_all(repo, "del")
    sync_check_or_apply(ctx, "file://" + str(repo), "5.2.x", None, False, True)
    m = su.load_manifest(ctx.manifest_file)
    assert m.entry("guide/c.adoc") is None
    archives = list((tmp_path / "archive").rglob("guide/c.adoc"))
    assert len(archives) == 2  # source + zh 两份归档
    assert any("zh" in p.parts for p in archives)


def test_rename_detection_by_blob_sha(tmp_path):
    files = dict(FILES)
    files["guide/c.adoc"] = "= C\n\ncharlie para\n"
    repo = make_upstream(tmp_path, files)
    ctx = make_ctx(tmp_path)
    sync_init(ctx, "file://" + str(repo), "5.2.x", None, False)
    old = repo / "src/main/docs/guide/c.adoc"
    content = old.read_text(encoding="utf-8")
    old.unlink()
    (repo / "src/main/docs/guide/c2.adoc").write_text(content,
                                                      encoding="utf-8")
    _commit_all(repo, "rename")
    r = sync_check_or_apply(ctx, "file://" + str(repo), "5.2.x", None, True,
                            False)
    assert any(c["type"] == "R" for c in r["changes"])


def test_manifest_corrupt_rejected(tmp_path):
    repo = make_upstream(tmp_path, FILES)
    ctx = make_ctx(tmp_path)
    sync_init(ctx, "file://" + str(repo), "5.2.x", None, False)
    ctx.manifest_file.write_text("schema: v9\nfiles: []\n", encoding="utf-8")
    with pytest.raises(RuntimeError, match="损坏"):
        sync_check_or_apply(ctx, "file://" + str(repo), "5.2.x", None, True,
                            False)
