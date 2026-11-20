"""validate_translation 七项门禁单测（tmp 目录注入模块常量）。"""

import json
import sys
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS))

import validate_translation as vt  # noqa: E402


PROVENANCE = ("<!-- upstream_file: guide/a.adoc  upstream_commit: {}  "
              "upstream_hash: {}  translated_at: 2026-11-20 -->")


def make_tree(tmp_path, src_text, zh_text, entry_commit="a" * 40,
              blob="b" * 40, with_manifest=True):
    (tmp_path / "source" / "guide").mkdir(parents=True, exist_ok=True)
    (tmp_path / "zh" / "guide").mkdir(parents=True, exist_ok=True)
    (tmp_path / "source" / "guide" / "a.adoc").write_text(src_text,
                                                          encoding="utf-8")
    (tmp_path / "zh" / "guide" / "a.adoc").write_text(zh_text,
                                                      encoding="utf-8")
    if with_manifest:
        (tmp_path / "manifest.yml").write_text(json.dumps({
            "schema": "v1",
            "upstream": {"remote": "x", "baseline_commit": "a" * 40,
                         "snapshot_date": "2026-11-20"},
            "files": [{"file": "guide/a.adoc", "blob_sha": blob,
                       "size": 10, "status": "partial", "zh": "zh/guide/a.adoc",
                       "paragraphs": 2, "updated_at": "2026-11-20",
                       "upstream_commit": entry_commit}],
        }), encoding="utf-8")
    return tmp_path


def patch_vt(monkeypatch, tmp_path, registry=None):
    monkeypatch.setattr(vt, "SOURCE_DIR", tmp_path / "source")
    monkeypatch.setattr(vt, "ZH_DIR", tmp_path / "zh")
    reg = tmp_path / "config" / "anchor-registry.yml"
    reg.parent.mkdir(parents=True, exist_ok=True)
    import yaml
    reg.write_text(yaml.safe_dump({"anchors": registry or []}),
                   encoding="utf-8")
    monkeypatch.setattr(vt, "ANCHOR_REGISTRY", reg)


GOOD_SRC = """= Title One

First paragraph about beans.

----
code line
----

include::guide/part.adoc[]
"""

GOOD_ZH = """> 本文翻译自 Micronaut 官方文档，非官方译文。

""" + PROVENANCE.format("a" * 40, "b" * 40) + """

= 标题一

关于 bean 的第一段。

----
code line
----

include::guide/part.adoc[]
"""


def test_good_file_passes(tmp_path, monkeypatch):
    make_tree(tmp_path, GOOD_SRC, GOOD_ZH)
    patch_vt(monkeypatch, tmp_path)
    errs, warns = vt.validate_file(
        tmp_path / "source/guide/a.adoc", tmp_path / "zh/guide/a.adoc",
        "guide/a.adoc", {}, [], {"blob_sha": "b" * 40,
                                 "upstream_commit": "a" * 40}, "a" * 40)
    assert errs == []
    assert warns == []


def test_check1_placeholder_residue(tmp_path, monkeypatch):
    bad = GOOD_ZH + "\n残留 {{PROTECTED_CODE_0123abcd}}\n"
    make_tree(tmp_path, GOOD_SRC, bad)
    patch_vt(monkeypatch, tmp_path)
    errs, _ = vt.validate_file(
        tmp_path / "source/guide/a.adoc", tmp_path / "zh/guide/a.adoc",
        "guide/a.adoc", {}, [], None, "a" * 40)
    assert any("①" in e for e in errs)


def test_check2_code_block_modified(tmp_path, monkeypatch):
    bad = GOOD_ZH.replace("code line", "code line modified")
    make_tree(tmp_path, GOOD_SRC, bad)
    patch_vt(monkeypatch, tmp_path)
    errs, _ = vt.validate_file(
        tmp_path / "source/guide/a.adoc", tmp_path / "zh/guide/a.adoc",
        "guide/a.adoc", {}, [], None, "a" * 40)
    assert any("②" in e for e in errs)


def test_check2_directive_line_dropped(tmp_path, monkeypatch):
    bad = GOOD_ZH.replace("include::guide/part.adoc[]\n", "")
    make_tree(tmp_path, GOOD_SRC, bad)
    patch_vt(monkeypatch, tmp_path)
    errs, _ = vt.validate_file(
        tmp_path / "source/guide/a.adoc", tmp_path / "zh/guide/a.adoc",
        "guide/a.adoc", {}, [], None, "a" * 40)
    assert any("②" in e for e in errs)


