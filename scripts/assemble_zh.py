#!/usr/bin/env python3
"""zh 落盘装配：还原文本 + 溯源投影（PLAN §5.4）→ zh/<rel>。

输入为 protect/restore 流水线产出的 <stem>-restored.txt；
页头引用块 + HTML 注释四字段的字段值全部取自账本
（upstream_commit / blob_sha），禁止手抄哈希。

CLI：
  --file REL [REL ...]   相对 source/ 的文件路径（guide/... 或
                         modules/<site>/guide/...——模块文件自动取
                         manifests/<site>.yml 账本与模块 toc，DR-006 §4）
  --restored-dir DIR     还原文本根目录（默认 workdir/protect/source）
  --translated-at DATE   translated_at 字段（默认当天）
  --baseline-date DATE   引用块中的基线锁定日期（默认：core=PLAN §5.4 固定值，
                         模块=账本 locked_at）

页名取 toc.yml 的显示标题（英文原题）；
官方站 URL 锚点 = core-<文件 stem>（core）/ <site>-<stem>（模块，
官方站实测约定，锚 id 带站点前缀；核实日期 2026-11-20）。
模块基线为分支 HEAD（DR-006 §6），引用块标注分支 + 锁定日期。

退出码：0 成功 / 2 环境错误（账本缺条目、还原文本缺失等）。
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
MODULES_JSON = REPO_ROOT / "config" / "modules.json"
BASELINE_LOCK_DATE = "2026-11-19"
OFFICIAL_BASE = "https://docs.micronaut.io/5.2.x/"

_MANIFEST_CACHE: Dict[str, dict] = {}


def module_site_of(rel: str) -> Optional[str]:
    """模块文件路径（modules/<site>/…）→ site；core 文件返回 None。"""
    parts = rel.split("/")
    if len(parts) > 3 and parts[0] == "modules":
        return parts[1]
    return None


def manifest_for(site: Optional[str]) -> dict:
    path = (REPO_ROOT / "manifests" / f"{site}.yml" if site
            else MANIFEST_FILE)
    key = str(path)
    if key not in _MANIFEST_CACHE:
        _MANIFEST_CACHE[key] = yaml.safe_load(
            path.read_text(encoding="utf-8"))
    return _MANIFEST_CACHE[key]


def module_title_of(site: str) -> str:
    """模块显示标题（config/modules.json）；缺省回退 site 首字母大写。"""
    if MODULES_JSON.exists():
        try:
            data = json.loads(MODULES_JSON.read_text(encoding="utf-8"))
            t = (data.get("modules") or {}).get(site, {}).get("title")
            if t:
                return t
        except (OSError, ValueError):
            pass
    return site.capitalize()


def toc_title(key_path: str, toc_file: Path) -> Optional[str]:
    """按 toc 键路径（如 ioc/beans）取显示标题；缺省 None。"""
    if not toc_file.exists():
        return None
    toc = yaml.safe_load(toc_file.read_text(encoding="utf-8")) or {}
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


def build_header(rel: str, entry: Dict, translated_at: str,
                 baseline_date: Optional[str]) -> str:
    stem = Path(rel).stem
    site = module_site_of(rel)
    m = manifest_for(site)
    if site:
        doc_rel = rel[len(f"modules/{site}/"):]
        toc_file = SOURCE_DIR / f"modules/{site}/guide/toc.yml"
        mod_title = module_title_of(site)
        title = mod_title
        m = manifest_for(site)
        url = f"{OFFICIAL_BASE}{site}/#{site}-{stem}"
        quote = (f"> 本文翻译自 Micronaut {mod_title} 官方文档"
                 f"（{m.get('ref') or '5.2.x'} 分支基线，"
                 f"{m.get('locked_at') or '—'} 锁定）")
        label_prefix = f"{mod_title} – "
    else:
        doc_rel = rel
        toc_file = SOURCE_DIR / "guide" / "toc.yml"
        title = None
        url = f"{OFFICIAL_BASE}core/#core-{stem}"
        quote = (f"> 本文翻译自 Micronaut Core v5.2.25 官方文档 ")
        label_prefix = "Guide – "
    key_path = (doc_rel[len("guide/"):-len(".adoc")]
                if doc_rel.startswith("guide/") and doc_rel.endswith(".adoc")
                else None)
    if key_path:
        toc_t = toc_title(key_path, toc_file)
        if toc_t:
            title = toc_t
    if not title:
        title = stem
    if site:
        quote += f" [{label_prefix}{title}]({url})，非官方译文，以英文原文为准。"
    else:
        # core 引用块格式逐字节不变（PLAN §5.4；与既有 387 译文一致）
        quote += (f"[{label_prefix}{title}]({url})，翻译基线锁定于 "
                  f"{baseline_date or BASELINE_LOCK_DATE}，"
                  f"非官方译文，以英文原文为准。")
    comment = (f"<!-- upstream_file: {rel}  "
               f"upstream_commit: {entry.get('upstream_commit') or manifest.get('upstream', {}).get('baseline_commit', '')}  "
               f"upstream_hash: {entry.get('blob_sha', '')}  "
               f"translated_at: {translated_at} -->")
    return quote + "\n" + comment


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(prog="assemble_zh.py",
                                     description="zh 落盘装配（溯源投影）")
    parser.add_argument("--file", nargs="+", required=True,
                        help="相对 source/ 的文件路径（模块文件带 "
                             "modules/<site>/ 前缀）")
    parser.add_argument("--restored-dir", default=None,
                        help="还原文本根目录（默认 workdir/protect/source）")
    parser.add_argument("--translated-at",
                        default=datetime.date.today().isoformat())
    parser.add_argument("--baseline-date", default=None,
                        help="core 引用块基线锁定日期（默认 PLAN §5.4 固定值；"
                             "模块取账本 locked_at）")
    args = parser.parse_args(argv)

    try:
        restored_root = (Path(args.restored_dir) if args.restored_dir
                         else REPO_ROOT / "workdir" / "protect" / "source")
        out = []
        for rel in args.file:
            site = module_site_of(rel)
            manifest = manifest_for(site)
            entries = {f["file"]: f for f in manifest.get("files", [])}
            entry = entries.get(rel)
            if entry is None:
                raise RuntimeError(f"账本无条目：{rel}")
            src = restored_root / Path(rel).parent / (
                f"{Path(rel).stem}-restored.txt")
            if not src.exists():
                raise RuntimeError(f"还原文本不存在：{src}")
            body = src.read_text(encoding="utf-8")
            if not body.endswith("\n"):
                body += "\n"
            zh_path = ZH_DIR / rel
            zh_path.parent.mkdir(parents=True, exist_ok=True)
            header = build_header(rel, entry, args.translated_at,
                                  args.baseline_date)
            zh_path.write_text(header + "\n\n" + body, encoding="utf-8")
            out.append({"file": rel, "zh": str(zh_path)})
        print(json.dumps({"written": out}, ensure_ascii=False))
    except (RuntimeError, OSError, yaml.YAMLError) as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
