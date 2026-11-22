"""sync_upstream 模块模式回归（DR-006 M4.0）：--manifest manifests/<site>.yml
→ dest_prefix=modules/<site>，账本顶层 ref/locked_at，core 缺省行为不变。"""

import sys
from pathlib import Path

import pytest
import yaml

SCRIPTS = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS))

import sync_upstream as su  # noqa: E402
from sync_upstream import SyncContext, mark_current  # noqa: E402

from test_sync import FILES, _run_git, make_upstream  # noqa: E402


def make_module_ctx(tmp_path, site="micrometer"):
    """模块账本路径 manifests/<site>.yml；快照落 source/modules/<site>/。"""
    manifests = tmp_path / "manifests"
    manifests.mkdir(exist_ok=True)
    return SyncContext(
        source_dir=tmp_path / "source",
        zh_dir=tmp_path / "zh",
        reports_dir=tmp_path / "reports",
        manifest_file=manifests / f"{site}.yml",
        workdir=tmp_path / "cache",
        repo_root=tmp_path,
        doc_root="src/main/docs",
        dest_prefix=f"modules/{site}",
    )


MODULE_FILES = {
    "guide/intro.adoc": "= Intro\n\nmicrometer paragraph one\n\npara two\n",
    "guide/rx.adoc": "= Rx\n\nobservability paragraph\n",
    "toc.yml": "pages:\n- page: guide/intro.adoc\n",
}


def test_init_module_writes_prefixed_source_manifest(tmp_path):
    repo = make_upstream(tmp_path, MODULE_FILES,
                         mirror={"resources/img/m.png": b"\x89PNG"})
    ctx = make_module_ctx(tmp_path)
    r = su.sync_init(ctx, "file://" + str(repo), "5.2.x", None, False)
    assert r["has_changes"]
    # 快照落盘带 modules/<site>/ 前缀
    assert (ctx.source_dir / "modules/micrometer/guide/intro.adoc").exists()
    assert (ctx.source_dir / "modules/micrometer/toc.yml").exists()
    assert (ctx.source_dir / "modules/micrometer/resources/img/m.png").exists()
    assert (ctx.source_dir / "modules/micrometer/_upstream_commit").exists()
    # core 的 source/ 根不受影响
    assert not (ctx.source_dir / "guide").exists()
    # 账本字段写全相对路径，顶层记 ref + locked_at
    m = su.load_manifest(ctx.manifest_file)
    names = {f["file"] for f in m.files}
    assert names == {"modules/micrometer/guide/intro.adoc",
                     "modules/micrometer/guide/rx.adoc",
                     "modules/micrometer/toc.yml"}
    assert all(f["zh"].startswith("zh/modules/micrometer/") for f in m.files)
    assert m.ref == "5.2.x"
    assert m.locked_at == m.snapshot_date
    assert m.baseline_commit == (
        ctx.source_dir / "modules/micrometer/_upstream_commit").read_text(
            encoding="utf-8").strip()


def test_core_manifest_schema_unchanged(tmp_path):
    """core 账本（manifest.yml）不写入 ref/locked_at——schema 零漂移。"""
    repo = make_upstream(tmp_path, FILES)
    ctx = SyncContext(
        source_dir=tmp_path / "source", zh_dir=tmp_path / "zh",
        reports_dir=tmp_path / "reports",
        manifest_file=tmp_path / "manifest.yml", workdir=tmp_path / "cache",
        repo_root=tmp_path)
    su.sync_init(ctx, "file://" + str(repo), "5.2.x", None, False)
    data = yaml.safe_load(ctx.manifest_file.read_text(encoding="utf-8"))
    assert "ref" not in data and "locked_at" not in data


def test_check_module_detects_modification(tmp_path):
    repo = make_upstream(tmp_path, MODULE_FILES)
    ctx = make_module_ctx(tmp_path)
    su.sync_init(ctx, "file://" + str(repo), "5.2.x", None, False)
    (repo / "src/main/docs/guide/intro.adoc").write_text(
        "= Intro\n\nmicrometer paragraph one\n\nCHANGED para\n",
        encoding="utf-8")
    _run_git(repo, "add", "-A")
    _run_git(repo, "commit", "-m", "edit")
    r = su.sync_check_or_apply(ctx, "file://" + str(repo), "5.2.x", None,
                               True, False)
    ch = {c["file"]: c for c in r["changes"]}
    assert ch["modules/micrometer/guide/intro.adoc"]["type"] == "M"
    assert ch["modules/micrometer/guide/intro.adoc"]["modified"] >= 1


