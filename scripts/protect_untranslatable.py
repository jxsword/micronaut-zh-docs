#!/usr/bin/env python3
"""不可译片段保护与还原（asciidoc 版，自 spdlog protect_untranslatable.py 适配）。

CLI 双子命令（PLAN §5.2）：
  --protect FILE...   对源文件生成受保护文本 + 映射表（workdir/protect/ 下）
  --restore FILE...   按 HASH 完整还原并校验无残留/无丢失（退出码：0 成功 / 2 失败）

批次流程（PLAN §5.1）：
  1. --protect source/guide/a.adoc
     → workdir/protect/guide/a-protected.txt          （translator 输入）
     → workdir/protect/guide/a-protected-map.json     （占位符映射，可由源确定性再生）
  2. translator 翻译 a-protected.txt → a-translated.txt（同目录，编排方或 agent 落盘）
  3. --restore workdir/protect/guide/a-translated.txt
     → workdir/protect/guide/a-restored.txt           （校验通过后移入 zh/）

设计要点：
  - 行级不可译构造（逐字块/指令/条件/属性行/锚点行/定界行）由 segment_adoc
    段型判定，整段替换为占位符 `{{PROTECTED_<TYPE>_<hash8>}}`；
  - 行内构造：xref/link 目标、pass::[]、行内锚点、inline code、URL、
    属性引用 {name}、admonition 标记、表格 |=== 定界行与单元格分隔符；
  - 占位符 = sha256(原文)[:8] → 同一片段占位符相同，重复片段幂等还原；
  - xref/link 只保护目标部分，[显示文本] 保留可译（对齐 spdlog LINK 策略）；
  - --restore 哈希完整性校验：映射丢失/占位符残留/译丢段均报错。

保护清单出处：PLAN §5.2（include::[]、xref::[]、link:[]、source::[]/source[]、
ifdef/ifndef/ifeval/endif、行内 code、URL、[[显式锚点]]、属性定义行、
admonition 标记、表格对齐符）。
"""

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

sys.path.insert(0, str(Path(__file__).parent))
from segment_adoc import segment_adoc  # noqa: E402

REPO_ROOT = Path(__file__).parent.parent.resolve()
PROTECT_DIR = REPO_ROOT / "workdir" / "protect"

# ---------- 行级段型（整段 → 占位符） ----------

TRANSIENT_TYPES = frozenset({"code_block", "directive", "conditional",
                             "attribute", "anchor", "block_delimiter"})

TRANSIENT_TYPE_NAMES = {"code_block": "CODEBLOCK", "directive": "DIRECTIVE",
                        "conditional": "CONDITIONAL", "attribute": "ATTRIBUTE",
                        "anchor": "ANCLINE", "block_delimiter": "DELIM"}

# ---------- 行内模式（按序应用） ----------

INLINE_PATTERNS = [
    # xref/link 目标：保护 `xref:target` / `link:url` 前缀，[显示文本] 保留可译
    (re.compile(r"\b(?:xref|link)::?(\S*?)(?=\[)"), "XREF"),
    # pass::[] 穿透宏整体保护
    (re.compile(r"\bpass::?\[[^\]]*\]"), "PASS"),
    # 行内锚点 [[id]] / [[id,reftext]]
    (re.compile(r"\[\[([^\]]+)\]\]"), "ANCHOR"),
    # 行内代码 `text`（asciidoc 单反引号）
    (re.compile(r"`[^`\n]+`"), "CODE"),
    # URL（xref/link 目标已先行保护，此处覆盖裸 URL）
    (re.compile(r"\b(?:https?|ftp)://[^\s\[\]<>()\"{}|\\^`]+"), "URL"),
    # 属性引用 {name}（排除 PROTECTED 占位符自身，见 RE_ATTRREF 注释）
    (re.compile(r"\{(?!PROTECTED_)[^{}\n]+\}"), "ATTRREF"),
]

# table 段内专用
RE_TABLE_DELIM_LINE = re.compile(r"^\|===\s*$", re.MULTILINE)
RE_CELLSEP = re.compile(r"(^|\s)\|(?=\s|\S)")

RE_ADMONITION_MARKER = re.compile(r"^(NOTE|TIP|IMPORTANT|WARNING|CAUTION):",
                                  re.MULTILINE)

