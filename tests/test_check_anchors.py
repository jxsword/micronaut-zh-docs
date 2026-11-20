"""check_anchors 单测：锚点定义收集、xref 收集、登记表构建。"""

import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS))

from check_anchors import (  # noqa: E402
    build_registry,
    collect_xrefs,
    scan_file_anchors,
    write_registry,
)


def test_scan_explicit_anchor_with_title_backfill():
    text = "[[configuration]]\n== Configuration\n\ntext\n"
    a = scan_file_anchors(text)
    assert "configuration" in a
    assert a["configuration"]["title"] == "Configuration"
    assert a["configuration"]["explicit"] is True


def test_scan_shorthand_block_id():
    text = "[#options]\n== Options\n"
    a = scan_file_anchors(text)
    assert "options" in a
    assert a["options"]["title"] == "Options"


def test_scan_reftext():
    text = "[[id1,Display Text]]\npara\n"
    a = scan_file_anchors(text)
    assert a["id1"]["reftext"] == "Display Text"


def test_collect_xrefs_both_forms():
    text = ("xref:guide/a.adoc#x[see] and xref::guide/b.adoc[] and "
            "<<#same,here>> and <<guide/c.adoc>>\n")
    targets = collect_xrefs(text)
    assert "guide/a.adoc#x" in targets
    assert "guide/b.adoc" in targets
    assert "#same" in targets
    assert "guide/c.adoc" in targets


def test_registry_resolves_referenced_anchors(tmp_path):
    src = tmp_path / "source"
    (src / "guide").mkdir(parents=True)
    (src / "guide" / "a.adoc").write_text(
        "[[sect-one]]\n== Section One\n\ntext\n", encoding="utf-8")
    (src / "guide" / "b.adoc").write_text(
        "xref:guide/a.adoc#sect-one[go]\n", encoding="utf-8")
    data = build_registry(src)
    assert len(data["anchors"]) == 1
    ent = data["anchors"][0]
    assert ent["id"] == "sect-one"
    assert ent["file"] == "guide/a.adoc"
    assert ent["title"] == "Section One"
    assert ent["referenced_by"] == ["guide/b.adoc"]
    assert data["unresolved"] == []


def test_registry_resolves_http_prefixed_bare_anchor(tmp_path):
    # 裸锚点以 "http" 开头（如 httpServer/httpClient）不是 URL，
    # 不得被 URL 过滤误跳过（B01 实测缺陷回归）
    src = tmp_path / "source"
    (src / "guide").mkdir(parents=True)
    (src / "guide" / "httpServer.adoc").write_text(
        "text\n", encoding="utf-8")
    (src / "guide" / "b.adoc").write_text(
        "see <<httpServer,HTTP server>>\n", encoding="utf-8")
    data = build_registry(src)
    assert len(data["anchors"]) == 1
    ent = data["anchors"][0]
    assert ent["id"] == "httpServer"
    assert ent["file"] == "guide/httpServer.adoc"
    assert data["unresolved"] == []


def test_registry_skips_real_url_targets(tmp_path):
    src = tmp_path / "source"
    (src / "guide").mkdir(parents=True)
    (src / "guide" / "a.adoc").write_text(
        "xref:https://example.com/x[go] and "
        "link:https://micronaut.io[site]\n", encoding="utf-8")
    data = build_registry(src)
    assert data["anchors"] == []
    assert data["unresolved"] == []


def test_registry_unresolved_anchor(tmp_path):
    src = tmp_path / "source"
    (src / "guide").mkdir(parents=True)
    (src / "guide" / "a.adoc").write_text(
        "xref:guide/a.adoc#ghost[go]\n", encoding="utf-8")
    data = build_registry(src)
    assert data["anchors"] == []
    assert len(data["unresolved"]) == 1
    assert data["unresolved"][0]["reason"] == "anchor-missing"


def test_registry_unresolved_file(tmp_path):
    src = tmp_path / "source"
    (src / "guide").mkdir(parents=True)
    (src / "guide" / "a.adoc").write_text(
        "xref:guide/ghost.adoc[go]\n", encoding="utf-8")
    data = build_registry(src)
    assert data["unresolved"][0]["reason"] == "file-missing"


def test_write_registry_yaml(tmp_path):
    import yaml
    src = tmp_path / "source"
    (src / "guide").mkdir(parents=True)
    (src / "guide" / "a.adoc").write_text(
        "[[x1]]\n== Title X\n", encoding="utf-8")
    (src / "guide" / "b.adoc").write_text(
        "xref:guide/a.adoc#x1[go]\n", encoding="utf-8")
    out = tmp_path / "config" / "anchor-registry.yml"
    data = write_registry(src, out)
    assert out.exists()
    loaded = yaml.safe_load(out.read_text(encoding="utf-8"))
    assert loaded["anchors"][0]["id"] == "x1"
    assert data["anchors"][0]["id"] == "x1"
