#!/usr/bin/env python3
"""批次切分报告生成：reports/inventory-5.2.25.md（PLAN §8 / 任务 §7）。

口径（PLAN §5.1）：
  - 词数 = 占位符保护后 wc -w 等价（每个占位符计 1 词）；
  - 非代码词 = 仅可译段（heading/paragraph/admonition/table），剔除占位符后计数；
  - 批次双指标：非代码词 ≤3500 且总词 ≤5500，按 toc 阅读顺序贪心装箱。
"""

import json
import re
import sys
from pathlib import Path
from typing import Dict, List

import yaml

sys.path.insert(0, str(Path(__file__).parent))
from segment_adoc import is_shell_file, segment_adoc  # noqa: E402
from protect_untranslatable import protect  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parent.parent
SOURCE_DIR = REPO_ROOT / "source"
MANIFEST_FILE = REPO_ROOT / "manifest.yml"
REPORT_PATH = REPO_ROOT / "reports" / "inventory-5.2.25.md"
TOC_FILE = SOURCE_DIR / "guide" / "toc.yml"

BATCH_MAX_NONCODE = 3500
BATCH_MAX_TOTAL = 5500
RE_PH = re.compile(r"\{\{PROTECTED_[A-Za-z0-9_]+_[0-9a-f]{8}\}\}")


def toc_files(toc_path: Path) -> List[str]:
    """解析 toc.yml：DFS 键路径 → guide/<键路径>.adoc；跳过 title 键。"""
    data = yaml.safe_load(toc_path.read_text(encoding="utf-8"))
    ordered: List[str] = []
    missing = []

    def walk(d, prefix):
        for k, v in d.items():
            if k == "title" and not isinstance(v, dict):
                continue  # title 键是容器标题，非文件
            path = prefix + [k]
            rel = "/".join(["guide"] + path) + ".adoc"
            if (SOURCE_DIR / rel).exists():
                ordered.append(rel)
            else:
                missing.append(rel)
            if isinstance(v, dict):
                walk(v, path)

    walk(data or {}, [])
    return ordered, missing


def word_counts(rel: str) -> Dict[str, int]:
    """单文件词数：总词（保护后全文件）、非代码词（可译段剔占位符）。"""
    content = (SOURCE_DIR / rel).read_text(encoding="utf-8")
    protected, _ = protect(content, rel)
    total = len(protected.split())
    segs = segment_adoc(content, rel)
    prose = " ".join(s.content for s in segs if s.translatable)
    prose = RE_PH.sub(" ", prose)
    noncode = len(prose.split())
    return {"total": total, "noncode": noncode,
            "segments": len(segs)}


def pack_batches(ordered: List[str], counts: Dict[str, Dict[str, int]],
                 exclude: set) -> List[dict]:
    """toc 顺序贪心装箱：非代码词 ≤3500 且总词 ≤5500。"""
    batches: List[dict] = []
    cur: Dict = {"files": [], "noncode": 0, "total": 0}

    def close():
        nonlocal cur
        if cur["files"]:
            batches.append(cur)
            cur = {"files": [], "noncode": 0, "total": 0}

    for rel in ordered:
        if rel in exclude:
            continue
        c = counts[rel]
        if cur["files"] and (cur["noncode"] + c["noncode"] > BATCH_MAX_NONCODE
                             or cur["total"] + c["total"] > BATCH_MAX_TOTAL):
            close()
        cur["files"].append(rel)
        cur["noncode"] += c["noncode"]
        cur["total"] += c["total"]
        if cur["noncode"] > BATCH_MAX_NONCODE or cur["total"] > BATCH_MAX_TOTAL:
            # 单文件超限 → 独立批次（宁超不裂文件）
            close()
    close()
    return batches


