#!/usr/bin/env python3
"""译文硬门禁校验器（PLAN §5.5 七项，全部硬性）。

七项门禁：
  ① 占位符全部还原（zh 中 0 处 PROTECTED_ 残留）
  ② 代码块与指令行与上游逐字节一致
  ③ banned 黑名单 0 命中 + 必译术语命中检查（glossary.yml）
  ④ 结构对齐：标题层级数与顺序一致，标题文本已译
  ⑤ xref/锚点目标存在（未译文件豁免）
  ⑥ 溯源投影四字段齐全且与 manifest 一致
  ⑦ 风格机检子集：中英文空格 / 全角标点 / 禁繁体 / 邻接规则

校验范围天然豁免 PROTECTED 占位符与代码块。
退出码：0 全绿 / 1 有错误 / 2 环境错误。
"""

import argparse
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import yaml

sys.path.insert(0, str(Path(__file__).parent))
from segment_adoc import RE_HEADING, RE_DIRECTIVE, segment_adoc  # noqa: E402

REPO_ROOT = Path(__file__).parent.parent.resolve()
SOURCE_DIR = REPO_ROOT / "source"
ZH_DIR = REPO_ROOT / "zh"
MANIFEST_FILE = REPO_ROOT / "manifest.yml"
GLOSSARY_FILE = REPO_ROOT / "config" / "glossary.yml"
ANCHOR_REGISTRY = REPO_ROOT / "config" / "anchor-registry.yml"

MAX_ZH_BYTES = 4 * 1024 * 1024

RE_PROVENANCE = re.compile(
    r"<!--\s*upstream_file:\s*(\S+)\s+upstream_commit:\s*([0-9a-f]{40})\s+"
    r"upstream_hash:\s*([0-9a-f]{40})\s+translated_at:\s*(\d{4}-\d{2}-\d{2})\s*-->")
RE_HEADING_LINE = re.compile(r"^(={1,6})\s+(.+)$", re.MULTILINE)
RE_XREF = re.compile(
    r"(?:xref::?(\S*?)\[[^\]]*\]|<<([^>,\s]+)(?:,[^>]*)?>>)")
RE_RESIDUAL_PH = re.compile(r"\{\{PROTECTED_[A-Za-z0-9_]+_[0-9a-f]{8}\}\}")
RE_URL = re.compile(r"\b(?:https?|ftp)://\S+")
RE_CJK = r"\u4e00-\u9fff"
RE_SPACING = re.compile(
    r"[\u4e00-\u9fff][A-Za-z0-9`]|[A-Za-z0-9`][\u4e00-\u9fff]")
RE_CJK_HALF_PUNCT = re.compile(r"[\u4e00-\u9fff][,.;:!?](?!\d)")
RE_ADJACENCY = re.compile(r"[`*_~]（")
RE_CODE_FENCE = re.compile(r"^----\s*$", re.MULTILINE)
RE_QUOTE_LINE = re.compile(r"^> ")


# 常见繁体独有字（禁繁体机检，覆盖高频误入字符）。
# 注意：只收繁简字形不同、简体不用的字；形同字（行/息/主/境/景/常 等
# 简繁共用字）不得收录，否则简体正文必误报（B01 实测缺陷修复）
TRADITIONAL_CHARS = set(
    "這異們為態軟體語圖難務應當屬實運類連網標誌單億個檔資訊佇設備勢營"
    "環變數執緒質側鏈聲處駐計劃與專門業務據點選項訊佈題關於讓"
)


def load_glossary() -> Dict[str, str]:
    if not GLOSSARY_FILE.exists():
        return {}
    data = yaml.safe_load(GLOSSARY_FILE.read_text(encoding="utf-8")) or {}
    return {t["en"]: t["zh"] for t in data.get("terms", [])
            if t.get("en") and t.get("zh")}


def load_banned() -> List[Dict]:
    if not GLOSSARY_FILE.exists():
        return []
    data = yaml.safe_load(GLOSSARY_FILE.read_text(encoding="utf-8")) or {}
    out = []
    for item in data.get("banned") or []:
        if isinstance(item, str):
            out.append({"bad": item, "prefer": "", "reason": ""})
        elif isinstance(item, dict):
            out.append({"bad": item.get("bad", ""), "prefer":
                        item.get("prefer", ""), "reason":
                        item.get("reason", "")})
    return out


