#!/usr/bin/env python3
"""批次切分报告生成（PLAN §5.1 口径；M4 起支持模块账本，DR-006 §4）。

core（缺省）：manifest.yml → reports/inventory-5.2.25.md，批次 B01…。
模块（--manifest manifests/<site>.yml）：账本字段带 modules/<site>/ 前缀，
  toc 取 source/modules/<site>/guide/toc.yml，报告 reports/inventory-<site>.md，
  批次编号 <前缀>-01…（前缀从 config/modules.json batch_prefix 取，缺省 site 大写）。

口径（PLAN §5.1）：
  - 词数 = 占位符保护后 wc -w 等价（每个占位符计 1 词）；
  - 非代码词 = 仅可译段（heading/paragraph/admonition/table），剔除占位符后计数；
  - 批次双指标：非代码词 ≤3500 且总词 ≤5500，按 toc 阅读顺序贪心装箱。
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import yaml

sys.path.insert(0, str(Path(__file__).parent))
from segment_adoc import is_shell_file, segment_adoc  # noqa: E402
from protect_untranslatable import protect  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parent.parent
SOURCE_DIR = REPO_ROOT / "source"
MANIFEST_FILE = REPO_ROOT / "manifest.yml"
MODULES_JSON = REPO_ROOT / "config" / "modules.json"
CORE_REPORT_PATH = REPO_ROOT / "reports" / "inventory-5.2.25.md"

BATCH_MAX_NONCODE = 3500
BATCH_MAX_TOTAL = 5500
RE_PH = re.compile(r"\{\{PROTECTED_[A-Za-z0-9_]+_[0-9a-f]{8}\}\}")


def resolve_target(manifest_arg: Optional[str]) -> Tuple[Path, str, str]:
    """--manifest → (账本路径, dest 前缀, site 名)；core 返回 (manifest.yml, '', 'core')。"""
    if manifest_arg is None:
        return MANIFEST_FILE, "", "core"
    mp = Path(manifest_arg).expanduser().resolve()
    if mp.name == "manifest.yml":
        return mp, "", "core"
    if mp.parent.name == "manifests" and mp.suffix == ".yml":
        return mp, f"modules/{mp.stem}", mp.stem
    raise ValueError(
        f"--manifest 须为 manifest.yml 或 manifests/<site>.yml：{manifest_arg}")


def batch_prefix_of(site: str, prefix_override: Optional[str]) -> str:
    """批次编号前缀：CLI 覆盖 > config/modules.json batch_prefix > site 大写。"""
    if prefix_override:
        return prefix_override
    if MODULES_JSON.exists():
        try:
            data = json.loads(MODULES_JSON.read_text(encoding="utf-8"))
            bp = (data.get("modules") or {}).get(site, {}).get("batch_prefix")
            if bp:
                return bp
        except (OSError, ValueError):
            pass
    return site.upper()


def toc_files(toc_path: Path, prefix: str) -> Tuple[List[str], List[str]]:
    """解析 toc.yml：DFS 键路径 → <prefix>/guide/<键路径>.adoc；跳过 title 键。

    返回 (有序文件列表[仓库相对路径], toc 键无对应文件列表)。"""
    data = yaml.safe_load(toc_path.read_text(encoding="utf-8"))
    ordered: List[str] = []
    missing = []
    guide_base = f"{prefix}/guide" if prefix else "guide"

    def walk(d, prefix_keys):
        for k, v in d.items():
            if k == "title" and not isinstance(v, dict):
                continue  # title 键是容器标题，非文件
            path = prefix_keys + [k]
            rel = "/".join([guide_base] + path) + ".adoc"
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


def build_report(manifest: dict, prefix: str, site: str, bp: str,
                 report_path: Path) -> dict:
    if not manifest.get("files"):
        raise RuntimeError("账本 files 为空——先运行 sync --init")
    toc_path = (SOURCE_DIR / prefix / "guide/toc.yml" if prefix
                else SOURCE_DIR / "guide/toc.yml")
    if not toc_path.exists():
        raise RuntimeError(f"toc 不存在：{toc_path}（模块首检：无 toc 需先造伪 toc）")
    ordered, toc_missing = toc_files(toc_path, prefix)
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
    up = manifest.get("upstream") or {}
    if site == "core":
        title = "全量清单与批次切分报告（v5.2.25 基线）"
        baseline_line = (f"- 基线：micronaut-core@{up.get('baseline_commit', '')[:12]}"
                         f"（tag v5.2.25），快照 {up.get('snapshot_date', '')}")
        ledger_line = (f"- 账本：{len(manifest['files'])} 条目"
                       "（含 guide/toc.yml、guide/toc-python.yml），")
        toc_notes = [
            "- **含显示标题**：toc.yml 为嵌套 dict（键→显示标题），与 toc-python.yml "
            "（Python 文风定制版）共 30KB；两者均已入账本（可译对象为标题值，YAML 键不译）。",
            "- 键路径 → 文件映射：`guide/<键路径>.adoc`（DFS 序即阅读顺序）；"
            f"toc 覆盖 {len(ordered)} 个文件，未入 toc 的 include 片段 {len(leftover)} 个"
            "（按目录序追加在批次末尾）。",
            "- 纯 include 壳文件 2 个（guide/appendix.adoc、guide/i18n.adoc）标 skipped，"
            "不进批次。",
        ]
    else:
        title = (f"模块批次切分报告：{site}"
                 f"（{up.get('remote', '')} @{up.get('baseline_commit', '')[:12]}）")
        baseline_line = (f"- 基线：{up.get('remote', '')}@{up.get('baseline_commit', '')[:12]}，"
                         f"ref {manifest.get('ref', '')}，快照 {up.get('snapshot_date', '')}"
                         f"（locked_at {manifest.get('locked_at', '')}）")
        ledger_line = f"- 账本：{len(manifest['files'])} 条目，"
        toc_notes = [
            f"- 键路径 → 文件映射：`{prefix}/guide/<键路径>.adoc`（DFS 序即阅读顺序）；"
            f"toc 覆盖 {len(ordered)} 个文件，未入 toc 的 include 片段 {len(leftover)} 个"
            "（按目录序追加在批次末尾）。",
        ]
    lines = [
        f"# {title}",
        "",
        baseline_line,
        ledger_line +
        f"missing {sum(1 for f in manifest['files'] if f['status']=='missing')} / "
        f"skipped {len(skipped)}",
        f"- 词数总计：非代码词 {sum_noncode} / 总词 {sum_total} / 总段 {sum_seg}"
        "（口径：保护后 wc -w 等价）",
        f"- 批次：{len(batches)} 个（双指标 非代码词 ≤{BATCH_MAX_NONCODE} 且 "
        f"总词 ≤{BATCH_MAX_TOTAL}，toc 顺序贪心装箱；编号前缀 {bp}-）",
        "",
        "## toc.yml 实测结论",
        "",
        *toc_notes,
        "",
        "## 批次切分表",
        "",
        "| 批次 | 文件数 | 非代码词 | 总词 |",
        "|---|---:|---:|---:|",
    ]
    for i, b in enumerate(batches, 1):
        lines.append(
            f"| {bp}-{i:02d} | {len(b['files'])} | {b['noncode']} | {b['total']} |")
    lines += [
        "",
        "## 逐批次文件清单",
        "",
    ]
    for i, b in enumerate(batches, 1):
        files_s = "、".join(f"`{f}`" for f in b["files"])
        lines += [f"### {bp}-{i:02d}（非代码词 {b['noncode']} / 总词 {b['total']}）",
                  "", files_s, ""]
    if toc_missing:
        lines += ["## toc 键无对应文件的条目", ""]
        lines += [f"- {m}" for m in toc_missing]
    footer = ("*inventory 自动生成：scripts/inventory.py"
              f"（{'PLAN §8' if site == 'core' else 'PLAN §5.1/DR-006 §4'}；"
              "批次数以本报告实测为准）*")
    lines += ["", "---", "", footer]
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("\n".join(lines), encoding="utf-8")
    return {"batches": len(batches), "files": n_total,
            "noncode": sum_noncode, "total": sum_total,
            "report": str(report_path)}


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        prog="inventory.py", description="批次切分报告（core/模块账本）")
    parser.add_argument("--manifest", default=None,
                        help="账本路径（缺省 manifest.yml=core；模块传 "
                             "manifests/<site>.yml）")
    parser.add_argument("--batch-prefix", default=None,
                        help="批次编号前缀（缺省：core=B；模块取 "
                             "config/modules.json batch_prefix，缺省 site 大写）")
    parser.add_argument("--report", default=None,
                        help="报告输出路径（缺省 reports/inventory-5.2.25.md / "
                             "reports/inventory-<site>.md）")
    args = parser.parse_args(argv)
    try:
        manifest_path, prefix, site = resolve_target(args.manifest)
        if not manifest_path.exists():
            print(f"ERROR: {manifest_path.name} 不存在（先运行 sync --init）",
                  file=sys.stderr)
            return 2
        manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
        bp = batch_prefix_of(site, args.batch_prefix)
        report_path = (Path(args.report) if args.report else
                       (CORE_REPORT_PATH if site == "core" else
                        REPO_ROOT / "reports" / f"inventory-{site}.md"))
        stats = build_report(manifest, prefix, site, bp, report_path)
        print(json.dumps(stats, ensure_ascii=False))
        return 0
    except (RuntimeError, OSError, ValueError, yaml.YAMLError) as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