def build_report(manifest: dict) -> str:
    ordered, toc_missing = toc_files(TOC_FILE)
    entries = {f["file"]: f for f in manifest["files"]}
    skipped = {f["file"] for f in manifest["files"]
               if f.get("status") == "skipped"}
    counts = {}
    for rel in sorted(entries):
        if rel.endswith((".yml",)):
            continue  # toc 文件单独处理（只译标题值，词数不进批次）
        counts[rel] = word_counts(rel)
    adoc = [r for r in sorted(entries) if not r.endswith(".yml")]
    ordered_adoc = [r for r in ordered if r not in skipped]
    leftover = sorted(set(adoc) - set(ordered_adoc) - skipped)
    ordered_adoc += leftover
    batches = pack_batches(ordered_adoc, counts, skipped)

    n_total = len(counts)
    sum_total = sum(c["total"] for c in counts.values())
    sum_noncode = sum(c["noncode"] for c in counts.values())
    sum_seg = sum(c["segments"] for c in counts.values())
    lines = [
        "# 全量清单与批次切分报告（v5.2.25 基线）",
        "",
        f"- 基线：micronaut-core@{manifest['upstream']['baseline_commit'][:12]}（tag v5.2.25），"
        f"快照 {manifest['upstream']['snapshot_date']}",
        f"- 账本：{len(manifest['files'])} 条目（含 guide/toc.yml、guide/toc-python.yml），"
        f"missing {sum(1 for f in manifest['files'] if f['status']=='missing')} / "
        f"skipped {len(skipped)}",
        f"- 词数总计：非代码词 {sum_noncode} / 总词 {sum_total} / 总段 {sum_seg}"
        "（口径：保护后 wc -w 等价）",
        f"- 批次：{len(batches)} 个（双指标 非代码词 ≤{BATCH_MAX_NONCODE} 且 "
        f"总词 ≤{BATCH_MAX_TOTAL}，toc 顺序贪心装箱）",
        "",
        "## toc.yml 实测结论",
        "",
        "- **含显示标题**：toc.yml 为嵌套 dict（键→显示标题），与 toc-python.yml "
        "（Python 文风定制版）共 30KB；两者均已入账本（可译对象为标题值，YAML 键不译）。",
        "- 键路径 → 文件映射：`guide/<键路径>.adoc`（DFS 序即阅读顺序）；"
        f"toc 覆盖 {len(ordered)} 个文件，未入 toc 的 include 片段 {len(leftover)} 个"
        "（按目录序追加在批次末尾）。",
        "- 纯 include 壳文件 2 个（guide/appendix.adoc、guide/i18n.adoc）标 skipped，"
        "不进批次。",
        "",
        "## 批次切分表",
        "",
        "| 批次 | 文件数 | 非代码词 | 总词 |",
        "|---|---:|---:|---:|",
    ]
    for i, b in enumerate(batches, 1):
        lines.append(
            f"| B{i:02d} | {len(b['files'])} | {b['noncode']} | {b['total']} |")
    lines += [
        "",
        "## 逐批次文件清单",
        "",
    ]
    for i, b in enumerate(batches, 1):
        files_s = "、".join(f"`{f}`" for f in b["files"])
        lines += [f"### B{i:02d}（非代码词 {b['noncode']} / 总词 {b['total']}）", "",
                  files_s, ""]
    if toc_missing:
        lines += ["## toc 键无对应文件的条目", ""]
        lines += [f"- {m}" for m in toc_missing]
    lines += ["", "---", "",
              "*inventory 自动生成：scripts/inventory.py（PLAN §8；批次数以本报告实测为准）*"]
    (REPO_ROOT / "reports").mkdir(exist_ok=True)
    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")
    return {"batches": len(batches), "files": n_total,
            "noncode": sum_noncode, "total": sum_total}


def main() -> int:
    if not MANIFEST_FILE.exists():
        print("ERROR: manifest.yml 不存在（先运行 sync --init）", file=sys.stderr)
        return 2
    manifest = yaml.safe_load(MANIFEST_FILE.read_text(encoding="utf-8"))
    stats = build_report(manifest)
    print(json.dumps(stats, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
