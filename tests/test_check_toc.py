# -*- coding: utf-8 -*-
"""check_toc.py 单元测试：tmp 夹具走 正常/漏译/键树错位/缺溯源 四路。"""
import importlib.util
import sys
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location(
    "check_toc", ROOT / "scripts" / "check_toc.py")
check_toc = importlib.util.module_from_spec(spec)
sys.modules["check_toc"] = check_toc
spec.loader.exec_module(check_toc)


def _make(tmp_path, src_yaml, zh_body, commit="a" * 40, sha="b" * 40):
    src = tmp_path / "source" / "guide"
    zh = tmp_path / "zh" / "guide"
    src.mkdir(parents=True)
    zh.mkdir(parents=True)
    (src / "toc.yml").write_text(src_yaml, encoding="utf-8")
    zh_text = ("# > 本文翻译自（测试夹具）\n"
               f"# <!-- upstream_file: guide/toc.yml  upstream_commit: {commit}  "
               f"upstream_hash: {sha}  translated_at: 2026-11-21 -->\n\n" + zh_body)
    (zh / "toc.yml").write_text(zh_text, encoding="utf-8")
    return src / "toc.yml", zh / "toc.yml"


def _entry(tmp_path, sha="b" * 40, commit="a" * 40):
    return {"guide/toc.yml": {"blob_sha": sha, "upstream_commit": commit}}


def test_ok(tmp_path, monkeypatch):
    src_yaml = "introduction:\n  title: Introduction\n  whatsNew: What's New\n"
    zh_body = ("introduction:\n  title: 介绍\n  whatsNew: 5.0.x 的新特性\n")
    src, _ = _make(tmp_path, src_yaml, zh_body)
    monkeypatch.setattr(check_toc, "SOURCE_DIR", tmp_path / "source")
    monkeypatch.setattr(check_toc, "ZH_DIR", tmp_path / "zh")
    problems, n = check_toc.check_file("guide/toc.yml", _entry(tmp_path))
    assert problems == [] and n == 2


def test_missing_translation(tmp_path, monkeypatch):
    src_yaml = "introduction:\n  title: Introduction\n"
    zh_body = "introduction:\n  title: Introduction\n"
    _make(tmp_path, src_yaml, zh_body)
    monkeypatch.setattr(check_toc, "SOURCE_DIR", tmp_path / "source")
    monkeypatch.setattr(check_toc, "ZH_DIR", tmp_path / "zh")
    problems, n = check_toc.check_file("guide/toc.yml", _entry(tmp_path))
    assert n == 1
    assert any("未译" in p or "漏译" in p or "白名单" in p for p in problems)


def test_key_tree_mismatch(tmp_path, monkeypatch):
    src_yaml = "introduction:\n  title: Introduction\n  whatsNew: What's New\n"
    zh_body = "introduction:\n  title: 介绍\n"
    _make(tmp_path, src_yaml, zh_body)
    monkeypatch.setattr(check_toc, "SOURCE_DIR", tmp_path / "source")
    monkeypatch.setattr(check_toc, "ZH_DIR", tmp_path / "zh")
    problems, _ = check_toc.check_file("guide/toc.yml", _entry(tmp_path))
    assert any("键树" in p for p in problems)


def test_bad_provenance(tmp_path, monkeypatch):
    src_yaml = "introduction:\n  title: Introduction\n"
    zh_body = "introduction:\n  title: 介绍\n"
    src, zh = _make(tmp_path, src_yaml, zh_body, sha="c" * 40)
    monkeypatch.setattr(check_toc, "SOURCE_DIR", tmp_path / "source")
    monkeypatch.setattr(check_toc, "ZH_DIR", tmp_path / "zh")
    problems, _ = check_toc.check_file("guide/toc.yml", _entry(tmp_path, sha="b" * 40))
    assert any("upstream_hash" in p for p in problems)


def test_comment_lost(tmp_path, monkeypatch):
    src_yaml = "introduction:\n  # old: Old Title\n  title: Introduction\n"
    zh_body = "introduction:\n  title: 介绍\n"
    _make(tmp_path, src_yaml, zh_body)
    monkeypatch.setattr(check_toc, "SOURCE_DIR", tmp_path / "source")
    monkeypatch.setattr(check_toc, "ZH_DIR", tmp_path / "zh")
    problems, _ = check_toc.check_file("guide/toc.yml", _entry(tmp_path))
    assert any("注释行丢失" in p for p in problems)
