"""validate_translation 模块回归（DR-006 M4.0）：--manifest、⑤ 模块前缀、
③ glossary 模块作用域（通用 + 当前模块术语，core 不含模块术语）。"""

import json
import sys
from pathlib import Path

import pytest
import yaml

SCRIPTS = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS))

import validate_translation as vt  # noqa: E402
from validate_translation import (  # noqa: E402
    glossary_for,
    load_module_glossary,
    module_prefix_of,
    validate_file,
)


PROVENANCE = ("<!-- upstream_file: modules/micrometer/guide/intro.adoc  "
              "upstream_commit: {commit}  upstream_hash: {blob}  "
              "translated_at: 2026-11-23 -->")


def make_module_tree(tmp_path, site="micrometer"):
    src = tmp_path / "source" / "modules" / site / "guide"
    zh = tmp_path / "zh" / "modules" / site / "guide"
    src.mkdir(parents=True, exist_ok=True)
    zh.mkdir(parents=True, exist_ok=True)
    rel = f"modules/{site}/guide/intro.adoc"
    src_text = "= Intro\n\nMicrometer instruments paragraph.\n"
    zh_text = ("> 本文翻译自 Micronaut Micrometer 官方文档，非官方译文。\n\n"
               + PROVENANCE.format(commit="a" * 40, blob="b" * 40) + "\n\n"
               "= 简介\n\nMicrometer 指标段落。\n")
    (src / "intro.adoc").write_text(src_text, encoding="utf-8")
    (zh / "intro.adoc").write_text(zh_text, encoding="utf-8")
    # manifest manifests/<site>.yml
    manifests = tmp_path / "manifests"
    manifests.mkdir(exist_ok=True)
    (manifests / f"{site}.yml").write_text(yaml.safe_dump({
        "schema": "v1",
        "upstream": {"remote": "x", "baseline_commit": "a" * 40,
                     "snapshot_date": "2026-11-23"},
        "ref": "5.2.x",
        "locked_at": "2026-11-23",
        "files": [{"file": rel, "blob_sha": "b" * 40, "size": 10,
                   "status": "current", "zh": f"zh/{rel}",
                   "paragraphs": 1, "updated_at": "2026-11-23",
                   "upstream_commit": "a" * 40}],
    }, allow_unicode=True), encoding="utf-8")
    return tmp_path


def patch_vt(monkeypatch, tmp_path):
    monkeypatch.setattr(vt, "SOURCE_DIR", tmp_path / "source")
    monkeypatch.setattr(vt, "ZH_DIR", tmp_path / "zh")
    reg = tmp_path / "config" / "anchor-registry.yml"
    reg.parent.mkdir(parents=True, exist_ok=True)
    reg.write_text(yaml.safe_dump({"anchors": []}), encoding="utf-8")
    monkeypatch.setattr(vt, "ANCHOR_REGISTRY", reg)


def test_module_prefix_of():
    assert module_prefix_of("modules/micrometer/guide/intro.adoc") == \
        "modules/micrometer"
    assert module_prefix_of("guide/aop.adoc") == ""
    assert module_prefix_of("modules/x.adoc") == ""  # 深度不足，非模块文件


def test_load_module_glossary_scoped(tmp_path, monkeypatch):
    gloss = {
        "modules": {"terms": [
            {"en": "meter registry", "zh": "MeterRegistry",
             "module": "micrometer"},
            {"en": "constraint", "zh": "约束", "module": "validation"},
            {"en": "bad entry", "zh": "无 module 字段"},
        ]},
    }
    fpath = tmp_path / "glossary.yml"
    fpath.write_text(yaml.safe_dump(gloss, allow_unicode=True),
                     encoding="utf-8")
    monkeypatch.setattr(vt, "GLOSSARY_FILE", fpath)
    mic = load_module_glossary("micrometer")
    assert mic == {"meter registry": "MeterRegistry"}
    assert load_module_glossary("validation") == {"constraint": "约束"}
    assert load_module_glossary(None) == {}
    assert load_module_glossary("core") == {}
    monkeypatch.setattr(vt, "GLOSSARY_FILE", tmp_path / "no-such.yml")
    assert load_module_glossary("micrometer") == {}


