#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""toc.yml / toc-python.yml 结构校验（M3 任务1，PLAN §1.2）。

对每个导航 YAML 校验：
  1. zh 键树与 source 逐一对齐（键名与嵌套顺序完全一致，title 伪键不参与）；
  2. 标题值已译：值含 CJK，或命中白名单（API 名/产品名等不译条目），
     且未命中白名单的值不得与源值逐字节相同（漏译检测）；
  3. 源文件注释行逐字节保留；
  4. zh 侧溯源投影：`# >` 引用行 + `<!-- upstream_file/commit/hash/translated_at -->`
     注释存在，且 file/commit/hash 三字段与 manifest.yml 对齐（对齐 sync --mark-current 口径）。

用法：memgate 2048 python3 scripts/check_toc.py [--file guide/toc.yml]
退出码：0=全过 / 2=校验失败。仅做只读校验，不写任何文件。
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import yaml

ROOT = Path(__file__).resolve().parent.parent
SOURCE_DIR = ROOT / "source"
ZH_DIR = ROOT / "zh"
MANIFEST = ROOT / "manifest.yml"

# 值不含 CJK 的合法条目（API 名/产品名/品牌章节名，不译）
ALLOWLIST = {
    "@Blocking", "IntelliJ IDEA", "Visual Studio Code", "Eclipse",
    "Apache NetBeans", "Micronaut Banner", "BeanContext", "BeanWrapper API",
    "ExceptionHandler", "HttpServerFilter", "JsonMapper", "Service Loader",
    "Cross-Origin-Embedder-Policy", "Cross-Origin-Resource-Policy",
    "Continuation", "Micronaut for Java", "Micronaut for Groovy",
    "Micronaut for Python", "Micronaut for Kotlin", "Micronaut for GraalVM",
    "Async/Await", "AWS Lambda", "Google Cloud Function", "Google Cloud Run",
    "Azure Function", "Logback", "Features", "JRebel", "ApplicationContext",
    "Micronaut CLI", "bean",
}

RE_PROVENANCE = re.compile(
    r"<!--\s*upstream_file:\s*(\S+)\s+upstream_commit:\s*([0-9a-f]{40})\s+"
    r"upstream_hash:\s*([0-9a-f]{40})\s+translated_at:\s*(\d{4}-\d{2}-\d{2})\s*-->")

CJK = re.compile(r"[\u4e00-\u9fff]")


def iter_pages(node, prefix=()):
    """yield (dotted_page_path, title_value)；title 伪键由父键承载。"""
    for k, v in node.items():
        if k == "title" and not isinstance(v, dict):
            continue
        p = prefix + (k,)
        if isinstance(v, dict):
            yield ".".join(p), v.get("title")
            yield from iter_pages(v, p)
        else:
            yield ".".join(p), v


def _load_manifest_entries() -> Dict[str, dict]:
    data = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
    return {e["file"]: e for e in data["files"]}


def check_file(rel: str, entries: Dict[str, dict]) -> Tuple[List[str], int]:
    """校验单个 toc 文件，返回 (问题列表, 校验页面数)。"""
    problems: List[str] = []
    src_path = SOURCE_DIR / rel
    zh_path = ZH_DIR / rel
    if not src_path.exists():
        return [f"源文件不存在：{src_path}"], 0
    if not zh_path.exists():
        return [f"译文不存在：{zh_path}"], 0
    src_text = src_path.read_text(encoding="utf-8")
    zh_text = zh_path.read_text(encoding="utf-8")
    src_data = yaml.safe_load(src_text)
    zh_data = yaml.safe_load(zh_text)

    src_pages = list(iter_pages(src_data))
    zh_pages = list(iter_pages(zh_data))
    if [p for p, _ in src_pages] != [p for p, _ in zh_pages]:
        problems.append("键树与源不对齐（键名或顺序差异）")
    n_pages = len(src_pages)
    for (sp, sv), (zp, zv) in zip(src_pages, zh_pages):
        if zv is None:
            problems.append(f"{sp}: 标题值为空")
            continue
        if not CJK.search(zv) and zv not in ALLOWLIST:
            problems.append(f"{sp}: 标题未译且不在白名单：{zv!r}")
        elif CJK.search(zv) and sv is not None and zv == sv:
            problems.append(f"{sp}: 标题与源逐字节相同（疑似漏译）")

    src_comments = [l for l in src_text.splitlines() if l.strip().startswith("#")]
    zh_lines = zh_text.splitlines()
    for c in src_comments:
        if c not in zh_lines:
            problems.append(f"注释行丢失：{c!r}")
    if len(zh_lines) != len(src_text.splitlines()) + 3:
        problems.append(f"行数异常：zh={len(zh_lines)} 源+3 应为 "
                        f"{len(src_text.splitlines()) + 3}")
    if not any(l.startswith("# > ") for l in zh_lines):
        problems.append("缺页头溯源引用行（# > 本文翻译自…）")

    mo = RE_PROVENANCE.search(zh_text)
    if mo is None:
        problems.append("缺溯源注释（upstream_file/upstream_commit/upstream_hash/"
                        "translated_at）")
    else:
        f_file, f_commit, f_hash, _ = mo.groups()
        entry = entries.get(rel)
        if entry is None:
            problems.append(f"manifest 中不存在 {rel}")
        else:
            if f_file != rel:
                problems.append(f"upstream_file={f_file!r} != {rel!r}")
            if f_hash != entry["blob_sha"]:
                problems.append(f"upstream_hash={f_hash[:8]}… != manifest "
                                f"blob_sha={entry['blob_sha'][:8]}…")
            expect_commit = entry.get("upstream_commit")
            if expect_commit and f_commit != expect_commit:
                problems.append(f"upstream_commit={f_commit[:8]}… != manifest "
                                f"{expect_commit[:8]}…")
    return problems, n_pages


def main() -> int:
    ap = argparse.ArgumentParser(description="toc.yml 结构校验（只读）")
    ap.add_argument("--file", metavar="NAME", default=None,
                    help="仅校验单个文件（如 guide/toc.yml）；缺省校验全部 toc*")
    args = ap.parse_args()

    targets = sorted(p.relative_to(SOURCE_DIR).as_posix()
                     for p in (SOURCE_DIR / "guide").glob("toc*.yml"))
    if args.file:
        targets = [args.file] if args.file in targets else []
        if not targets:
            print(json.dumps({"result": "FAILED", "errors": [f"未知文件 {args.file}"]},
                             ensure_ascii=False))
            return 2
    entries = _load_manifest_entries()
    all_problems: List[str] = []
    total = 0
    for rel in targets:
        problems, n = check_file(rel, entries)
        total += n
        for p in problems:
            all_problems.append(f"[{rel}] {p}")
    result = {"result": "PASSED" if not all_problems else "FAILED",
              "files": targets, "pages": total, "errors": all_problems}
    print(json.dumps(result, ensure_ascii=False))
    return 0 if not all_problems else 2


if __name__ == "__main__":
    sys.exit(main())
