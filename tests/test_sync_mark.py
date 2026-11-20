"""sync_upstream 单测第二部分：--mark-current 与 --collect-commits。"""

import sys
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS))

import sync_upstream as su  # noqa: E402
from sync_upstream import SyncContext, mark_current, sync_init  # noqa: E402

from test_sync import FILES, _run_git, make_ctx, make_upstream  # noqa: E402


def _baseline(ctx):
    return (ctx.source_dir / "_upstream_commit").read_text(
        encoding="utf-8").strip()


def _init(tmp_path, files=None):
    repo = make_upstream(tmp_path, files or FILES)
    ctx = make_ctx(tmp_path)
    sync_init(ctx, "file://" + str(repo), "5.2.x", None, False)
    return repo, ctx


def _write_zh(ctx, rel, *, upstream_hash=None, commit=None):
    commit = commit or _baseline(ctx)
    if upstream_hash is None:
        upstream_hash = su.load_manifest(ctx.manifest_file).entry(
            rel)["blob_sha"]
    zh = ctx.zh_dir / rel
    zh.parent.mkdir(parents=True, exist_ok=True)
    zh.write_text(
        "> 译文引用块\n\n"
        f"<!-- upstream_file: {rel}  upstream_commit: {commit}  "
        f"upstream_hash: {upstream_hash}  translated_at: 2026-11-20 -->\n\n"
        "译文正文\n", encoding="utf-8")


def test_mark_current_success(tmp_path):
    _, ctx = _init(tmp_path)
    _write_zh(ctx, "guide/a.adoc")
    r = mark_current(ctx, "guide/a.adoc")
    assert r["status"] == "current"
    m = su.load_manifest(ctx.manifest_file)
    assert m.entry("guide/a.adoc")["status"] == "current"


def test_mark_current_rejects_wrong_hash(tmp_path):
    _, ctx = _init(tmp_path)
    _write_zh(ctx, "guide/a.adoc", upstream_hash="0" * 40)
    with pytest.raises(RuntimeError, match="不一致"):
        mark_current(ctx, "guide/a.adoc")


def test_mark_current_rejects_wrong_commit(tmp_path):
    _, ctx = _init(tmp_path)
    _write_zh(ctx, "guide/a.adoc", commit="1" * 40)
    with pytest.raises(RuntimeError, match="不一致"):
        mark_current(ctx, "guide/a.adoc")


def test_mark_current_rejects_missing_provenance(tmp_path):
    _, ctx = _init(tmp_path)
    zh = ctx.zh_dir / "guide" / "a.adoc"
    zh.parent.mkdir(parents=True, exist_ok=True)
    zh.write_text("纯译文，无溯源注释\n", encoding="utf-8")
    with pytest.raises(RuntimeError, match="缺溯源注释"):
        mark_current(ctx, "guide/a.adoc")


def test_mark_current_rejects_missing_zh(tmp_path):
    _, ctx = _init(tmp_path)
    with pytest.raises(RuntimeError, match="译文不存在"):
        mark_current(ctx, "guide/a.adoc")


def test_mark_current_uses_perfile_commit_when_present(tmp_path):
    _, ctx = _init(tmp_path)
    m = su.load_manifest(ctx.manifest_file)
    e = m.entry("guide/a.adoc")
    e["upstream_commit"] = "a" * 40
    su.save_manifest(ctx.manifest_file, m)
    # baseline 是 tag commit；注释写 per-file commit → 应通过
    _write_zh(ctx, "guide/a.adoc", commit="a" * 40)
    mark_current(ctx, "guide/a.adoc")
    m2 = su.load_manifest(ctx.manifest_file)
    assert m2.entry("guide/a.adoc")["status"] == "current"


def test_collect_commits_with_mocked_gh(tmp_path, monkeypatch):
    _, ctx = _init(tmp_path)
    calls = []

    def fake_gh(slug, path, ref):
        calls.append(path)
        return "a" * 40

    monkeypatch.setattr(su, "_gh_api_last_commit", fake_gh)
    r = su.collect_commits(ctx, "5.2.x", None)
    assert r["collected"] == 3
    assert len(calls) == 3
    m = su.load_manifest(ctx.manifest_file)
    assert all(e.get("upstream_commit") == "a" * 40 for e in m.files)


def test_collect_commits_failure_deferred(tmp_path, monkeypatch):
    _, ctx = _init(tmp_path)

    def fake_gh(slug, path, ref):
        return None

    monkeypatch.setattr(su, "_gh_api_last_commit", fake_gh)
    r = su.collect_commits(ctx, "5.2.x", None)
    assert r["failed_deferred"] == 3
    m = su.load_manifest(ctx.manifest_file)
    assert all(not e.get("upstream_commit") for e in m.files)


def test_collect_commits_skips_already_collected(tmp_path, monkeypatch):
    _, ctx = _init(tmp_path)
    calls = []

    def fake_gh(slug, path, ref):
        calls.append(path)
        return "b" * 40

    monkeypatch.setattr(su, "_gh_api_last_commit", fake_gh)
    su.collect_commits(ctx, "5.2.x", None)
    assert len(calls) == 3
    r = su.collect_commits(ctx, "5.2.x", None)
    assert r["already"] == 3
    assert r["collected"] == 0
    assert len(calls) == 3  # 缓存/账本命中，不再调用 API


def test_collect_commits_cache_reused_after_refill(tmp_path, monkeypatch):
    """账本为空但缓存有值 → 直接从缓存取，不调 API。"""
    _, ctx = _init(tmp_path)
    cache_file = ctx.workdir.parent / "commit-cache.json"
    cache_file.parent.mkdir(parents=True, exist_ok=True)
    m = su.load_manifest(ctx.manifest_file)
    cache = {f"{e['file']}:{e['blob_sha']}": "c" * 40 for e in m.files}
    cache_file.write_text(__import__("json").dumps(cache), encoding="utf-8")
    calls = []

    def fake_gh(slug, path, ref):
        calls.append(path)
        return "d" * 40

    monkeypatch.setattr(su, "_gh_api_last_commit", fake_gh)
    r = su.collect_commits(ctx, "5.2.x", None)
    assert r["collected"] == 3
    assert calls == []
