#!/usr/bin/env python3
"""自动生成 reports/progress.md（章节 × 状态统计）。

数据唯一来源 = manifest.yml；自动生成禁手改（PLAN R2）。
进度口径：current /（总文件 − skipped）。
"""

import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
MANIFEST_FILE = REPO_ROOT / "manifest.yml"
REPORT = REPO_ROOT / "reports" / "progress.md"


def chapter_key(rel: str) -> str:
    parts = rel.split("/")
    if len(parts) >= 3:
        return parts[1]
    if len(parts) == 2:
        return parts[0]
    return "(top)"


def render(manifest: dict) -> str:
    files = manifest.get("files", [])
    by_chapter = defaultdict(Counter)
    for f in files:
        by_chapter[chapter_key(f["file"])][f.get("status", "missing")] += 1
    total = Counter()
    for c in by_chapter.values():
        total.update(c)
    translatable = total.get("current", 0) + total.get("stale", 0) \
        + total.get("partial", 0) + total.get("missing", 0)
    done = total.get("current", 0)
    pct = f"{done / translatable * 100:.1f}%" if translatable else "—"
    lines = [
        "# 翻译进度报表（自动生成，禁手改）",
        "",
        f"> 生成: {time.strftime('%Y-%m-%d %H:%M:%S')} ｜ 数据源: manifest.yml ｜ "
        f"基线: {(manifest.get('upstream') or {}).get('baseline_commit', '')[:12]}",
        "",
        "| 章节 | 文件数 | missing | stale | partial | current | skipped | 进度 |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for chap in sorted(by_chapter):
        c = by_chapter[chap]
        n = sum(c.values())
        trans = n - c.get("skipped", 0)
        p = f"{c.get('current', 0) / trans * 100:.0f}%" if trans else "—"
        lines.append(
            f"| {chap} | {n} | {c.get('missing', 0)} | {c.get('stale', 0)} "
            f"| {c.get('partial', 0)} | {c.get('current', 0)} "
            f"| {c.get('skipped', 0)} | {p} |")
    lines += [
        "| **合计** | **{}** | **{}** | **{}** | **{}** | **{}** | **{}** | **{}** |".format(
            sum(total.values()), total.get("missing", 0), total.get("stale", 0),
            total.get("partial", 0), total.get("current", 0),
            total.get("skipped", 0), pct),
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    if not MANIFEST_FILE.exists():
        print("ERROR: manifest.yml 不存在（先运行 sync --init）", file=sys.stderr)
        return 2
    manifest = yaml.safe_load(MANIFEST_FILE.read_text(encoding="utf-8"))
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(render(manifest), encoding="utf-8")
    print(f"written: {REPORT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
