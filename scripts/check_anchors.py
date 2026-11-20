#!/usr/bin/env python3
"""xref/锚点完整性检查，产出 config/anchor-registry.yml（PLAN §5.6）。

扫描 source/ 全量 .adoc：
  - 锚点定义：[[id]] / [[id,reftext]] / [#id]（块属性锚）；
  - xref 引用：xref::?target[...] 与 <<target[,label]>>；
  - 每个被引用锚点登记：锚点 → 所在文件 / 标题 / 引用方清单；
  - 引用目标解析失败的列入 unresolved（登记表内保留，供 M3 断链清零跟踪）。

translator prompt 必读本登记表：翻译被引用标题时原位注入 [[原锚点]]。
退出码：0 正常；无致命失败分支（unresolved 只登记不阻断）。
"""

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Optional

import yaml

sys.path.insert(0, str(Path(__file__).parent))
from segment_adoc import segment_adoc  # directive/anchor 段型复用  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parent.parent
SOURCE_DIR = REPO_ROOT / "source"
REGISTRY_FILE = REPO_ROOT / "config" / "anchor-registry.yml"

RE_ANCHOR_DEF = re.compile(r"^\[\[([^\],]+)(?:,([^\]]*))?\]\]\s*$")
RE_BLOCK_ID = re.compile(r"^\[#([^\s\]]+)\]\s*$")
RE_XREF = re.compile(
    r"(?:xref::?(\S*?)\[[^\]]*\]|<<([^>,\s]+)(?:,[^>]*)?>>)")


def scan_file_anchors(text: str) -> Dict[str, dict]:
    """收集单文件锚点定义：id → {reftext, title, line}。

    [#id] 简写锚附着于其后第一个标题/块，[[id]] 常紧邻标题——
    两者都回填下一个标题行文本作为 title。"""
    from segment_adoc import RE_HEADING  # 局部导入避免循环
    anchors: Dict[str, dict] = {}
    pending: Optional[str] = None
    for i, line in enumerate(text.split("\n"), 1):
        st = line.strip()
        m = RE_ANCHOR_DEF.match(st)
        if m:
            anchors[m.group(1).strip()] = {
                "reftext": (m.group(2) or "").strip(),
                "title": "", "line": i, "explicit": True}
            pending = m.group(1).strip()
            continue
        m = RE_BLOCK_ID.match(st)
        if m:
            anchors[m.group(1).strip()] = {
                "reftext": "", "title": "", "line": i, "explicit": True}
            pending = m.group(1).strip()
            continue
        if RE_HEADING.match(st):
            if pending and pending in anchors:
                equals = RE_HEADING.match(st).group(1)
                anchors[pending]["title"] = st[len(equals):].strip()
            pending = None
            continue
        pending = None
    return anchors


def collect_xrefs(text: str) -> List[str]:
    """收集单文件 xref 目标（file#anchor / #anchor / file）。"""
    targets = []
    for m in RE_XREF.finditer(text):
        t = (m.group(1) or m.group(2) or "")
        if t:
            targets.append(t.strip())
    return targets


