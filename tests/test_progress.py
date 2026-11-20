"""progress.py 单测：章节分组与状态统计。"""

import sys
from pathlib import Path

import yaml

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


def test_chapter_key():
    assert chapter_key("guide/chap1/x.adoc") == "chap1"
    assert chapter_key("guide/top.adoc") == "guide"
    assert chapter_key("toc.yml") == "(top)"


def test_render_totals():
    text = render(_manifest())
    assert "| **合计** |" in text
    assert "0.0%" in text  # 全 missing/skipped/partial → current=0
    for chap in ("chap1", "chap2", "guide", "(top)"):
        assert chap in text


def test_render_pct():
    m = _manifest()
    m["files"][0]["status"] = "current"   # x
    m["files"][2]["status"] = "current"   # z
    text = render(m)
    # translatable = 6 − 1 skipped = 5，current = 2 → 40.0%
    assert "40.0%" in text