def strip_code(content: str) -> str:
    """剥除代码块/行内码/占位符/URL/引用块行/指令行，供 ③④⑦ 在散文上校验。"""
    lines = content.split("\n")
    out = []
    in_code = False
    for line in lines:
        if line.rstrip() == "----":
            in_code = not in_code
            out.append("")
            continue
        if in_code:
            out.append("")
            continue
        if RE_QUOTE_LINE.match(line):
            out.append("")
            continue
        if RE_DIRECTIVE.match(line):
            # 指令行（include::/snippet::/source:: 等）逐字节同源、受 ② 门禁，
            # 其宏参数（如 io.micronaut.docs.inject.qualifiers.*）不是散文，
            # 不得参与 ③ 术语匹配（B02 实测缺陷修复）
            out.append("")
            continue
        out.append(line)
    text = "\n".join(out)
    text = RE_RESIDUAL_PH.sub(" ", text)
    text = re.sub(r"`[^`\n]+`", " ", text)
    text = RE_URL.sub(" ", text)
    return text


def check_placeholders(zh_text: str, errors: List[str]):
    """① 占位符全部还原。"""
    residue = RE_RESIDUAL_PH.findall(zh_text)
    if residue:
        errors.append(f"① {len(residue)} 处 PROTECTED_ 占位符残留")


def check_code_directives(src_text: str, zh_text: str, errors: List[str]):
    """② 代码块与指令行逐字节一致（multiset）。"""
    import collections
    src_segs = segment_adoc(src_text, "src")
    zh_segs = segment_adoc(zh_text, "zh")
    src_code = sorted(s.content for s in src_segs if s.type == "code_block")
    zh_code = sorted(s.content for s in zh_segs if s.type == "code_block")
    if src_code != zh_code:
        errors.append(f"② 代码块不一致（源 {len(src_code)} / 译 {len(zh_code)}）")
    src_dir_lines = sorted(s.content for s in src_segs
                           if s.type in ("directive", "conditional"))
    zh_dir_lines = sorted(s.content for s in zh_segs
                          if s.type in ("directive", "conditional"))
    if src_dir_lines != zh_dir_lines:
        missing = set(src_dir_lines) - set(zh_dir_lines)
        extra = set(zh_dir_lines) - set(src_dir_lines)
        errors.append(f"② 指令/条件行不一致：缺失 {sorted(missing)[:3]}"
                      f" 多出 {sorted(extra)[:3]}")


def check_terms(src_text: str, zh_text: str, glossary: Dict[str, str],
                banned: List[Dict], errors: List[str]):
    """③ banned 0 命中 + 必译术语命中（散文域）。"""
    src_prose = strip_code(src_text)
    zh_prose = strip_code(zh_text)
    for entry in banned:
        bad = entry.get("bad", "")
        if bad and bad in zh_prose:
            msg = f"③ 禁用译名命中：{bad}"
            if entry.get("prefer"):
                msg += f"（应用 {entry['prefer']}）"
            errors.append(msg)
    for en, zh in glossary.items():
        if en in src_prose and zh not in zh_prose:
            errors.append(f"③ 必译术语缺失：{en} → {zh}")


def check_structure(src_text: str, zh_text: str, errors: List[str]):
    """④ 标题层级数与顺序一致；标题文本已译。"""
    src_h = RE_HEADING_LINE.findall(src_text)
    zh_h = RE_HEADING_LINE.findall(zh_text)
    if len(src_h) != len(zh_h):
        errors.append(f"④ 标题数量不一致：源 {len(src_h)} / 译 {len(zh_h)}")
        return
    for (sl, st), (zl, zt) in zip(src_h, zh_h):
        if len(sl) != len(zl):
            errors.append(f"④ 标题层级不一致：源「{st[:20]}」"
                          f"L{len(sl)} → 译 L{len(zl)}")
        if zt.strip() == st.strip():
            words = [w for w in re.split(r"\s+", st) if re.search(r"[A-Za-z]", w)]
            if len(words) >= 2:
                errors.append(f"④ 标题未翻译：「{st}」")


def load_anchor_registry() -> Dict:
    if not ANCHOR_REGISTRY.exists():
        return {"anchors": []}
    data = yaml.safe_load(ANCHOR_REGISTRY.read_text(encoding="utf-8")) or {}
    return data or {"anchors": []}


