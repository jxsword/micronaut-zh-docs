"""protect_untranslatable 单测：protect/restore 往返、占位符语义、CLI 流程。"""

import json
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS))

from protect_untranslatable import protect, restore, generate_placeholder  # noqa: E402

SCRIPT = str(SCRIPTS / "protect_untranslatable.py")


def run_cli(args):
    """以参数列表调用 CLI（shell=False，无任何 shell 拼接）。"""
    cmd = [sys.executable, SCRIPT]
    for a in args:
        cmd.append(a)
    return subprocess.run(
        cmd, capture_output=True, text=True, check=False, shell=False)


SAMPLE = """:project-version: 5.2.25

[[quickstart]]
= Quick Start

Micronaut lets you run xref:guide/a.adoc#x[linked] code fast.
Use `mvn package` or visit https://micronaut.io/download today.

NOTE: remember to check {project-version} first.

ifdef::env-github[]
This block only shows on GitHub.
endif::[]

----
$ ./gradlew run
----

|===
|Option |Meaning

|`-x` |skip step
|===
"""


def test_roundtrip_identity():
    protected, ph_map = protect(SAMPLE, "s.adoc")
    assert "PROTECTED_" in protected
    restored = restore(protected, ph_map)
    expected = SAMPLE.rstrip("\n")
    assert restored == expected or restored == SAMPLE


def test_code_block_whole_placeholder():
    protected, ph_map = protect(SAMPLE, "s.adoc")
    target = "----\n$ ./gradlew run\n----"
    phs = [k for k, v in ph_map.items() if v == target]
    assert len(phs) == 1
    assert phs[0] in protected
    assert "gradlew" not in protected


def test_conditional_and_attribute_lines():
    protected, ph_map = protect(SAMPLE, "s.adoc")
    assert any(v == "ifdef::env-github[]" for v in ph_map.values())
    assert any(v == "endif::[]" for v in ph_map.values())
    assert any(v == ":project-version: 5.2.25" for v in ph_map.values())
    assert "env-github" not in protected


def test_anchor_line():
    protected, ph_map = protect(SAMPLE, "s.adoc")
    assert any(v == "[[quickstart]]" for v in ph_map.values())


def test_inline_code_and_url():
    protected, ph_map = protect(SAMPLE, "s.adoc")
    values = set(ph_map.values())
    assert "`mvn package`" in values
    assert "https://micronaut.io/download" in values
    assert "micronaut.io/download" not in protected


def test_xref_target_protected_label_kept():
    src = "See xref:target[the page] now.\n"
    protected, ph_map = protect(src, "x.adoc")
    assert "xref:target" in ph_map.values()
    assert "[the page]" in protected
    restored = restore(protected, ph_map)
    assert restored == "See xref:target[the page] now.\n"


def test_attrref_excludes_placeholder_format():
    protected, ph_map = protect("Version {project-version} here.\n", "x.adoc")
    assert "{project-version}" in ph_map.values()
    assert protected.count("PROTECTED_") == protected.count("{{PROTECTED_")


def test_admonition_marker():
    protected, ph_map = protect("NOTE: body text\n", "x.adoc")
    assert "NOTE:" in ph_map.values()
    assert "body text" in protected
    assert not protected.startswith("NOTE")


def test_table_delim_and_cellsep():
    protected, ph_map = protect("|===\n|A |B\n|1 |2\n|===\n", "t.adoc")
    delim = [k for k, v in ph_map.items() if v == "|==="]
    assert len(delim) == 1
    celsep = [k for k, v in ph_map.items() if v == "|"]
    assert len(celsep) == 1
    restored = restore(protected, ph_map)
    assert restored == "|===\n|A |B\n|1 |2\n|===\n"


def test_placeholder_determinism():
    p1, m1 = protect("Use `x` tool.\n", "a.adoc")
    p2, m2 = protect("Use `x` tool.\n", "b.adoc")
    assert p1 == p2
    assert m1 == m2


def test_restore_strict_failures():
    text = "before {{PROTECTED_CODE_0123abcd}} after"
    with pytest.raises(RuntimeError, match="无映射"):
        restore(text, {})
    ph = generate_placeholder("CODE", "`x`")
    with pytest.raises(RuntimeError, match="缺失"):
        restore("translated prose", {ph: "`x`"})
    with pytest.raises(RuntimeError, match="残留"):
        restore("plain " + ph,
                {ph: "x {{PROTECTED_CODE_deadbeef}} nested"})


def test_restore_lenient():
    ph = generate_placeholder("CODE", "`x`")
    out = restore("translated prose only", {ph: "`x`"}, strict=False)
    assert out == "translated prose only"


def test_cli_protect_and_restore(tmp_path):
    src = tmp_path / "guide" / "a.adoc"
    src.parent.mkdir(parents=True)
    src.write_text(SAMPLE, encoding="utf-8")
    outdir = tmp_path / "protect"
    r = run_cli(["--protect", str(src), "--outdir", str(outdir)])
    assert r.returncode == 0, r.stderr
    prot = outdir / "guide" / "a-protected.txt"
    mp = outdir / "guide" / "a-protected-map.json"
    assert prot.exists() and mp.exists()
    translated = prot.read_text(encoding="utf-8").replace(
        "Micronaut lets you run", "Micronaut 让你可以快速运行")
    translated_file = outdir / "guide" / "a-translated.txt"
    translated_file.write_text(translated, encoding="utf-8")
    r2 = run_cli(["--restore", str(translated_file)])
    assert r2.returncode == 0, r2.stderr
    restored = (outdir / "guide" / "a-restored.txt").read_text(encoding="utf-8")
    assert "$ ./gradlew run" in restored
    assert "Micronaut 让你可以快速运行" in restored
    assert "PROTECTED_" not in restored


def test_cli_restore_missing_map(tmp_path):
    f = tmp_path / "x-translated.txt"
    f.write_text("text {{PROTECTED_CODE_0123abcd}}\n", encoding="utf-8")
    r = run_cli(["--restore", str(f)])
    assert r.returncode == 2
    assert "ERROR" in r.stderr


def test_repeated_identical_blocks_idempotent():
    text = "----\nsame\n----\n\npara\n\n----\nsame\n----\n"
    protected, ph_map = protect(text, "r.adoc")
    phs = [k for k, v in ph_map.items() if v == "----\nsame\n----"]
    assert len(phs) == 1
    restored = restore(protected, ph_map)
    expected = text.rstrip("\n")
    assert restored == expected or restored == text


def test_trailing_newline_tolerance():
    protected, ph_map = protect("para\n", "n.adoc")
    restored = restore(protected, ph_map)
    assert restored == "para\n"