RE_RESIDUAL = re.compile(r"\{\{PROTECTED_[A-Za-z0-9_]+_[0-9a-f]{8}\}\}")


def generate_placeholder(ptype: str, content: str) -> str:
    phash = hashlib.sha256(content.encode("utf-8")).hexdigest()[:8]
    return f"{{{{PROTECTED_{ptype}_{phash}}}}}"


def _add(ph_map: Dict[str, str], ptype: str, content: str) -> str:
    ph = generate_placeholder(ptype, content)
    if ph in ph_map and ph_map[ph] != content:
        # sha256[:8] 碰撞防御（64bit 空间，实际不可达，防御性报错）
        raise RuntimeError(f"placeholder hash collision: {ph}")
    ph_map[ph] = content
    return ph


def _protect_segment(seg) -> Tuple[str, Dict[str, str]]:
    """对单分段保护：行级段型整段替换；其余做行内保护。

    返回 (protected_text, placeholder_map)。"""
    ph_map: Dict[str, str] = {}
    if seg.type in TRANSIENT_TYPES:
        ph = _add(ph_map, TRANSIENT_TYPE_NAMES[seg.type], seg.content)
        return ph, ph_map

    text = seg.content

    if seg.type == "table":
        def _delim(m):
            return _add(ph_map, "TABLEDELIM", m.group(0))
        text = RE_TABLE_DELIM_LINE.sub(_delim, text)

        def _cellsep(m):
            return m.group(1) + _add(ph_map, "CELLSEP", "|")
        text = RE_CELLSEP.sub(_cellsep, text)

    if seg.type == "admonition":
        def _adm(m):
            return _add(ph_map, "ADMON", m.group(0))
        text = RE_ADMONITION_MARKER.sub(_adm, text)

    for pattern, ptype in INLINE_PATTERNS:
        def _repl(m, ptype=ptype):
            return _add(ph_map, ptype, m.group(0))
        text = pattern.sub(_repl, text)

    return text, ph_map


def protect(content: str, fname: str = "<inline>") -> Tuple[str, Dict[str, str]]:
    """整文件保护：先分段，再逐段保护。返回 (protected_text, placeholder_map)。

    段间以原文件行序拼接（行级段型 → 占位符行），保留空行结构。"""
    segments = segment_adoc(content, fname)
    ph_map: Dict[str, str] = {}
    out_lines: List[str] = []
    last_line = 0
    for seg in segments:
        # 补回段前空行（分段器跳过的空行按行号重建）
        for _ in range(seg.line_start - last_line - 1):
            out_lines.append("")
        ptext, seg_map = _protect_segment(seg)
        ph_map.update(seg_map)
        out_lines.append(ptext)
        last_line = seg.line_end
    # 文件尾空行
    total = len(content.split("\n"))
    for _ in range(total - last_line):
        out_lines.append("")
    return "\n".join(out_lines), ph_map


def restore(text: str, ph_map: Dict[str, str],
            strict: bool = True) -> str:
    """按映射完整还原；strict 模式校验无残留/无丢失（哈希完整性）。

    校验项：
      - 映射丢失：译文中占位符不在映射内（映射表损坏/不同版本）→ 报错；
      - 占位符残留：还原后仍有 PROTECTED_ 残留 → 报错；
      - 占位符丢失：映射内的占位符在译文中不存在（译文删段）→ strict 下报错
        （允许调用方对删除段落场景传 strict=False）。"""
    present = set(RE_RESIDUAL.findall(text))
    missing_map = present - set(ph_map.keys())
    if missing_map:
        raise RuntimeError(
            f"restore 失败：{len(missing_map)} 个占位符无映射（映射表与文本不匹配）："
            f"{sorted(missing_map)[:5]}")
    lost = [ph for ph in ph_map if ph not in present]
    if lost and strict:
        raise RuntimeError(
            f"restore 失败：{len(lost)} 个映射项在译文中缺失（疑似译丢段）："
            f"{sorted(lost)[:5]}")
    restored = text
    for ph, original in ph_map.items():
        if ph in restored:
            restored = restored.replace(ph, original)
    residue = RE_RESIDUAL.findall(restored)
    if residue:
        raise RuntimeError(f"restore 失败：还原后仍有 {len(residue)} 处占位符残留")
    return restored