def check_xrefs(zh_rel: str, zh_text: str, errors: List[str],
                warnings: List[str]):
    """⑤ xref/锚点目标存在（未译文件豁免）。

    裸锚点（<<anchor,Label>>，无 # 文件前缀）经 anchor-registry 解析
    （check_anchors 全域解析：显式 [[id]] + include 文件 basename 约定）；
    未登记的裸锚点列为豁免警告（M3 断链清零跟踪），不算错误。"""
    registry = load_anchor_registry()
    reg_file = {}
    for a in registry.get("anchors", []):
        if a.get("id") and a.get("id") not in reg_file:
            reg_file[a["id"]] = a.get("file", "")
    for m in RE_XREF.finditer(zh_text):
        target = (m.group(1) or m.group(2) or "").strip()
        if not target:
            continue
        fpart, sep, anchor = target.partition("#")
        fpart = fpart.strip()
        anchor = anchor.strip()
        if fpart.startswith(("http://", "https://", "ftp://", "mailto:")):
            continue
        if not fpart and not anchor:
            continue
        if not fpart:
            # <<#anchor>> 与 <<anchor>> 同为裸锚点，全域经登记表解析
            resolved = reg_file.get(anchor, "")
            if not resolved:
                warnings.append(
                    f"⑤ 裸锚点未登记，豁免（M3 跟踪）：{anchor}")
                continue
            fpart = resolved
        elif not sep and "/" not in fpart and "." not in fpart:
            # 与 check_anchors 同规则：无 # 且不含 / . → 裸锚点
            resolved = reg_file.get(fpart, "")
            if not resolved:
                warnings.append(
                    f"⑤ 裸锚点未登记，豁免（M3 跟踪）：{fpart}")
                continue
            anchor, fpart = fpart, resolved
        elif not sep:
            anchor = ""  # 页级文件引用（含 / 或 .），存在性已验证
        src_file = SOURCE_DIR / fpart if fpart else SOURCE_DIR / zh_rel
        if not src_file.exists():
            errors.append(f"⑤ xref 目标文件不存在于上游：{fpart or zh_rel}")
            continue
        if not anchor:
            continue
        # 目标文件已译 → zh 中须有该锚点（原位注入）；未译 → 豁免。
        # 注：不做 reg_ids 放行——登记表条目恰是被引锚点，放行会使
        # 注入机检恒真（B01 实测缺陷修复，对齐 PLAN §5.6 机检本意）
        zh_target = ZH_DIR / fpart if fpart else ZH_DIR / zh_rel
        if zh_target.exists():
            zt = zh_target.read_text(encoding="utf-8")
            has = (f"[[{anchor}" in zt or f"[#{anchor}]" in zt)
            if not has:
                errors.append(
                    f"⑤ 锚点 {anchor} 在已译目标 {fpart} 的译文中不存在")
        else:
            warnings.append(
                f"⑤ 豁免：目标未译 {fpart}#{anchor}")


def check_provenance(zh_rel: str, zh_text: str, entry: Optional[Dict],
                     baseline: str, errors: List[str]):
    """⑥ 溯源投影四字段齐全且与 manifest 一致。"""
    mo = RE_PROVENANCE.search(zh_text)
    if mo is None:
        errors.append("⑥ 缺溯源注释（upstream_file/upstream_commit/"
                      "upstream_hash/translated_at）")
        return
    f_file, f_commit, f_hash, _f_date = mo.groups()
    if entry is None:
        errors.append("⑥ manifest 无该文件条目")
        return
    if f_file != zh_rel:
        errors.append(f"⑥ upstream_file={f_file!r} != {zh_rel!r}")
    if f_hash != entry.get("blob_sha"):
        errors.append("⑥ upstream_hash 与 manifest blob_sha 不一致")
    expect = entry.get("upstream_commit") or baseline
    if expect and f_commit != expect:
        errors.append("⑥ upstream_commit 与账本不一致")


def strip_blocks(content: str) -> str:
    """剥除逐字块/占位符/引用块行，但保留行内码——供 ⑦ 邻接规则检查。"""
    lines = content.split("\n")
    out = []
    in_code = False
    for line in lines:
        if line.rstrip() == "----":
            in_code = not in_code
            out.append("")
            continue
        if in_code:
            out.append("")
            continue
        if RE_QUOTE_LINE.match(line):
            out.append("")
            continue
        out.append(RE_RESIDUAL_PH.sub(" ", line))
    return "\n".join(out)