def test_check3_banned_hit(tmp_path, monkeypatch):
    make_tree(tmp_path, GOOD_SRC, GOOD_ZH)
    patch_vt(monkeypatch, tmp_path)
    errs, _ = vt.validate_file(
        tmp_path / "source/guide/a.adoc", tmp_path / "zh/guide/a.adoc",
        "guide/a.adoc", {}, [{"bad": "编译时间", "prefer": "编译期"}],
        None, "a" * 40)
    assert not any("③" in e for e in errs)
    make_tree(tmp_path, GOOD_SRC, GOOD_ZH + "\n这是编译时间的说明。\n")
    errs, _ = vt.validate_file(
        tmp_path / "source/guide/a.adoc", tmp_path / "zh/guide/a.adoc",
        "guide/a.adoc", {}, [{"bad": "编译时间", "prefer": "编译期"}],
        None, "a" * 40)
    assert any("③" in e for e in errs)


def test_check3_required_term_missing(tmp_path, monkeypatch):
    make_tree(tmp_path, GOOD_SRC, GOOD_ZH)
    patch_vt(monkeypatch, tmp_path)
    errs, _ = vt.validate_file(
        tmp_path / "source/guide/a.adoc", tmp_path / "zh/guide/a.adoc",
        "guide/a.adoc", {"beans": "Bean"}, [], None, "a" * 40)
    assert any("③ 必译术语缺失" in e for e in errs)


def test_check4_structure_level_mismatch(tmp_path, monkeypatch):
    bad = GOOD_ZH.replace("= 标题一", "== 标题一")
    make_tree(tmp_path, GOOD_SRC, bad)
    patch_vt(monkeypatch, tmp_path)
    errs, _ = vt.validate_file(
        tmp_path / "source/guide/a.adoc", tmp_path / "zh/guide/a.adoc",
        "guide/a.adoc", {}, [], None, "a" * 40)
    assert any("④" in e for e in errs)


def test_check4_heading_count_mismatch(tmp_path, monkeypatch):
    bad = GOOD_ZH.replace("= 标题一\n", "")
    make_tree(tmp_path, GOOD_SRC, bad)
    patch_vt(monkeypatch, tmp_path)
    errs, _ = vt.validate_file(
        tmp_path / "source/guide/a.adoc", tmp_path / "zh/guide/a.adoc",
        "guide/a.adoc", {}, [], None, "a" * 40)
    assert any("④" in e for e in errs)


def test_check4_heading_not_translated(tmp_path, monkeypatch):
    bad = GOOD_ZH.replace("= 标题一", "= Title One")
    make_tree(tmp_path, 1 if 0 else GOOD_SRC, bad)
    patch_vt(monkeypatch, tmp_path)
    errs, _ = vt.validate_file(
        tmp_path / "source/guide/a.adoc", tmp_path / "zh/guide/a.adoc",
        "guide/a.adoc", {}, [], None, "a" * 40)
    assert any("④ 标题未翻译" in e for e in errs)


def test_check5_anchor_missing_in_translated_target(tmp_path, monkeypatch):
    # 目标文件已译但缺锚点注入 → 报错
    zh_with_xref = GOOD_ZH + "\nxref:guide/b.adoc#sect-one[see]\n"
    make_tree(tmp_path, GOOD_SRC, zh_with_xref)
    (tmp_path / "source" / "guide" / "b.adoc").write_text(
        "[[sect-one]]\n== Section One\n", encoding="utf-8")
    (tmp_path / "zh" / "guide" / "b.adoc").write_text(
        "[[sect-one]]\n== 第一节\n", encoding="utf-8")
    patch_vt(monkeypatch, tmp_path)
    errs, warns = vt.validate_file(
        tmp_path / "source/guide/a.adoc", tmp_path / "zh/guide/a.adoc",
        "guide/a.adoc", {}, [], None, "a" * 40)
    assert not any("⑤" in e for e in errs)
    # 目标已译且锚点缺失 → 报错
    (tmp_path / "zh" / "guide" / "b.adoc").write_text(
        "== 第一节\n", encoding="utf-8")
    errs, _ = vt.validate_file(
        tmp_path / "source/guide/a.adoc", tmp_path / "zh/guide/a.adoc",
        "guide/a.adoc", {}, [], None, "a" * 40)
    assert any("⑤" in e for e in errs)


