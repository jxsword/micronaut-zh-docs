"""segment_adoc 单测：段型识别、防死循环护栏、规模上限、壳文件判定。"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from segment_adoc import (  # noqa: E402
    MAX_SEGMENTS_PER_FILE,
    Segment,
    compute_hash,
    is_shell_file,
    segment_adoc,
)


def types_of(content, name="t.adoc"):
    return [s.type for s in segment_adoc(content, name)]


def test_heading_levels_and_ids():
    segs = segment_adoc("= Top\n\n== Second\n\n=== Third\n", "g/x.adoc")
    assert [s.type for s in segs] == ["heading", "heading", "heading"]
    assert [s.metadata["level"] for s in segs] == [1, 2, 3]
    assert segs[0].id == "g/x.adoc-heading-0"
    assert segs[0].metadata["title"] == "Top"
    assert segs[0].hash == compute_hash("= Top")


def test_paragraph_and_hash():
    text = "first para line1\nline2\n\nsecond para\n"
    segs = segment_adoc(text, "a.adoc")
    assert [s.type for s in segs] == ["paragraph", "paragraph"]
    assert segs[0].content == "first para line1\nline2"
    assert segs[0].line_start == 1 and segs[0].line_end == 2
    assert segs[1].hash == compute_hash("second para")


def test_listing_block_verbatim():
    text = "para\n\n----\nint x = 1;\n----\n\nafter\n"
    segs = segment_adoc(text, "a.adoc")
    assert [s.type for s in segs] == ["paragraph", "code_block", "paragraph"]
    assert segs[1].content == "----\nint x = 1;\n----"


def test_literal_and_passthrough_blocks():
    text = "....\nliteral\n....\n\n++++\npass\n++++\n"
    assert types_of(text) == ["code_block", "code_block"]


def test_unclosed_block_consumes_to_eof():
    text = "----\nunclosed code"
    segs = segment_adoc(text, "a.adoc")
    assert len(segs) == 1 and segs[0].type == "code_block"
    assert segs[0].content == "----\nunclosed code"


def test_table_block():
    text = "|===\n|A |B\n|1 |2\n|===\n\npara\n"
    segs = segment_adoc(text, "a.adoc")
    assert [s.type for s in segs] == ["table", "paragraph"]
    assert "|===" in segs[0].content and "|2" in segs[0].content


def test_transparent_delimiters():
    text = "====\nexample prose\n====\n\npara\n"
    segs = segment_adoc(text, "a.adoc")
    assert [s.type for s in segs] == ["block_delimiter", "paragraph",
                                      "block_delimiter", "paragraph"]


def test_directive_and_conditional_lines():
    text = ("include::intro.adoc[]\n"
            "ifdef::env-github[]\n"
            "visible text\n"
            "endif::[]\n")
    segs = segment_adoc(text, "a.adoc")
    assert [s.type for s in segs] == ["directive", "conditional", "paragraph",
                                      "conditional"]
    assert segs[0].metadata["target"] == "intro.adoc"


def test_anchor_lines():
    text = "[[configuration]]\n\n== Configuration\n\n[#options]\npara\n"
    segs = segment_adoc(text, "a.adoc")
    assert [s.type for s in segs] == ["anchor", "heading", "anchor", "paragraph"]
    assert segs[0].metadata["anchor_id"] == "configuration"
    assert segs[2].metadata["anchor_id"] == "options"


def test_attribute_definitions():
    text = ":project-version: 5.2.25\n:nocontext:\n\npara\n"
    segs = segment_adoc(text, "a.adoc")
    assert [s.type for s in segs] == ["attribute", "attribute", "paragraph"]
    assert segs[0].metadata["name"] == "project-version"


def test_block_attributes():
    text = "[source,java]\n----\ncode\n----\n\n[cols=\"1,2\"]\n|===\n|a\n|===\n"
    segs = segment_adoc(text, "a.adoc")
    assert [s.type for s in segs] == ["attribute", "code_block", "attribute",
                                      "table"]


def test_admonition():
    text = "NOTE: this is a note\nspanning lines.\n\nTIP: tip body\n"
    segs = segment_adoc(text, "a.adoc")
    assert [s.type for s in segs] == ["admonition", "admonition"]
    assert "spanning lines" in segs[0].content


def test_inline_anchor_and_xref_stay_in_paragraph():
    text = "See xref:guide/a.adoc#anchor[the page] and `inline code`.\n"
    segs = segment_adoc(text, "a.adoc")
    assert [s.type for s in segs] == ["paragraph"]
    assert "xref:guide/a.adoc#anchor[the page]" in segs[0].content


def test_paragraph_breaks_on_special_line():
    text = "para one\n== Heading\npara two\n"
    assert types_of(text) == ["paragraph", "heading", "paragraph"]


def test_no_dead_loop_on_degenerate_input():
    # 残缺行/空段护栏：任何输入都必须终止（2026-11-18 OOM 回归）
    for degenerate in ["|", "----", "====", "[", ":", "....", ".x", "--",
                       "[[", "ifdef::", "NOTE:", "=", "+++"]:
        segs = segment_adoc(degenerate, "d.adoc")  # 不抛异常即通过
        assert len(segs) <= 2


def test_max_segments_hard_limit():
    content = "\n\n".join(f"para {n}" for n in range(600))
    segs = segment_adoc(content, "big.adoc")  # 600 段 < 上限，正常
    assert len(segs) == 600
    # 直接验证上限常量语义（触发分支经 patch 计数验证代价高，常量与实现
    # 位于同一模块，50k 触发路径由 pytest 覆盖在段数断言内）
    assert MAX_SEGMENTS_PER_FILE == 50_000
    with pytest.MonkeyPatch.context() as mp:
        import segment_adoc as sa
        mp.setattr(sa, "MAX_SEGMENTS_PER_FILE", 5)
        with pytest.raises(RuntimeError, match="硬上限"):
            sa.segment_adoc("a\n\nb\n\nc\n\nd\n\ne\n\nf\n\ng", "x.adoc")


def test_is_shell_file():
    shell = "include::aop/intro.adoc[]\ninclude::aop/body.adoc[]\n"
    assert is_shell_file(segment_adoc(shell, "s.adoc"))
    assert not is_shell_file(segment_adoc("= Title\n\ninclude::x[]\n", "s.adoc"))
    assert not is_shell_file(segment_adoc("", "s.adoc"))
    assert not is_shell_file(segment_adoc("= Title\n\npara\n", "s.adoc"))


def test_translation_flag_partition():
    segs = segment_adoc("= H\n\npara\n\n----\ncode\n----\n\n[[x]]\n",
                        "t.adoc")
    for s in segs:
        assert s.translatable == (s.type in {"heading", "paragraph",
                                             "admonition", "table"})


def test_snippet_directive_recognized():
    # snippet:: 是构建期代码注入宏，必须按指令行保护（B01 实测补录）
    segs = segment_adoc(
        'para\n\nsnippet::io.micronaut.docs.Foo[tags="imports,class"]\n\npara2\n',
        "t.adoc")
    kinds = [s.type for s in segs]
    assert segs[1].type == "directive"
    assert "directive" in kinds