def test_apply_module_new_and_missing_zh_status(tmp_path, monkeypatch):
    monkeypatch.setenv("MZD_ALLOW_APPLY", "1")
    files = dict(MODULE_FILES)
    files["guide/extra.adoc"] = "= Extra\n\nadded paragraph\n"
    repo = make_upstream(tmp_path, files)
    ctx = make_module_ctx(tmp_path)
    su.sync_init(ctx, "file://" + str(repo), "5.2.x", None, False)
    zh = ctx.zh_dir / "modules/micrometer/guide/intro.adoc"
    zh.parent.mkdir(parents=True)
    zh.write_text("译文\n", encoding="utf-8")
    (repo / "src/main/docs/guide/intro.adoc").write_text(
        "= Intro\n\nCHANGED\n", encoding="utf-8")
    _run_git(repo, "add", "-A")
    _run_git(repo, "commit", "-m", "edit")
    r = su.sync_check_or_apply(ctx, "file://" + str(repo), "5.2.x", None,
                               False, True)
    m = su.load_manifest(ctx.manifest_file)
    assert m.entry("modules/micrometer/guide/intro.adoc")["status"] == "stale"
    assert m.entry("modules/micrometer/guide/extra.adoc")["status"] == "missing"
    assert (ctx.source_dir / "modules/micrometer/guide/extra.adoc").exists()


def test_mark_current_module_uses_module_baseline(tmp_path):
    repo = make_upstream(tmp_path, MODULE_FILES)
    ctx = make_module_ctx(tmp_path)
    su.sync_init(ctx, "file://" + str(repo), "5.2.x", None, False)
    baseline = (ctx.source_dir / "modules/micrometer/_upstream_commit").read_text(
        encoding="utf-8").strip()
    m = su.load_manifest(ctx.manifest_file)
    entry = m.entry("modules/micrometer/guide/intro.adoc")
    zh = ctx.zh_dir / "modules/micrometer/guide/intro.adoc"
    zh.parent.mkdir(parents=True)
    zh.write_text(
        "> 译文\n\n"
        f"<!-- upstream_file: modules/micrometer/guide/intro.adoc  "
        f"upstream_commit: {baseline}  upstream_hash: {entry['blob_sha']}  "
        f"translated_at: 2026-11-23 -->\n\n正文\n", encoding="utf-8")
    r = mark_current(ctx, "modules/micrometer/guide/intro.adoc")
    assert r["status"] == "current"


def test_resolve_manifest_rules(tmp_path):
    from sync_upstream import resolve_manifest

    class A:
        manifest = None
    # 缺省 → core
    path, prefix = resolve_manifest(A)
    assert prefix == ""
    # manifests/<site>.yml → modules/<site>
    A.manifest = tmp_path / "manifests" / "validation.yml"
    path, prefix = resolve_manifest(A)
    assert prefix == "modules/validation" and path.name == "validation.yml"
    # manifest.yml 显式指定 → core
    A.manifest = tmp_path / "manifest.yml"
    _, prefix = resolve_manifest(A)
    assert prefix == ""
    # 非法位置 → 拒绝
    A.manifest = tmp_path / "elsewhere" / "x.yml"
    with pytest.raises(ValueError, match="manifest"):
        resolve_manifest(A)


def test_module_ref_from_manifest_used_as_default(tmp_path, monkeypatch):
    """--ref 缺省且模块账本已记录 ref → 取账本 ref（DR-006 §6 逐模块基线）。"""
    repo = make_upstream(tmp_path, MODULE_FILES)
    ctx = make_module_ctx(tmp_path)
    su.sync_init(ctx, "file://" + str(repo), "5.2.x", None, False)
    assert su.manifest_ref_of(ctx.manifest_file) == "5.2.x"
    # core manifest 无 ref 字段 → None
    core_manifest = tmp_path / "core-manifest.yml"
    core_manifest.write_text("schema: v1\nupstream: {}\nfiles: []\n",
                             encoding="utf-8")
    assert su.manifest_ref_of(core_manifest) is None
