#!/usr/bin/env python3
"""自动生成 reports/progress.md（模块 × 章节状态统计，DR-006 M4 聚合）。

数据唯一来源 = manifest.yml（core）+ manifests/*.yml（模块账本）；
自动生成禁手改（PLAN R2）。进度口径：current /（总文件 − skipped）。

输出：总览表（按模块一行）+ core 分章节表 + 各模块分章节表。
模块章节按剥去 modules/<site>/ 前缀后的相对路径分组。
"""

import sys
import time
from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict, Optional, Tuple

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
MANIFEST_FILE = REPO_ROOT / "manifest.yml"
MANIFESTS_DIR = REPO_ROOT / "manifests"
REPORT = REPO_ROOT / "reports" / "progress.md"


def chapter_key(rel: str, module: Optional[str] = None) -> str:
    """章节键：core 相对 source/；模块先剥 modules/<site>/ 前缀再取段。"""
    if module and rel.startswith(f"modules/{module}/"):
        rel = rel[len(f"modules/{module}/"):]
    parts = rel.split("/")
    if len(parts) >= 3:
        return parts[1]
    if len(parts) == 2:
        return parts[0]
    return "(top)"


def collect_sources() -> list:
    """(module 名, 账本 dict) 列表；core 在前，模块按名排序。"""
    sources = []
    if MANIFEST_FILE.exists():
        sources.append(("core", yaml.safe_load(
            MANIFEST_FILE.read_text(encoding="utf-8"))))
    if MANIFESTS_DIR.is_dir():
        for p in sorted(MANIFESTS_DIR.glob("*.yml")):
            try:
                data = yaml.safe_load(p.read_text(encoding="utf-8"))
            except yaml.YAMLError as e:
                print(f"WARN: 跳过损坏账本 {p.name}: {e}", file=sys.stderr)
                continue
            if isinstance(data, dict) and data.get("files"):
                sources.append((p.stem, data))
    return sources


def render_source(name: str, manifest: dict) -> Tuple[str, Counter]:
    """单账本分章节表；返回 (表格文本, 该账本状态 Counter)。"""
    files = manifest.get("files", [])
    by_chapter: Dict[str, Counter] = defaultdict(Counter)
    for f in files:
        by_chapter[chapter_key(f["file"], name if name != "core" else None)][
            f.get("status", "missing")] += 1
    total = Counter()
    for c in by_chapter.values():
        total.update(c)
    translatable = (total.get("current", 0) + total.get("stale", 0)
                    + total.get("partial", 0) + total.get("missing", 0))
    done = total.get("current", 0)
    pct = f"{done / translatable * 100:.1f}%" if translatable else "—"
    up = manifest.get("upstream") or {}
    ref = manifest.get("ref")
    lines = [f"## {name}", ""]
    meta = f"基线: {up.get('baseline_commit', '')[:12]}，快照 {up.get('snapshot_date', '')}"
    if ref:
        meta += f"，ref {ref}（locked_at {manifest.get('locked_at', '')}）"
    lines += [f"> {meta}", "",
              "| 章节 | 文件数 | missing | stale | partial | current | skipped | 进度 |",
              "|---|---:|---:|---:|---:|---:|---:|---:|"]
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
    return "\n".join(lines), total


def render(sources: list) -> str:
    """聚合报表：总览表（模块维度）+ 各账本分章节表。"""
    lines = [
        "# 翻译进度报表（自动生成，禁手改）",
        "",
        f"> 生成: {time.strftime('%Y-%m-%d %H:%M:%S')} ｜ "
        "数据源: manifest.yml + manifests/*.yml（DR-006 M4 聚合）",
        "",
        "## 总览（按模块）",
        "",
        "| 模块 | 文件数 | missing | stale | partial | current | skipped | 进度 |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    sections = []
    for name, manifest in sources:
        text, total = render_source(name, manifest)
        trans = (total.get("current", 0) + total.get("stale", 0)
                 + total.get("partial", 0) + total.get("missing", 0))
        pct = (f"{total.get('current', 0) / trans * 100:.1f}%"
               if trans else "—")
        lines.append(
            f"| {name} | {sum(total.values())} | {total.get('missing', 0)} "
            f"| {total.get('stale', 0)} | {total.get('partial', 0)} "
            f"| {total.get('current', 0)} | {total.get('skipped', 0)} "
            f"| {pct} |")
        sections.append(text)
    lines += ["", *sections]
    return "\n".join(lines)


def main() -> int:
    sources = collect_sources()
    if not sources:
        print("ERROR: manifest.yml 不存在（先运行 sync --init）", file=sys.stderr)
        return 2
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(render(sources), encoding="utf-8")
    print(f"written: {REPORT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