def build_registry(source_dir: Path) -> Dict:
    """扫描全量 source/ 构建登记表数据结构。"""
    anchors_by_file: Dict[str, Dict[str, dict]] = {}
    referenced_by: Dict[str, List[str]] = defaultdict(list)
    unresolved: List[Dict] = []
    files = sorted(source_dir.rglob("*.adoc"))
    texts = {}
    basename_index: Dict[str, List[str]] = defaultdict(list)
    for f in files:
        rel = f.relative_to(source_dir).as_posix()
        texts[rel] = f.read_text(encoding="utf-8", errors="replace")
        anchors_by_file[rel] = scan_file_anchors(texts[rel])
        basename_index[f.stem].append(rel)
    for rel in sorted(texts):
        for target in collect_xrefs(texts[rel]):
            fpart, sep, anchor = target.partition("#")
            fpart = fpart.strip()
            anchor = anchor.strip()
            if fpart.startswith(("http://", "https://", "ftp://", "mailto:")):
                # 仅按协议头识别 URL；裸锚点如 httpServer/httpClient 以
                # "http" 开头但并非 URL，不得误跳过（B01 实测缺陷修复）
                continue
            if not sep and fpart:
                # 无 #：页级文件引用（含 / 或 .adoc）或裸锚点
                if "." in fpart or "/" in fpart:
                    anchor = ""
                else:
                    anchor, fpart = fpart, ""
            if not fpart and not anchor:
                continue
            if fpart and fpart not in texts:
                unresolved.append({"target": target, "from": rel,
                                   "reason": "file-missing"})
                continue
            if fpart and not anchor:
                continue  # 页级文件引用，存在性已验证
            if fpart and fpart not in texts:
                unresolved.append({"target": target, "from": rel,
                                   "reason": "file-missing"})
                continue
            if fpart:
                if anchor in anchors_by_file[fpart]:
                    referenced_by[f"{fpart}#{anchor}"].append(rel)
                else:
                    unresolved.append({"target": target, "from": rel,
                                       "reason": "anchor-missing"})
            else:
                # 裸锚点全域解析：
                # ① 显式 [[id]] 定义；② micronaut 约定——锚 id = include 文件
                # basename（如 <<buildCLI>> → guide/quickStart/buildCLI.adoc，
                # 标题取该文件首个标题）；都失败才记 unresolved。
                hits = [f for f in sorted(anchors_by_file)
                        if anchor in anchors_by_file[f]]
                if not hits:
                    hits = sorted(basename_index.get(anchor, []))
                if hits:
                    for f in hits:
                        referenced_by[f"{f}#{anchor}"].append(rel)
                else:
                    unresolved.append({"target": target, "from": rel,
                                       "reason": "anchor-missing"})
    anchors = []
    for key, refs in sorted(referenced_by.items()):
        fpart, anchor = key.split("#", 1)
        a = anchors_by_file[fpart].get(anchor) or {}
        title = a.get("title", "")
        if not title:
            # basename 派生锚：标题 = 该文件首个标题行
            from segment_adoc import RE_HEADING
            for line in texts[fpart].split("\n"):
                if RE_HEADING.match(line.strip()):
                    equals = RE_HEADING.match(line.strip()).group(1)
                    title = line.strip()[len(equals):].strip()
                    break
        anchors.append({
            "id": anchor,
            "file": fpart,
            "title": title,
            "reftext": a.get("reftext", ""),
            "explicit": a.get("explicit", False),
            "referenced_by": sorted(set(refs)),
        })
    return {"anchors": anchors, "unresolved": unresolved,
            "scanned_files": len(files)}


def write_registry(source_dir: Path, out_file: Path) -> Dict:
    data = build_registry(source_dir)
    header = (
        "# 锚点登记表（check_anchors.py 自动生成，禁手改）\n"
        "# 被引用锚点 → 所在文件/标题；translator 翻译被引用标题时\n"
        "# 原位注入 [[原锚点]]（PLAN §5.6）。unresolved 供 M3 断链清零跟踪。\n")
    out_file.parent.mkdir(parents=True, exist_ok=True)
    out_file.write_text(header + yaml.safe_dump(
        data, allow_unicode=True, sort_keys=False), encoding="utf-8")
    return data


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        prog="check_anchors.py",
        description="扫描 source/ 的 xref/锚点，产出 config/anchor-registry.yml")
    parser.add_argument("--source-dir", default=None,
                        help="覆盖 source 目录（测试注入）")
    parser.add_argument("--out", default=None, help="覆盖登记表输出路径")
    args = parser.parse_args(argv)
    source_dir = (Path(args.source_dir) if args.source_dir
                  else SOURCE_DIR)
    out = Path(args.out) if args.out else REGISTRY_FILE
    data = write_registry(source_dir, out)
    print(__import__("json").dumps(
        {"anchors": len(data["anchors"]),
         "unresolved": len(data["unresolved"]),
         "files": data["scanned_files"]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())