def test_glossary_for_core_and_module(tmp_path, monkeypatch):
    base = {"beans": "Bean"}
    monkeypatch.setattr(vt, "GLOSSARY_FILE", tmp_path / "no-glossary.yml")
    # core 文件：仅通用集
    assert glossary_for("guide/aop.adoc", base) == base
    # 模块文件：通用 + 模块术语

    def fake_load(site):
        return {"meter registry": "MeterRegistry"} if site == "micrometer" else {}

    monkeypatch.setattr(vt, "load_module_glossary", fake_load)
    merged = glossary_for("modules/micrometer/guide/intro.adoc", base)
    assert merged == {"beans": "Bean",
                      "meter registry": "MeterRegistry"}


def test_validate_module_file_passes(tmp_path, monkeypatch):
    tmp_path = make_module_tree(tmp_path)
    patch_vt(monkeypatch, tmp_path)
    rel = "modules/micrometer/guide/intro.adoc"
    errs, warns = validate_file(
        tmp_path / "source" / rel, tmp_path / "zh" / rel, rel,
        {}, [], {"blob_sha": "b" * 40, "upstream_commit": "a" * 40}, "a" * 40)
    assert errs == []
    assert warns == []


def test_validate_module_xref_resolves_within_module(tmp_path, monkeypatch):
    """模块内 xref:guide/other.adoc → 按模块文档树前缀解析（不误报 core 缺文件）。"""
    tmp_path = make_module_tree(tmp_path)
    src = tmp_path / "source/modules/micrometer/guide"
    zh = tmp_path / "zh/modules/micrometer/guide"
    (src / "other.adoc").write_text("[[sect]]\n== Other\n", encoding="utf-8")
    (zh / "other.adoc").write_text("[[sect]]\n== 其他\n", encoding="utf-8")
    zhi = zh / "intro.adoc"
    zhi.write_text(zhi.read_text(encoding="utf-8")
                   + "\nxref:guide/other.adoc#sect[see]\n", encoding="utf-8")
    patch_vt(monkeypatch, tmp_path)
    rel = "modules/micrometer/guide/intro.adoc"
    errs, warns = validate_file(
        tmp_path / "source" / rel, tmp_path / "zh" / rel, rel,
        {}, [], {"blob_sha": "b" * 40, "upstream_commit": "a" * 40}, "a" * 40)
    assert not any("⑤" in e for e in errs)
    assert not any("⑤" in w for w in warns)


def test_validate_module_xref_untranslated_target_exempt(tmp_path, monkeypatch):
    tmp_path = make_module_tree(tmp_path)
    (tmp_path / "source/modules/micrometer/guide/ghost.adoc").write_text(
        "[[g]]\n== Ghost\n", encoding="utf-8")
    zhi = tmp_path / "zh/modules/micrometer/guide/intro.adoc"
    zhi.write_text(zhi.read_text(encoding="utf-8")
                   + "\nxref:guide/ghost.adoc#g[see]\n", encoding="utf-8")
    patch_vt(monkeypatch, tmp_path)
    rel = "modules/micrometer/guide/intro.adoc"
    errs, warns = validate_file(
        tmp_path / "source" / rel, tmp_path / "zh" / rel, rel,
        {}, [], {"blob_sha": "b" * 40, "upstream_commit": "a" * 40}, "a" * 40)
    assert not any("⑤" in e for e in errs)
    assert any("豁免" in w for w in warns)


def test_validate_main_with_module_manifest(tmp_path, monkeypatch, capsys):
    """端到端：--manifest manifests/<site>.yml + --file 模块路径 → PASSED。"""
    tmp_path = make_module_tree(tmp_path)
    patch_vt(monkeypatch, tmp_path)
    rc = vt.main(["--manifest", str(tmp_path / "manifests" / "micrometer.yml"),
                  "--file", "modules/micrometer/guide/intro.adoc"])
    assert rc == 0
    out = capsys.readouterr().out
    assert "PASSED" in out


def test_validate_main_module_manifest_missing(tmp_path, monkeypatch):
    patch_vt(monkeypatch, tmp_path)
    rc = vt.main(["--manifest", str(tmp_path / "manifests" / "ghost.yml")])
    assert rc == 2
