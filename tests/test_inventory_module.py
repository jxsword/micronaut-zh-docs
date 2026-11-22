"""inventory.py 模块回归（DR-006 M4.0）：--manifest 路由、批次编号前缀、
toc 路径参数化；core 缺省行为不变（无测试即打包逻辑与既有产物对齐）。"""

import json
import sys
from pathlib import Path

import pytest
import yaml

SCRIPTS = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS))

import inventory as inv  # noqa: E402
from inventory import (  # noqa: E402
    batch_prefix_of,
    pack_batches,
    resolve_target,
    toc_files,
)


def test_resolve_target_rules(tmp_path):
    assert resolve_target(None) == (inv.MANIFEST_FILE, "", "core")
    p, prefix, site = resolve_target(str(tmp_path / "manifests" / "validation.yml"))
    assert prefix == "modules/validation" and site == "validation"
    p, prefix, site = resolve_target(str(tmp_path / "manifest.yml"))
    assert prefix == "" and site == "core"
    with pytest.raises(ValueError, match="manifest"):
        resolve_target(str(tmp_path / "elsewhere" / "x.yml"))


def test_batch_prefix_of(tmp_path, monkeypatch):
    # 无 modules.json → site 大写
    monkeypatch.setattr(inv, "MODULES_JSON", tmp_path / "no.json")
    assert batch_prefix_of("micrometer", None) == "MICROMETER"
    # modules.json 提供 batch_prefix
    mj = tmp_path / "modules.json"
    mj.write_text(json.dumps(
        {"modules": {"micrometer": {"batch_prefix": "MICRO"}}}),
        encoding="utf-8")
    monkeypatch.setattr(inv, "MODULES_JSON", mj)
    assert batch_prefix_of("micrometer", None) == "MICRO"
    assert batch_prefix_of("validation", None) == "VALIDATION"
    # CLI 覆盖优先
    assert batch_prefix_of("micrometer", "V") == "V"


def test_toc_files_module_prefix(tmp_path):
    # 伪造 source/modules/micrometer/guide/{intro,rx}.adoc + toc
    g = tmp_path / "source" / "modules" / "micrometer" / "guide"
    g.mkdir(parents=True)
    (g / "intro.adoc").write_text("x\n", encoding="utf-8")
    (g / "rx.adoc").write_text("y\n", encoding="utf-8")
    toc = tmp_path / "toc.yml"
    toc.write_text(yaml.safe_dump({"intro": "Intro", "rx": "Reactive"}),
                   encoding="utf-8")
    monkey_target = tmp_path / "source"
    orig = inv.SOURCE_DIR
    inv.SOURCE_DIR = monkey_target
    try:
        ordered, missing = toc_files(toc, "modules/micrometer")
    finally:
        inv.SOURCE_DIR = orig
    assert ordered == ["modules/micrometer/guide/intro.adoc",
                       "modules/micrometer/guide/rx.adoc"]
    assert missing == []


def test_toc_files_core_prefix(tmp_path):
    g = tmp_path / "source" / "guide"
    g.mkdir(parents=True)
    (g / "aop.adoc").write_text("x\n", encoding="utf-8")
    toc = tmp_path / "toc.yml"
    toc.write_text(yaml.safe_dump({"aop": "AOP"}), encoding="utf-8")
    orig = inv.SOURCE_DIR
    inv.SOURCE_DIR = tmp_path / "source"
    try:
        ordered, missing = toc_files(toc, "")
    finally:
        inv.SOURCE_DIR = orig
    assert ordered == ["guide/aop.adoc"]


def test_pack_batches_dual_metric():
    counts = {
        "a.adoc": {"noncode": 2000, "total": 3000},
        "b.adoc": {"noncode": 2000, "total": 3000},
        "c.adoc": {"noncode": 100, "total": 100},
    }
    batches = pack_batches(["a.adoc", "b.adoc", "c.adoc"], counts, set())
    # a+b 超非代码词上限 → a、b 各自成批，c 与 b …
    assert len(batches) >= 2
    assert batches[0]["files"] == ["a.adoc"]
    assert batches[1]["files"] == ["b.adoc", "c.adoc"]


def test_build_report_module(tmp_path, monkeypatch):
    """模块端到端：伪账本 + 伪 toc + 伪 source → 报告产出 MICRO-01。"""
    src = tmp_path / "source" / "modules" / "micrometer" / "guide"
    src.mkdir(parents=True)
    (src / "intro.adoc").write_text(
        "= Intro\n\nMicrometer counts metrics in application code.\n",
        encoding="utf-8")
    (src / "toc.yml").write_text(yaml.safe_dump({"intro": "Intro"}),
                                 encoding="utf-8")
    manifest = {
        "schema": "v1",
        "upstream": {"remote": "micronaut-projects/micronaut-micrometer",
                     "baseline_commit": "c" * 40, "snapshot_date": "2026-11-23"},
        "ref": "5.2.x",
        "locked_at": "2026-11-23",
        "files": [
            {"file": "modules/micrometer/guide/intro.adoc", "blob_sha": "b" * 8,
             "size": 100, "status": "missing",
             "zh": "zh/modules/micrometer/guide/intro.adoc",
             "paragraphs": 2, "updated_at": "2026-11-23"},
            {"file": "modules/micrometer/guide/toc.yml", "blob_sha": "b" * 8,
             "size": 20, "status": "missing",
             "zh": "zh/modules/micrometer/guide/toc.yml",
             "paragraphs": 1, "updated_at": "2026-11-23"},
        ],
    }
    mj = tmp_path / "modules.json"
    mj.write_text(json.dumps(
        {"modules": {"micrometer": {"batch_prefix": "MICRO"}}}),
        encoding="utf-8")
    monkeypatch.setattr(inv, "SOURCE_DIR", tmp_path / "source")
    monkeypatch.setattr(inv, "MODULES_JSON", mj)
    report = tmp_path / "reports" / "inventory-micrometer.md"
    stats = inv.build_report(manifest, "modules/micrometer", "micrometer",
                             "MICRO", report)
    assert stats["batches"] == 1
    text = report.read_text(encoding="utf-8")
    assert "### MICRO-01" in text
    assert "ref 5.2.x" in text
    assert "locked_at 2026-11-23" in text