def check_style(zh_text: str, errors: List[str]):
    """⑦ 风格机检子集（豁免占位符/代码块/引用块；邻接规则保留行内码检查）。"""
    prose = strip_code(zh_text)
    rawish = strip_blocks(zh_text)
    for i, line in enumerate(prose.split("\n"), 1):
        for m in RE_SPACING.finditer(line):
            errors.append(f"⑦ 中英文之间缺空格（L{i}）：…{m.group(0)}…")
        for m in RE_CJK_HALF_PUNCT.finditer(line):
            errors.append(f"⑦ 中文句使用半角标点（L{i}）：…{m.group(0)}…")
        for ch in line:
            if ch in TRADITIONAL_CHARS:
                errors.append(f"⑦ 疑似繁体字「{ch}」（L{i}）")
                break
    for i, line in enumerate(rawish.split("\n"), 1):
        for m in RE_ADJACENCY.finditer(line):
            errors.append(f"⑦ 标记后紧跟全角开括号（L{i}）：…{m.group(0)}…")


def validate_file(src_path: Path, zh_path: Path, zh_rel: str,
                  glossary: Dict[str, str], banned: List[Dict],
                  entry: Optional[Dict], baseline: str) -> Tuple:
    errors: List[str] = []
    warnings: List[str] = []
    if not src_path.exists():
        errors.append(f"上游源文件不存在：{src_path}")
        return errors, warnings
    if not zh_path.exists():
        errors.append(f"译文不存在：{zh_path}")
        return errors, warnings
    if zh_path.stat().st_size > MAX_ZH_BYTES:
        errors.append(f"译文超过 {MAX_ZH_BYTES}B 硬上限")
        return errors, warnings
    src_text = src_path.read_text(encoding="utf-8")
    zh_text = zh_path.read_text(encoding="utf-8")
    check_placeholders(zh_text, errors)
    check_code_directives(src_text, zh_text, errors)
    check_terms(src_text, zh_text, glossary, banned, errors)
    check_structure(src_text, zh_text, errors)
    check_xrefs(zh_rel, zh_text, errors, warnings)
    check_provenance(zh_rel, zh_text, entry, baseline, errors)
    check_style(zh_text, errors)
    return errors, warnings


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        prog="validate_translation.py",
        description="译文硬门禁校验（七项；退出码 0 全绿 / 1 有错 / 2 环境错误）")
    parser.add_argument("--file", default=None,
                        help="只校验指定文件（相对 source/ 的路径）")
    args = parser.parse_args(argv)

    try:
        if not MANIFEST_FILE.exists():
            print("ERROR: manifest.yml 不存在（先运行 sync --init）",
                  file=sys.stderr)
            return 2
        manifest = yaml.safe_load(MANIFEST_FILE.read_text(encoding="utf-8"))
        entries = {f["file"]: f for f in manifest.get("files", [])}
        baseline = (manifest.get("upstream") or {}).get("baseline_commit", "")
        glossary = load_glossary()
        banned = load_banned()
        print(f"loaded: {len(glossary)} 术语 / {len(banned)} 禁用译名")

        targets = [args.file] if args.file else sorted(entries)
        all_errors, all_warnings = [], []
        validated = 0
        for rel in targets:
            zh_file = ZH_DIR / rel
            if not zh_file.exists():
                continue  # 未译文件不校验（空译文库全量跑仍绿）
            validated += 1
            errs, warns = validate_file(
                SOURCE_DIR / rel, zh_file, rel, glossary, banned,
                entries.get(rel), baseline)
            for e in errs:
                all_errors.append(f"{rel}: {e}")
            for w in warns:
                all_warnings.append(f"{rel}: {w}")

        if all_warnings:
            print(f"WARNINGS ({len(all_warnings)}):")
            for w in all_warnings:
                print(f"  {w}")
        if all_errors:
            print(f"ERRORS ({len(all_errors)}):")
            for e in all_errors:
                print(f"  {e}")
            print(f"validate FAILED: {validated} 文件，{len(all_errors)} 项错误")
            return 1
        print(f"validate PASSED: {validated} 文件全绿")
        return 0
    except (OSError, yaml.YAMLError) as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
