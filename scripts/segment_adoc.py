#!/usr/bin/env python3
"""Asciidoc 语义分段器（自 spdlog-zh-docs segment_markdown.py 适配 .adoc）。

段落 id `{file}-{type}-{index}`、hash=sha256[:16]，是增量同步（sync_upstream.py
段落级三方比对）与批次词数统计的共同基础。

加固要点（家族 2026-11-18 OOM 事故复盘，移植自 fmt/spdlog 加固版）：
  1. 段落分支末尾 `if i == start: i += 1` 防死循环护栏——任何未推进情形强制前进；
  2. 无递归解析：块定界符（---- / .... / ++++ 等）按"开到匹配闭"平铺消费，
     嵌套块不递归；example/sidebar/quote/open 定界符视为透明（1 行段）；
  3. 单文件段数硬上限 MAX_SEGMENTS_PER_FILE，超限报错退出。

段类型（translatable 标记译否）：
  heading        =/= 一级~六级标题（可译，validate ④ 结构对齐对象）
  paragraph      普通散文段落（可译）
  admonition     NOTE:/TIP:/… 提示段（可译，标记经 protect 保留）
  table          |=== … |=== 表格块（单元格可译，分隔符经 protect 保留）
  code_block     ---- / .... / ++++ 定界的逐字块（不可译，validate ② 逐字节比对）
  directive      行级宏：include::/xref::/image::/source::/toc::/pass::（不可译）
  conditional    ifdef::/ifndef::/ifeval::/endif:: 行（不可译）
  attribute      :name: value 属性定义行 / [block attribute] 行（不可译）
  anchor         [[id]] / [#id] 锚点行（不可译；译文中允许按 registry 原位注入）
  block_delimiter ==== / **** / ____ / -- 等透明定界行（不可译）
"""

import hashlib
from dataclasses import dataclass, field
from typing import Dict, List

MAX_SEGMENTS_PER_FILE = 50_000   # 单文件段数硬上限（PLAN §9 风险 4）

import re

# ---------- 行分类正则（顺序即优先级） ----------

RE_TABLE_DELIM = re.compile(r"^\|===\s*$")
RE_LISTING = re.compile(r"^-{4,}\s*$")          # ---- 列表块（verbatim）
RE_LITERAL = re.compile(r"^\.{4,}\s*$")         # .... literal 块（verbatim）
RE_PASSTHROUGH = re.compile(r"^\+{4,}\s*$")     # ++++ passthrough 块（verbatim）
RE_SIDEBAR = re.compile(r"^\*{4,}\s*$")
RE_QUOTE = re.compile(r"^_{4,}\s*$")
RE_EXAMPLE = re.compile(r"^={4,}\s*$")
RE_OPEN_BLOCK = re.compile(r"^--\s*$")
RE_HEADING = re.compile(r"^(={1,6})\s+\S")
RE_ANCHOR = re.compile(r"^\[\[([^\]]+)\]\]\s*$")            # [[id]] / [[id,reftext]]
RE_BLOCK_ID = re.compile(r"^\[#([^\s\]]+)\]\s*$")           # [#id] shorthand
RE_ATTRDEF = re.compile(r"^:([\w\-\.@]+):\s*(.*)$")
RE_BLOCK_ATTR = re.compile(r"^\[(?!\[)[^\]]+\]\s*$")        # [source,java] / [cols=".."]
RE_CONDITIONAL = re.compile(r"^(ifdef|ifndef|ifeval|endif)::\S*\s*$")
RE_DIRECTIVE = re.compile(
    r"^(include\d*|xref|image|source|toc|pass|link|video|audio)::"
    r"(\S*?)\[[^\]]*\]\s*$")
RE_ADMONITION = re.compile(r"^(NOTE|TIP|IMPORTANT|WARNING|CAUTION):\s+\S")

# 段落续行禁止开始（这些行型必须自成一段）
_SPECIAL_STARTS = ("|===", "----", "....", "++++", "****", "____", "===", "--")

