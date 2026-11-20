#!/usr/bin/env python3
"""zh 落盘装配：还原文本 + 溯源投影（PLAN §5.4）→ zh/<rel>。

输入为 protect/restore 流水线产出的 <stem>-restored.txt；
页头引用块 + HTML 注释四字段的字段值全部取自 manifest.yml
（upstream_commit / blob_sha），禁止手抄哈希。

CLI：
  --file REL [REL ...]   相对 source/ 的文件路径（guide/...）
  --restored-dir DIR     还原文本根目录（默认 workdir/protect/source）
  --translated-at DATE   translated_at 字段（默认当天）
  --baseline-date DATE   引用块中的基线锁定日期（默认取 PLAN §5.4 固定值）

页名取 source/guide/toc.yml 的显示标题（英文原题）；
官方站 URL 锚点 = core-<文件 stem>（官方站实测约定，
锚 id 带 core- 前缀；核实日期 2026-11-20）。

退出码：0 成功 / 2 环境错误（manifest 缺条目、还原文本缺失等）。
"""

import argparse
import datetime
import json
import sys
from pathlib import Path
from typing import Dict, List, Optional

import yaml

REPO_ROOT = Path(__file__).parent.parent.resolve()
SOURCE_DIR = REPO_ROOT / "source"
ZH_DIR = REPO_ROOT / "zh"
MANIFEST_FILE = REPO_ROOT / "manifest.yml"
TOC_FILE = SOURCE_DIR / "guide" / "toc.yml"
BASELINE_LOCK_DATE = "2026-11-19"
OFFICIAL_BASE = "https://docs.micronaut.io/5.2.x/core/"


def toc_title(key_path: str) -> Optional[str]:
    """按 toc 键路径（如 ioc/beans）取显示标题；缺省 None。"""
    if not TOC_FILE.exists():
        return None
    toc = yaml.safe_load(TOC_FILE.read_text(encoding="utf-8")) or {}
    node = toc
    for part in key_path.split("/"):
        if not isinstance(node, dict) or part not in node:
            return None
        node = node[part]
    if isinstance(node, dict):
        return node.get("title")
    if isinstance(node, str):
        return node
    return None


def build_header(rel: str, entry: Dict, translated_at: str) -> str:
    stem = Path(rel).stem
    key_path = rel[len("guide/"):-len(".adoc")] if rel.startswith(
        "guide/") and rel.endswith(".adoc") else None
    title = toc_title(key_path) if key_path else None
    if not title:
        title = stem
    url = f"{OFFICIAL_BASE}#core-{stem}"
    quote = (f"> 本文翻译自 Micronaut Core v5.2.25 官方文档 "
             f"[Guide – {title}]({url})，翻译基线锁定于 "
             f"{BASELINE_LOCK_DATE}，非官方译文，以英文原文为准。")
    comment = (f"<!-- upstream_file: {rel}  "
               f"upstream_commit: {entry.get('upstream_commit', '')}  "
               f"upstream_hash: {entry.get('blob_sha', '')}  "
               f"translated_at: {translated_at} -->")
    return quote + "\n" + comment


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(prog="assemble_zh.py",
                                     description="zh 落盘装配（溯源投影）")
    parser.add_argument("--file", nargs="+", required=True,
                        help="相对 source/ 的文件路径")
    parser.add_argument("--restored-dir", default=None,
                        help="还原文本根目录（默认 workdir/protect/source）")
    parser.add_argument("--translated-at",
                        default=datetime.date.today().isoformat())
    args = parser.parse_args(argv)

    try:
        manifest = yaml.safe_load(MANIFEST_FILE.read_text(encoding="utf-8"))
        entries = {f["file"]: f for f in manifest.get("files", [])}
        restored_root = (Path(args.restored_dir) if args.restored_dir
                         else REPO_ROOT / "workdir" / "protect" / "source")
        out = []
        for rel in args.file:
            entry = entries.get(rel)
            if entry is None:
                raise RuntimeError(f"manifest 无条目：{rel}")
            src = restored_root / Path(rel).parent / (
                f"{Path(rel).stem}-restored.txt")
            if not src.exists():
                raise RuntimeError(f"还原文本不存在：{src}")
            body = src.read_text(encoding="utf-8")
            if not body.endswith("\n"):
                body += "\n"
            zh_path = ZH_DIR / rel
            zh_path.parent.mkdir(parents=True, exist_ok=True)
            header = build_header(rel, entry, args.translated_at)
            zh_path.write_text(header + "\n\n" + body, encoding="utf-8")
            out.append({"file": rel, "zh": str(zh_path)})
        print(json.dumps({"written": out}, ensure_ascii=False))
    except (RuntimeError, OSError, yaml.YAMLError) as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