def test_check5_untranslated_target_exempt(tmp_path, monkeypatch):
    zh_with_xref = GOOD_ZH + "\nxref:guide/untranslated.adoc#x[see]\n"
    make_tree(tmp_path, GOOD_SRC, zh_with_xref)
    (tmp_path / "source" / "guide" / "untranslated.adoc").write_text(
        "[[x]]\n== X\n", encoding="utf-8")
    patch_vt(monkeypatch, tmp_path)
    errs, warns = vt.validate_file(
        tmp_path / "source/guide/a.adoc", tmp_path / "zh/guide/a.adoc",
        "guide/a.adoc", {}, [], None, "a" * 40)
    assert not any("⑤" in e for e in errs)
    assert any("豁免" in w for w in warns)


def test_check5_target_file_missing_in_source(tmp_path, monkeypatch):
    zh_with_xref = GOOD_ZH + "\nxref:guide/ghost.adoc[see]\n"
    make_tree(tmp_path, GOOD_SRC, zh_with_xref)
    patch_vt(monkeypatch, tmp_path)
    errs, _ = vt.validate_file(
        tmp_path / "source/guide/a.adoc", tmp_path / "zh/guide/a.adoc",
        "guide/a.adoc", {}, [], None, "a" * 40)
    assert any("⑤" in e for e in errs)


def test_check5_bare_anchor_resolves_via_registry(tmp_path, monkeypatch):
    # 裸锚点 <<httpServer,Label>> 经登记表解析到文件；目标未译 → 豁免警告
    zh_with_xref = GOOD_ZH + "\nsee <<httpServer,HTTP server>>\n"
    make_tree(tmp_path, GOOD_SRC, zh_with_xref)
    (tmp_path / "source" / "guide" / "httpServer.adoc").write_text(
        "text\n", encoding="utf-8")
    patch_vt(monkeypatch, tmp_path, registry=[
        {"id": "httpServer", "file": "guide/httpServer.adoc"}])
    errs, warns = vt.validate_file(
        tmp_path / "source/guide/a.adoc", tmp_path / "zh/guide/a.adoc",
        "guide/a.adoc", {}, [], None, "a" * 40)
    assert not any("⑤" in e for e in errs)
    assert any("豁免" in w for w in warns)


def test_check5_bare_anchor_unregistered_is_warning(tmp_path, monkeypatch):
    # 未登记裸锚点 → 豁免警告（M3 断链清零跟踪），不算错误
    zh_with_xref = GOOD_ZH + "\nsee <<ghostAnchor,Label>>\n"
    make_tree(tmp_path, GOOD_SRC, zh_with_xref)
    patch_vt(monkeypatch, tmp_path)
    errs, warns = vt.validate_file(
        tmp_path / "source/guide/a.adoc", tmp_path / "zh/guide/a.adoc",
        "guide/a.adoc", {}, [], None, "a" * 40)
    assert not any("⑤" in e for e in errs)
    assert any("裸锚点未登记" in w for w in warns)


def test_check5_bare_anchor_translated_target_needs_injection(
        tmp_path, monkeypatch):
    # 裸锚点解析到已译目标文件：缺注入 → 报错；有注入 → 通过
    zh_with_xref = GOOD_ZH + "\nsee <<upgrading,Upgrading>>\n"
    make_tree(tmp_path, GOOD_SRC, zh_with_xref)
    (tmp_path / "source" / "guide" / "b.adoc").write_text(
        "=== Upgrading between versions\n", encoding="utf-8")
    zh_b = ("> 译文。\n\n" + PROVENANCE.format("a" * 40, "b" * 40) +
            "\n\n[[upgrading]]\n=== 升级\n")
    (tmp_path / "zh" / "guide" / "b.adoc").write_text(zh_b, encoding="utf-8")
    patch_vt(monkeypatch, tmp_path, registry=[
        {"id": "upgrading", "file": "guide/b.adoc"}])
    errs, _ = vt.validate_file(
        tmp_path / "source/guide/a.adoc", tmp_path / "zh/guide/a.adoc",
        "guide/a.adoc", {}, [], None, "a" * 40)
    assert not any("⑤" in e for e in errs)
    (tmp_path / "zh" / "guide" / "b.adoc").write_text(
        zh_b.replace("[[upgrading]]\n", ""), encoding="utf-8")
    errs, _ = vt.validate_file(
        tmp_path / "source/guide/a.adoc", tmp_path / "zh/guide/a.adoc",
        "guide/a.adoc", {}, [], None, "a" * 40)
    assert any("⑤" in e for e in errs)