# 不可译段型（protect/validate/词数统计共用）
NON_TRANSLATABLE = frozenset({
    "code_block", "directive", "conditional", "attribute",
    "anchor", "block_delimiter",
})
TRANSLATABLE = frozenset({"heading", "paragraph", "admonition", "table"})


@dataclass
class Segment:
    """分段：id 为 `{file}-{type}-{index}`（index 为文件内全局序号）。"""
    id: str
    type: str
    content: str
    hash: str
    file_path: str
    line_start: int
    line_end: int
    metadata: Dict = field(default_factory=dict)

    @property
    def translatable(self) -> bool:
        return self.type in TRANSLATABLE


def compute_hash(content: str) -> str:
    return hashlib.sha256(content.encode("utf-8")).hexdigest()[:16]


def segment_adoc(content: str, fname: str) -> List[Segment]:
    """行扫描分段 asciidoc 文本；fname 用于段落 id 与报错。"""
    segs: List[Segment] = []
    lines = content.split("\n")
    i = 0
    idx = 0
    cur_sec = ""
    while i < len(lines):
        line = lines[i]
        st = line.rstrip()

        if st == "":
            i += 1
            continue

        # --- 逐字块：---- .... ++++ （开到匹配闭，整块不可译） ---
        m = (RE_LISTING.match(st) or RE_LITERAL.match(st)
             or RE_PASSTHROUGH.match(st))
        if m:
            closer = re.compile(m.group(0).strip().replace(".", r"\.")
                                .replace("+", r"\+").replace("-", r"-")
                                + r"\s*$")
            start = i
            i += 1
            while i < len(lines) and not closer.match(lines[i].rstrip()):
                i += 1
            if i < len(lines):
                i += 1  # 消费闭合定界行
            body = "\n".join(lines[start:i])
            segs.append(Segment(f"{fname}-code_block-{idx}", "code_block", body,
                                compute_hash(body), fname, start + 1, i))
            idx += 1
            continue

        # --- 表格块：|=== … |=== ---
        if RE_TABLE_DELIM.match(st):
            start = i
            i += 1
            while i < len(lines) and not RE_TABLE_DELIM.match(lines[i].rstrip()):
                i += 1
            if i < len(lines):
                i += 1  # 消费闭合 |===
            tbl = "\n".join(lines[start:i])
            segs.append(Segment(f"{fname}-table-{idx}", "table", tbl,
                                compute_hash(tbl), fname, start + 1, i))
            idx += 1
            continue

        # --- 透明定界行（example/sidebar/quote/open block） ---
        if (RE_EXAMPLE.match(st) or RE_SIDEBAR.match(st) or RE_QUOTE.match(st)
                or RE_OPEN_BLOCK.match(st)):
            segs.append(Segment(f"{fname}-block_delimiter-{idx}",
                                "block_delimiter", line, compute_hash(line),
                                fname, i + 1, i + 1))
            idx += 1
            i += 1
            continue

        # --- 标题 ---
        mh = RE_HEADING.match(st)
        if mh:
            level = len(mh.group(1))
            title = st[len(mh.group(1)):].strip()
            segs.append(Segment(f"{fname}-heading-{idx}", "heading", line,
                                compute_hash(line), fname, i + 1, i + 1,
                                {"level": level, "title": title}))
            cur_sec = title
            idx += 1
            i += 1
            continue

        # --- 锚点 / 属性 / 条件 / 指令（行级，不可译） ---
        if RE_ANCHOR.match(st):
            ids = st.strip()[2:-2]  # 去掉 [[ ]]
            anchor_id = ids.split(",", 1)[0].strip()
            segs.append(Segment(f"{fname}-anchor-{idx}", "anchor", line,
                                compute_hash(line), fname, i + 1, i + 1,
                                {"anchor_id": anchor_id}))
            idx += 1
            i += 1
            continue
        if RE_BLOCK_ID.match(st):
            segs.append(Segment(
                f"{fname}-anchor-{idx}", "anchor", line, compute_hash(line),
                fname, i + 1, i + 1,
                {"anchor_id": RE_BLOCK_ID.match(st).group(1)}))
            idx += 1
            i += 1
            continue
        if RE_ATTRDEF.match(st):
            segs.append(Segment(
                f"{fname}-attribute-{idx}", "attribute", line,
                compute_hash(line), fname, i + 1, i + 1,
                {"name": RE_ATTRDEF.match(st).group(1)}))
            idx += 1
            i += 1
            continue
        if RE_BLOCK_ATTR.match(st):
            segs.append(Segment(f"{fname}-attribute-{idx}", "attribute", line,
                                compute_hash(line), fname, i + 1, i + 1))
            idx += 1
            i += 1
            continue
        if RE_CONDITIONAL.match(st):
            segs.append(Segment(f"{fname}-conditional-{idx}", "conditional",
                                line, compute_hash(line), fname, i + 1, i + 1))
            idx += 1
            i += 1
            continue
        if RE_DIRECTIVE.match(st):
            segs.append(Segment(
                f"{fname}-directive-{idx}", "directive", line,
                compute_hash(line), fname, i + 1, i + 1,
                {"target": RE_DIRECTIVE.match(st).group(2)}))
            idx += 1
            i += 1
            continue

        # --- 提示段（NOTE: 等，标记不可译、正文可译） ---
        if RE_ADMONITION.match(st):
            start = i
            i += 1
            while i < len(lines) and lines[i].strip() != "":
                ls = lines[i].strip()
                if i > start and (ls.startswith("|===") or ls.startswith("----")
                                  or ls.startswith("....")
                                  or ls.startswith("++++")
                                  or RE_HEADING.match(ls)
                                  or RE_CONDITIONAL.match(ls)
                                  or RE_ANCHOR.match(ls)
                                  or RE_BLOCK_ID.match(ls)
                                  or RE_ATTRDEF.match(ls)
                                  or RE_BLOCK_ATTR.match(ls)
                                  or RE_DIRECTIVE.match(ls)):
                    break
                i += 1
            body = "\n".join(lines[start:i])
            segs.append(Segment(f"{fname}-admonition-{idx}", "admonition", body,
                                compute_hash(body), fname, start + 1, i,
                                {"section": cur_sec}))
            idx += 1
            if i == start:
                i += 1  # 防死循环护栏
            continue

        # --- 普通段落 ---
        start = i
        i += 1  # 首行已消费（st 非空）
        while i < len(lines):
            ls = lines[i].strip()
            if ls == "":
                break
            if i > start and (ls.startswith(_SPECIAL_STARTS)
                              or RE_HEADING.match(ls)
                              or RE_ANCHOR.match(ls)
                              or RE_BLOCK_ID.match(ls)
                              or RE_ATTRDEF.match(ls)
                              or RE_BLOCK_ATTR.match(ls)
                              or RE_CONDITIONAL.match(ls)
                              or RE_DIRECTIVE.match(ls)
                              or RE_ADMONITION.match(ls)):
                break
            i += 1
        body = "\n".join(lines[start:i])
        segs.append(Segment(f"{fname}-paragraph-{idx}", "paragraph", body,
                            compute_hash(body), fname, start + 1, i,
                            {"section": cur_sec}))
        idx += 1
        if i == start:
            # 防死循环护栏（2026-11-18 OOM 事故根因）：内层未推进时强制前进
            i += 1

        if len(segs) > MAX_SEGMENTS_PER_FILE:
            raise RuntimeError(
                f"{fname}: 段数超过硬上限 {MAX_SEGMENTS_PER_FILE}（报错退出）")
    return segs


def is_shell_file(segments: List[Segment]) -> bool:
    """纯 include 壳判定：无任何可译段且至少含一个 include 指令。

    0 字节文件由调用方判定（segments 为空时本函数返回 False，避免把
    「空段」误判为壳——空文件在 sync 中单独标 skipped）。"""
    has_include = any(s.type == "directive" and s.metadata.get("target", "")
                      for s in segments)
    return has_include and not any(s.translatable for s in segments)
