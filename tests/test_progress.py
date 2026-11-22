"""progress.py 单测：章节分组与状态统计（M4 起多账本聚合，DR-006）。"""

import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS))

from progress import chapter_key, render  # noqa: E402


def _manifest():
    return {
        "upstream": {"baseline_commit": "a" * 40},
        "files": [
            {"file": "guide/chap1/x.adoc", "status": "missing"},
            {"file": "guide/chap1/y.adoc", "status": "skipped"},
            {"file": "guide/chap2/z.adoc", "status": "current"},
            {"file": "guide/chap2/w.adoc", "status": "stale"},
            {"file": "guide/top.adoc", "status": "partial"},
            {"file": "toc.yml", "status": "missing"},
        ],
    }


def _module_manifest():
    return {
        "upstream": {"baseline_commit": "b" * 40},
        "ref": "5.2.x",
        "locked_at": "2026-11-23",
        "files": [
            {"file": "modules/micrometer/guide/intro.adoc", "status": "missing"},
            {"file": "modules/micrometer/guide/rx/counter.adoc",
             "status": "current"},
            {"file": "modules/micrometer/toc.yml", "status": "missing"},
        ],
    }


def test_chapter_key():
    assert chapter_key("guide/chap1/x.adoc") == "chap1"
    assert chapter_key("guide/top.adoc") == "guide"
    assert chapter_key("toc.yml") == "(top)"


def test_chapter_key_module_prefix_stripped():
    # 模块文件剥 modules/<site>/ 前缀后再取章节段
    assert chapter_key("modules/micrometer/guide/rx/counter.adoc",
                       "micrometer") == "rx"
    assert chapter_key("modules/micrometer/guide/intro.adoc",
                       "micrometer") == "guide"
    assert chapter_key("modules/micrometer/toc.yml", "micrometer") == "(top)"
    # 不剥前缀时 module=None 保持原路径语义（防御：防串模块）
    assert chapter_key("modules/micrometer/guide/intro.adoc") == "micrometer"


def test_render_core_totals():
    text = render([("core", _manifest())])
    assert "| **合计** |" in text
    assert "0.0%" in text  # 全 missing/skipped/partial → current=0
    for chap in ("chap1", "chap2", "guide", "(top)"):
        assert chap in text


def test_render_aggregates_modules():
    text = render([("core", _manifest()), ("micrometer", _module_manifest())])
    # 总览表含模块行
    assert "| micrometer | 3 |" in text
    assert "| core | 6 |" in text
    # 模块独立分节 + ref/locked_at 元信息
    assert "## micrometer" in text
    assert "ref 5.2.x" in text
    assert "locked_at 2026-11-23" in text
    # 模块章节按剥前缀分组（rx 而非完整路径）
    assert "| rx |" in text


def test_render_module_pct():
    text = render([("micrometer", _module_manifest())])
    # translatable = 3 − 0 skipped = 3，current = 1 → 33.3%
    assert "33.3%" in text