def test_check5_url_target_skipped(tmp_path, monkeypatch):
    zh_with_url = GOOD_ZH + "\nsee xref:https://example.com/x[go]\n"
    make_tree(tmp_path, GOOD_SRC, zh_with_url)
    patch_vt(monkeypatch, tmp_path)
    errs, warns = vt.validate_file(
        tmp_path / "source/guide/a.adoc", tmp_path / "zh/guide/a.adoc",
        "guide/a.adoc", {}, [], None, "a" * 40)
    assert not any("⑤" in e for e in errs)
    assert not any("⑤" in w for w in warns)


def test_check6_provenance_mismatch(tmp_path, monkeypatch):
    make_tree(tmp_path, GOOD_SRC, GOOD_ZH)
    patch_vt(monkeypatch, tmp_path)
    bad_entry = {"blob_sha": "c" * 40, "upstream_commit": "a" * 40}
    errs, _ = vt.validate_file(
        tmp_path / "source/guide/a.adoc", tmp_path / "zh/guide/a.adoc",
        "guide/a.adoc", {}, [], bad_entry, "a" * 40)
    assert any("⑥" in e for e in errs)
    # 缺注释
    zh_no_comment = GOOD_ZH.split("-->", 1)[1]
    make_tree(tmp_path, GOOD_SRC, zh_no_comment)
    errs, _ = vt.validate_file(
        tmp_path / "source/guide/a.adoc", tmp_path / "zh/guide/a.adoc",
        "guide/a.adoc", {}, [], None, "a" * 40)
    assert any("⑥ 缺溯源注释" in e for e in errs)


def test_check7_spacing_violation(tmp_path, monkeypatch):
    bad = GOOD_ZH.replace("关于 bean 的第一段", "关于bean 的第一段")
    make_tree(tmp_path, GOOD_SRC, bad)
    patch_vt(monkeypatch, tmp_path)
    errs, _ = vt.validate_file(
        tmp_path / "source/guide/a.adoc", tmp_path / "zh/guide/a.adoc",
        "guide/a.adoc", {}, [], None, "a" * 40)
    assert any("⑦ 中英文" in e for e in errs)


def test_check7_halfwidth_punct(tmp_path, monkeypatch):
    bad = GOOD_ZH.replace("关于 bean 的第一段。", "关于 bean 的第一段.")
    make_tree(tmp_path, GOOD_SRC, bad)
    patch_vt(monkeypatch, tmp_path)
    errs, _ = vt.validate_file(
        tmp_path / "source/guide/a.adoc", tmp_path / "zh/guide/a.adoc",
        "guide/a.adoc", {}, [], None, "a" * 40)
    assert any("⑦" in e for e in errs)


def test_check7_traditional_char(tmp_path, monkeypatch):
    zh_bad = GOOD_ZH.replace("关于", "關於")
    make_tree(tmp_path, GOOD_SRC, zh_bad)
    patch_vt(monkeypatch, tmp_path)
    errs, _ = vt.validate_file(
        tmp_path / "source/guide/a.adoc", tmp_path / "zh/guide/a.adoc",
        "guide/a.adoc", {}, [], None, "a" * 40)
    assert any("⑦ 疑似繁体" in e for e in errs)


def test_check7_shared_shape_chars_not_flagged(tmp_path, monkeypatch):
    # 行/息/主/境/景/常 为简繁共用字，简体正文常用，不得误报
    # （B01 实测缺陷回归：执行/信息/主题/环境/背景/正常）
    zh_ok = GOOD_ZH.replace("关于 bean 的第一段。",
                            "正常执行并输出信息，主题背景环境如常。")
    make_tree(tmp_path, GOOD_SRC, zh_ok)
    patch_vt(monkeypatch, tmp_path)
    errs, _ = vt.validate_file(
        tmp_path / "source/guide/a.adoc", tmp_path / "zh/guide/a.adoc",
        "guide/a.adoc", {}, [], None, "a" * 40)
    assert not any("疑似繁体" in e for e in errs)


def test_check7_adjacency(tmp_path, monkeypatch):
    bad = GOOD_ZH.replace("关于 bean 的第一段。", "关于 bean，见`x`（详情）。\n")
    make_tree(tmp_path, GOOD_SRC, bad)
    patch_vt(monkeypatch, tmp_path)
    errs, _ = vt.validate_file(
        tmp_path / "source/guide/a.adoc", tmp_path / "zh/guide/a.adoc",
        "guide/a.adoc", {}, [], None, "a" * 40)
    assert any("⑦" in e for e in errs)