def restore_lenient(text: str, ph_map: Dict[str, str]) -> str:
    """宽松还原：允许译文已删除的占位符（评审后确认删除的段落）。"""
    return restore(text, ph_map, strict=False)


def protect_file(src_file: Path, out_dir: Path) -> Tuple[Path, Path]:
    """对源文件生成受保护文本与映射表，写入 out_dir 镜像路径。

    返回 (protected_path, map_path)。文件名纪律：扩展名前仅字母/数字/汉字/
    下划线/连字符（STEM-protected.txt / STEM-protected-map.json）。"""
    src_abs = src_file.resolve()
    if src_abs.is_relative_to(REPO_ROOT):
        rel = src_abs.relative_to(REPO_ROOT)
    else:
        # 仓库外路径（测试注入）：保留末两级目录结构（parent/file）
        parts = src_abs.parts
        rel = Path(*parts[-2:]) if len(parts) >= 2 else Path(src_abs.name)
    stem = src_file.stem
    out_base = out_dir / rel.parent / stem
    out_base.parent.mkdir(parents=True, exist_ok=True)
    content = src_file.read_text(encoding="utf-8")
    protected, ph_map = protect(content, str(rel))
    prot_path = out_base.with_name(f"{stem}-protected.txt")
    map_path = out_base.with_name(f"{stem}-protected-map.json")
    prot_path.write_text(protected + "\n", encoding="utf-8")
    map_path.write_text(json.dumps(ph_map, ensure_ascii=False, indent=1,
                                   sort_keys=True), encoding="utf-8")
    return prot_path, map_path


def restore_file(translated_file: Path, map_path: Optional[Path] = None,
                 out_path: Optional[Path] = None,
                 strict: bool = True) -> Path:
    """还原译文文件；映射缺省取同目录 `<stem>-protected-map.json`。

    输出 `<stem>-restored.txt`（或 out_path）。"""
    map_path = map_path or translated_file.with_name(
        translated_file.name.replace("-translated.txt", "-protected-map.json"))
    if not map_path.exists():
        raise RuntimeError(f"映射表不存在：{map_path}")
    ph_map = json.loads(map_path.read_text(encoding="utf-8"))
    text = translated_file.read_text(encoding="utf-8")
    restored = restore(text, ph_map, strict=strict)
    if out_path is None:
        out_path = translated_file.with_name(
            translated_file.name.replace("-translated.txt", "-restored.txt"))
    out_path.write_text(restored, encoding="utf-8")
    return out_path


# ---------- CLI ----------

def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        prog="protect_untranslatable.py",
        description="asciidoc 不可译片段保护/还原（--protect / --restore）")
    g = parser.add_mutually_exclusive_group(required=True)
    g.add_argument("--protect", nargs="+", metavar="FILE",
                   help="对源文件生成受保护文本与映射表")
    g.add_argument("--restore", nargs="+", metavar="FILE",
                   help="还原译文文件（读取同名 -protected-map.json）")
    parser.add_argument("--outdir", default=None,
                        help=f"protect 输出目录（默认 {PROTECT_DIR}）")
    parser.add_argument("--lenient", action="store_true",
                        help="restore 允许译文缺失的占位符（确认删除段）")
    parser.add_argument("--stdout", action="store_true",
                        help="restore 结果打印到 stdout 而非写文件")
    args = parser.parse_args(argv)

    try:
        if args.protect:
            out_dir = Path(args.outdir) if args.outdir else PROTECT_DIR
            for f in args.protect:
                src = Path(f)
                if not src.exists():
                    raise RuntimeError(f"源文件不存在：{src}")
                prot, mp = protect_file(src, out_dir)
                print(json.dumps({
                    "file": str(src), "protected": str(prot), "map": str(mp),
                    "placeholders": len(json.loads(mp.read_text(encoding="utf-8"))),
                }, ensure_ascii=False))
        else:
            for f in args.restore:
                tf = Path(f)
                if not tf.exists():
                    raise RuntimeError(f"译文文件不存在：{tf}")
                out = restore_file(tf, strict=not args.lenient)
                if args.stdout:
                    print(out.read_text(encoding="utf-8"), end="")
                    out.unlink()
                else:
                    print(json.dumps({"restored": str(out)}, ensure_ascii=False))
    except (RuntimeError, OSError) as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
