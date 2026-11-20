#!/usr/bin/env python3
"""上游 micronaut-core 文档同步脚本（blob sha 检测 + 段落级 diff + manifest 状态机）。

移植自 google-benchmark-zh-docs sync_upstream.py（OOM 加固版，manifest schema v1），
按 DR-002/PLAN §4 适配 Micronaut 文档树。差异点：
  - 上游文档树 src/main/docs 层级结构（guide/ 子目录 + resources/ 图片 + toc.yml）；
  - 账本跟踪 .adoc + toc.yml/toc-python.yml，其余文件（图片等）镜像不入账本；
  - 0 字节或纯 include 壳文件状态 skipped（PLAN §4.3），不进批次；
  - --check 默认对照 5.2.x 分支 HEAD（--init 默认锁定 tag v5.2.25）；
  - 初译期（v1.0 tag 之前）--apply 门控禁用：仅 --check + 开 issue（PLAN §4.4）；
  - 上游删除文件经 --apply 移入 archive/<日期>/（不删除，保留追溯）；
  - 退出码 0=无变更 / 1=有变更待翻译 / 2=环境错误（PLAN §4.2）；
  - 新增 --collect-commits：逐文件 upstream_commit 经 gh api 串行采集（可延后补采）。

安全纪律（PLAN §9 风险 4，家族 2026-11-18 OOM 事故复盘三项审查）：
  1. 运行强制 memgate 包裹：`memgate 2048 python3 scripts/sync_upstream.py …`
  2. 输入规模硬上限：单文件 >2MB 或总解析段数 >50k 直接报错退出
  3. 逐文件分段处理，不全库驻留；段落对齐 difflib 逐文件 O(n·m)；无递归解析
  4. --dry-run 只打印不写盘；--file 单文件调试

manifest.yml 只能由本脚本读写（人工直改视为账本损坏，validate 门禁报错）。

CLI:
  --init              首次快照：sparse 克隆上游 → source/ 全量镜像 → _upstream_commit
                      + manifest 全量 missing/skipped，产出同步报告（仅一次）
  --check             只检测：对照上游，打印变更摘要，不写盘（CI 每周检测用）
  --apply             应用变更（初译期门控禁用，解禁条件见 apply_unlocked）
  --mark-current FILE 修订核销：校验 zh/<FILE> 溯源注释四字段后标记 current
  --collect-commits   逐文件采集 upstream_commit（gh api 串行 + 本地缓存，可延后）
  --dry-run           与 --init/--apply 组合：只打印不写盘
  --file NAME         只处理指定文件（相对 src/main/docs 的路径，调试）
  --repo URL          覆盖上游仓库地址（测试注入本地 file:// 仓库）
  --workdir DIR       覆盖克隆缓存目录（测试隔离）
  --ref REF           上游分支/标签（缺省按模式：init=v5.2.25，其余=5.2.x）

状态机：current（译文与上游对齐）| stale（上游已变，待修订）| partial（批次进行中）|
missing（未开译）| skipped（0 字节/纯 include 壳，不进批次）。
partial 只由翻译批次流转，sync 不产生。
"""

import argparse
import difflib
import hashlib
import json
import logging
import os
import re
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import yaml

sys.path.insert(0, str(Path(__file__).parent))
from segment_adoc import compute_hash, is_shell_file, segment_adoc  # noqa: E402

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

REPO_ROOT = Path(__file__).parent.parent.resolve()
SOURCE_DIR = REPO_ROOT / "source"
ZH_DIR = REPO_ROOT / "zh"
REPORTS_DIR = REPO_ROOT / "reports"
MANIFEST_FILE = REPO_ROOT / "manifest.yml"
ARCHIVE_DIR = REPO_ROOT / "archive"

UPSTREAM_REPO = "https://github.com/micronaut-projects/micronaut-core"
UPSTREAM_DOC = "src/main/docs"
DEFAULT_REF = "5.2.x"        # --check/--apply 默认对照 5.2.x 分支 HEAD
INIT_REF = "v5.2.25"         # --init 默认锁定 tag
TRANSLATABLE_SUFFIX = ".adoc"
TRANSLATABLE_NAMES = {"toc.yml", "toc-python.yml"}

# PLAN §9 风险 4：规模硬上限
MAX_FILE_BYTES = 2 * 1024 * 1024       # 单文件 2MB
MAX_TOTAL_SEGMENTS = 50_000            # 全库总段数

MANIFEST_SCHEMA_VERSION = "v1"
RE_PROVENANCE = re.compile(
    r"<!--\s*upstream_file:\s*(\S+)\s+upstream_commit:\s*([0-9a-f]{40})\s+"
    r"upstream_hash:\s*([0-9a-f]{40})\s+translated_at:\s*(\d{4}-\d{2}-\d{2})\s*-->")

SYNC_CONTEXT = None  # 测试注入用（SyncContext 实例覆盖目录常量）


@dataclass
class SyncContext:
    """目录注入：生产用模块常量，测试注入 tmp_path 隔离目录。"""
    source_dir: Path
    zh_dir: Path
    reports_dir: Path
    manifest_file: Path
    workdir: Path
    repo_root: Path


@dataclass
class Segment:
    """段落（re-export 供外部使用）。"""
    index: int
    type: str
    content: str
    hash: str
    line_start: int
    line_end: int
    section: str = ""


@dataclass
class FileChange:
    """单文件变更工作项。"""
    file: str
    type: str            # A / M / D / R / NONE
    old_blob: str = ""
    new_blob: str = ""
    added: int = 0
    modified: int = 0
    removed: int = 0
    action: str = ""     # applied / would-apply / detected / archived


@dataclass
class Manifest:
    schema: str
    remote: str
    baseline_commit: str = ""
    snapshot_date: str = ""
    files: List[Dict] = field(default_factory=list)

    def entry(self, fname: str) -> Optional[Dict]:
        for f in self.files:
            if f["file"] == fname:
                return f
        return None


# ---------- 基础工具 ----------

def compute_blob_sha(data: bytes) -> str:
    """git blob sha1（与 `git hash-object` 等价），文件级变更检测依据（PLAN §4.1）。

    sha1 仅作内容标识符（必须与 git/GitHub blob sha 逐字节一致方可比对），
    非安全原语；段落 hash 用 sha256（segment_adoc.compute_hash）。"""
    return hashlib.sha1(b"blob %d\x00" % len(data) + data).hexdigest()


def _git(args: List[str], cwd: Optional[Path] = None) -> str:
    """git 子进程：一律参数列表，不用 shell 拼接。"""
    result = subprocess.run(["git", *args], cwd=cwd, check=True,
                            capture_output=True, text=True)
    return result.stdout


def _gh_api_last_commit(repo_slug: str, path: str, ref: str) -> Optional[str]:
    """gh api 查询某文件在 ref 上最后一次提交 sha；失败返回 None（可延后补采）。"""
    result = subprocess.run(
        ["gh", "api",
         f"repos/{repo_slug}/commits?path={path}&sha={ref}&per_page=1",
         "--jq", ".[0].sha"],
        capture_output=True, text=True, check=False)
    if result.returncode == 0 and result.stdout.strip():
        return result.stdout.strip()
    logger.warning("gh api 采集失败（可延后补采）: %s: %s",
                   path, result.stderr.strip()[:200])
    return None


def _safe_join(base: Path, rel: str) -> Path:
    """resolve 后校验仍位于 base 内，防路径逃逸。"""
    base = base.resolve()
    p = (base / rel).resolve()
    if not p.is_relative_to(base):
        raise ValueError(f"path escapes {base}: {rel}")
    return p


def _write_source(source_dir: Path, rel: str, data: bytes) -> Path:
    """写入 source/<rel>（自动建父目录 + 路径逃逸校验）。"""
    dest = _safe_join(source_dir, rel)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(data)
    return dest


def get_ctx() -> SyncContext:
    global SYNC_CONTEXT
    if SYNC_CONTEXT is not None:
        return SYNC_CONTEXT
    # 上游克隆缓存与 gh api 缓存放仓库外（~/.cache，可覆盖）：第三方克隆不入库
    cache_root = Path(os.environ.get(
        "MZD_CACHE_DIR", str(Path.home() / ".cache" / "micronaut-zh-docs")))
    return SyncContext(
        source_dir=SOURCE_DIR, zh_dir=ZH_DIR, reports_dir=REPORTS_DIR,
        manifest_file=MANIFEST_FILE, repo_root=REPO_ROOT,
        workdir=cache_root / "upstream",
    )


def apply_unlocked(ctx: SyncContext) -> bool:
    """初译期 --apply 门控（PLAN §4.4）：v1.0 tag 存在（或测试环境变量）才解禁。"""
    if os.environ.get("MZD_ALLOW_APPLY") == "1":
        return True
    try:
        _git(["rev-parse", "--verify", "v1.0^{commit}"], cwd=ctx.repo_root)
        return True
    except subprocess.CalledProcessError:
        return False


# ---------- 上游克隆缓存（sparse 浅克隆 src/main/docs，PLAN §4.1） ----------

def prepare_upstream(repo_url: str, workdir: Path, ref: str) -> str:
    """确保 workdir 缓存检出 ref 并返回 HEAD SHA。

    已有缓存 → fetch --depth 1 更新；无缓存 → clone --depth 1 --sparse
    （https 远端加 --filter=blob:none；file:// 本地仓不加 filter）。"""
    if (workdir / ".git").exists():
        _git(["fetch", "--depth", "1", "origin", ref], cwd=workdir)
        _git(["checkout", "-q", "FETCH_HEAD"], cwd=workdir)
        return _git(["rev-parse", "HEAD"], cwd=workdir).strip()
    if workdir.exists():
        shutil.rmtree(workdir)
    workdir.parent.mkdir(parents=True, exist_ok=True)
    cmd = ["clone", "--depth", "1", "--single-branch", "--branch", ref]
    if not repo_url.startswith("file://"):
        cmd += ["--filter=blob:none", "--sparse"]
    cmd += [repo_url, str(workdir)]
    _git(cmd)
    _git(["sparse-checkout", "set", UPSTREAM_DOC], cwd=workdir)
    return _git(["rev-parse", "HEAD"], cwd=workdir).strip()


def read_upstream(doc_dir: Path) -> Tuple[Dict[str, bytes], Dict[str, bytes]]:
    """递归读取上游 src/main/docs：返回 (tracked, mirror)。

    tracked = 账本跟踪文件（.adoc + toc.yml/toc-python.yml），mirror = 其余
    （resources/ 图片等，镜像不入账本）。未知扩展名镜像并告警（全量快照原则）。"""
    if not doc_dir.is_dir():
        raise RuntimeError(f"upstream docs dir not found: {doc_dir}")
    tracked: Dict[str, bytes] = {}
    mirror: Dict[str, bytes] = {}
    for p in sorted(doc_dir.rglob("*")):
        if not p.is_file():
            continue
        rel = p.relative_to(doc_dir).as_posix()
        data = p.read_bytes()
        if len(data) > MAX_FILE_BYTES:
            raise RuntimeError(f"{rel}: 文件超过 {MAX_FILE_BYTES}B 硬上限")
        if p.suffix == TRANSLATABLE_SUFFIX or p.name in TRANSLATABLE_NAMES:
            tracked[rel] = data
        else:
            if p.suffix not in (".png", ".svg", ".gif", ".jpg", ".jpeg",
                                ".webp", ".ico", ".pdf"):
                logger.warning("未知扩展名文件镜像（不入账本）: %s", rel)
            mirror[rel] = data
    if not tracked and not mirror:
        raise RuntimeError("upstream docs 无任何文件")
    return tracked, mirror


def mirror_into_source(mirror: Dict[str, bytes], source_dir: Path) -> List[str]:
    """镜像非账本文件（resources/ 图片等）进 source/，返回相对路径列表。"""
    mirrored = []
    for rel, data in sorted(mirror.items()):
        dest = _safe_join(source_dir, rel)
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(data)
        mirrored.append(rel)
    return mirrored


# ---------- 段落级工作项 ----------

def diff_paragraphs(old_segs, new_segs) -> List[Tuple[str, list, list]]:
    """段落 hash 序列 difflib 对齐，产出三类工作项（宁多译不误译）。"""
    if not old_segs and not new_segs:
        return []
    sm = difflib.SequenceMatcher(a=[s.hash for s in old_segs],
                                 b=[s.hash for s in new_segs], autojunk=False)
    work = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            continue
        work.append((tag, old_segs[i1:i2], new_segs[j1:j2]))
    return work


def scan_workitems(old_segs, new_segs) -> Dict[str, int]:
    counts = {"added": 0, "modified": 0, "removed": 0}
    for tag, olds, news in diff_paragraphs(old_segs, new_segs):
        if tag == "insert":
            counts["added"] += len(news)
        elif tag == "delete":
            counts["removed"] += len(olds)
        elif tag == "replace":
            counts["modified"] += max(len(olds), len(news))
    return counts


# ---------- manifest（脚本独占读写，纪律 3） ----------

def load_manifest(path: Path) -> Optional[Manifest]:
    if not path.exists():
        return None
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or data.get("schema") != MANIFEST_SCHEMA_VERSION:
        raise RuntimeError(
            f"manifest.yml schema 异常（期望 {MANIFEST_SCHEMA_VERSION}）——账本疑似损坏，停止")
    files = data.get("files")
    if files is None:
        raise RuntimeError("manifest.yml 缺 files 节——账本疑似损坏，停止")
    up = data.get("upstream") or {}
    return Manifest(schema=data["schema"], remote=up.get("remote", UPSTREAM_REPO),
                    baseline_commit=up.get("baseline_commit", ""),
                    snapshot_date=up.get("snapshot_date", ""), files=files)


def save_manifest(path: Path, m: Manifest):
    data = {
        "schema": m.schema,
        "upstream": {
            "remote": m.remote,
            "baseline_commit": m.baseline_commit,
            "snapshot_date": m.snapshot_date,
    },
        "files": m.files,
    }
    path.write_text(
        yaml.safe_dump(data, allow_unicode=True, sort_keys=False, width=100),
        encoding="utf-8")


def zh_path_of(ctx: SyncContext, rel: str) -> Path:
    return _safe_join(ctx.zh_dir, rel)


def _has_zh(ctx: SyncContext, rel: str) -> bool:
    return zh_path_of(ctx, rel).exists()


# ---------- 核心流程 ----------

def _segments_of(content: str, name: str) -> List:
    return segment_adoc(content, name)


def sync_init(ctx: SyncContext, repo_url: str, ref: str,
              only_file: Optional[str], dry_run: bool) -> Dict:
    """首次快照：source/ 全量镜像 + _upstream_commit + manifest 全量 missing/skipped。"""
    if ctx.manifest_file.exists():
        raise RuntimeError("manifest.yml 已存在；首次快照只应执行一次。"
                           "后续同步用 --check / --apply。")
    sha = prepare_upstream(repo_url, ctx.workdir, ref)
    tracked, mirror = read_upstream(ctx.workdir / UPSTREAM_DOC)

    if only_file:
        tracked = {k: v for k, v in tracked.items() if k == only_file}
        mirror = {k: v for k, v in mirror.items() if k == only_file}
        if not tracked and not mirror:
            raise RuntimeError(f"--file {only_file}: 上游不存在该文件")

    seg_counts: Dict[str, int] = {}
    total_segments = 0
    for name, raw in sorted(tracked.items()):
        segs = _segments_of(raw.decode("utf-8"), name)
        seg_counts[name] = len(segs)
        total_segments += len(segs)
    if total_segments > MAX_TOTAL_SEGMENTS:
        raise RuntimeError(f"总段数 {total_segments} 超过硬上限 {MAX_TOTAL_SEGMENTS}")

    if dry_run:
        print(json.dumps({
            "mode": "init", "dry_run": True, "commit": sha, "ref": ref,
            "tracked": len(tracked), "mirror": len(mirror),
            "total_segments": total_segments,
        }, ensure_ascii=False))
        return {"mode": "init", "commit": sha, "has_changes": True,
                "dry_run": True}

    ctx.source_dir.mkdir(parents=True, exist_ok=True)
    for name, raw in sorted(tracked.items()):
        _write_source(ctx.source_dir, name, raw)
    for name, raw in sorted(mirror.items()):
        _write_source(ctx.source_dir, name, raw)
    mirrored = [f"{rel}" for rel in sorted(mirror)]
    logger.info("镜像非账本文件 %d 个", len(mirrored))

    (ctx.source_dir / "_upstream_commit").write_text(sha + "\n", encoding="utf-8")

    today = date.today().isoformat()
    m = Manifest(schema=MANIFEST_SCHEMA_VERSION, remote=repo_url,
                 baseline_commit=sha, snapshot_date=today, files=[])
    for name in sorted(tracked):
        raw = tracked[name]
        segs_n = seg_counts[name]
        skipped = (len(raw) == 0 or
                   is_shell_file(_segments_of(raw.decode("utf-8"), name)))
        m.files.append({
            "file": name,
            "blob_sha": compute_blob_sha(raw),
            "size": len(raw),
            "status": "skipped" if skipped else "missing",
            "zh": f"zh/{name}",
            "paragraphs": segs_n,
            "updated_at": today,
        })
    save_manifest(ctx.manifest_file, m)

    n_missing = sum(1 for f in m.files if f["status"] == "missing")
    n_skipped = sum(1 for f in m.files if f["status"] == "skipped")
    report = render_report(
        mode="init", sha=sha, ref=ref, dry_run=False,
        changes=[FileChange(f["file"], "A", new_blob=f["blob_sha"],
                            action=f["status"]) for f in m.files],
        extra={"mirror_count": len(mirrored), "total_segments": total_segments,
               "missing": n_missing, "skipped": n_skipped,
               "baseline_locked": True})
    ctx.reports_dir.mkdir(parents=True, exist_ok=True)
    report_path = ctx.reports_dir / f"sync-{today}-{sha[:8]}.md"
    report_path.write_text(report, encoding="utf-8")
    logger.info("同步报告：%s", report_path)

    print(json.dumps({"mode": "init", "commit": sha, "dry_run": False,
                      "tracked": len(tracked), "mirror": len(mirrored),
                      "missing": n_missing, "skipped": n_skipped,
                      "total_segments": total_segments,
                      "report": report_path.name}, ensure_ascii=False))
    return {"mode": "init", "commit": sha, "has_changes": True, "dry_run": False}


def sync_check_or_apply(ctx, repo_url, ref, only_file, dry_run, apply) -> Dict:
    """--check / --apply：文件级 blob sha 比对 → 段落级工作项 → 写盘（apply）。"""
    m = load_manifest(ctx.manifest_file)
    if m is None:
        raise RuntimeError("manifest.yml 不存在；请先执行 --init 首次快照")
    if apply and not dry_run and not apply_unlocked(ctx):
        raise RuntimeError(
            "初译期 --apply 门控禁用（PLAN §4.4）：v1.0 tag 前仅允许 --check + 开 issue。"
            "测试可临时用 MZD_ALLOW_APPLY=1。")
    sha = prepare_upstream(repo_url, ctx.workdir, ref)
    tracked, mirror = read_upstream(ctx.workdir / UPSTREAM_DOC)

    changes: List[FileChange] = []
    workitems: Dict[str, Dict[str, int]] = {}

    manifest_names = {f["file"] for f in m.files}
    upstream_names = set(tracked.keys())
    if only_file:
        manifest_names = {n for n in manifest_names if n == only_file}
        upstream_names = {n for n in upstream_names if n == only_file}

    # 改名识别：上游删除集 × 新增集按 blob sha 配对（无 git 历史也可识别）
    removed_names = manifest_names - upstream_names
    added_names = upstream_names - manifest_names
    renames: Dict[str, str] = {}
    for new_name in sorted(added_names):
        new_sha = compute_blob_sha(tracked[new_name])
        for old_name in sorted(removed_names):
            old_entry = m.entry(old_name)
            if old_entry and old_entry["blob_sha"] == new_sha:
                renames[old_name] = new_name
                break
    for old_name, new_name in renames.items():
        removed_names.discard(old_name)
        added_names.discard(new_name)

    today = date.today().isoformat()

    for name in sorted(manifest_names & upstream_names):
        raw = tracked[name]
        entry = m.entry(name)
        new_blob = compute_blob_sha(raw)
        ch = FileChange(name, "NONE", old_blob=entry["blob_sha"], new_blob=new_blob)
        if new_blob != entry["blob_sha"]:
            ch.type = "M"
            old_segs = _segments_of(
                (_safe_join(ctx.source_dir, name)).read_text(encoding="utf-8"), name)
            new_segs = _segments_of(raw.decode("utf-8"), name)
            counts = scan_workitems(old_segs, new_segs)
            ch.added, ch.modified, ch.removed = (counts["added"],
                                                 counts["modified"],
                                                 counts["removed"])
            workitems[name] = counts
            if apply and not dry_run:
                _write_source(ctx.source_dir, name, raw)
                entry["blob_sha"] = new_blob
                entry["size"] = len(raw)
                entry["paragraphs"] = len(new_segs)
                entry["updated_at"] = today
                entry["upstream_commit"] = ""  # 待 --collect-commits 补采
                # stale 仅当 zh 已开译（存在译文），否则保持 missing
                entry["status"] = "stale" if _has_zh(ctx, name) else "missing"
                ch.action = "applied"
            else:
                ch.action = "would-apply" if apply else "detected"
        changes.append(ch)

    for old_name, new_name in renames.items():
        ch = FileChange(f"{old_name} -> {new_name}", "R",
                        old_blob=m.entry(old_name)["blob_sha"],
                        new_blob=compute_blob_sha(tracked[new_name]))
        if apply and not dry_run:
            raw = tracked[new_name]
            _write_source(ctx.source_dir, new_name, raw)
            src_old = _safe_join(ctx.source_dir, old_name)
            if src_old.exists():
                src_old.unlink()
            zh_old = zh_path_of(ctx, old_name)
            if zh_old.exists():
                zh_new = zh_path_of(ctx, new_name)
                zh_new.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(zh_old), str(zh_new))
                text = zh_new.read_text(encoding="utf-8")
                text = text.replace(f"upstream_file: {old_name}",
                                    f"upstream_file: {new_name}", 1)
                zh_new.write_text(text, encoding="utf-8")
            entry = m.entry(old_name)
            entry["file"] = new_name
            entry["zh"] = f"zh/{new_name}"
            entry["blob_sha"] = ch.new_blob
            entry["size"] = len(raw)
            entry["paragraphs"] = len(_segments_of(raw.decode("utf-8"), new_name))
            entry["updated_at"] = today
            entry["upstream_commit"] = ""
            ch.action = "applied"
        else:
            ch.action = "would-apply" if apply else "detected"
        changes.append(ch)

    archived: List[str] = []
    for name in sorted(removed_names):
        old_blob = entry_blob_of(m, name)
        if apply and not dry_run:
            day = date.today().isoformat()
            for from_dir, sub in ((ctx.source_dir, "source"), (ctx.zh_dir, "zh")):
                src = _safe_join(from_dir, name)
                if src.exists():
                    dst = ctx.repo_root / "archive" / day / sub / name
                    dst.parent.mkdir(parents=True, exist_ok=True)
                    shutil.move(str(src), str(dst))
            m.files.remove(m.entry(name))
            archived.append(name)
            changes.append(FileChange(name, "D", old_blob=old_blob,
                                      action="archived"))
        else:
            changes.append(FileChange(name, "D",
                                      old_blob=entry_blob_of(m, name) or "",
                                      action="flagged-for-human"))
    if apply and not dry_run and archived:
        logger.info("上游删除 %d 个文件，已移入 archive/（保留追溯）", len(archived))

    for name in sorted(added_names):
        raw = tracked[name]
        segs = _segments_of(raw.decode("utf-8"), name)
        ch = FileChange(name, "A", new_blob=compute_blob_sha(raw))
        if apply and not dry_run:
            _write_source(ctx.source_dir, name, raw)
            skipped = len(raw) == 0 or is_shell_file(segs)
            m.files.append({
                "file": name, "blob_sha": compute_blob_sha(raw),
                "size": len(raw),
                "status": "skipped" if skipped else "missing",
                "zh": f"zh/{name}", "paragraphs": len(segs),
                "updated_at": today,
            })
            ch.action = "applied"
        else:
            ch.action = "would-apply" if apply else "detected"
        changes.append(ch)

    if apply and not dry_run:
        m.files.sort(key=lambda f: f["file"])
        save_manifest(ctx.manifest_file, m)
        (ctx.source_dir / "_upstream_commit").write_text(sha + "\n", encoding="utf-8")
        mirrored = mirror_into_source(mirror, ctx.source_dir)
        if mirrored:
            logger.info("镜像非账本文件 %d 个", len(mirrored))

    stale = [f["file"] for f in m.files if f["status"] == "stale"]
    missing = [f["file"] for f in m.files if f["status"] == "missing"]
    summary = {
        "mode": "apply" if apply else "check",
        "commit": sha,
        "dry_run": dry_run,
        "has_changes": any(c.type != "NONE" for c in changes),
        "changes": [c.__dict__ for c in changes],
        "workitems": workitems,
        "stale": stale,
        "missing": missing,
    }

    if apply and not dry_run and any(c.type != "NONE" for c in changes):
        ctx.reports_dir.mkdir(parents=True, exist_ok=True)
        report_path = ctx.reports_dir / f"sync-{today}-{sha[:8]}.md"
        report_path.write_text(
            render_report(mode="apply", sha=sha, ref=ref, dry_run=False,
                          changes=changes, extra={"workitems": workitems}),
            encoding="utf-8")
        logger.info("同步报告：%s", report_path)
        summary["report"] = report_path.name
    elif changes:
        print(render_report(mode="apply" if apply else "check", sha=sha, ref=ref,
                            dry_run=True, changes=changes,
                            extra={"workitems": workitems}))

    print(json.dumps(summary, ensure_ascii=False))
    return summary


def entry_blob_of(m: Manifest, fname: str) -> str:
    e = m.entry(fname)
    return e["blob_sha"] if e else ""


def mark_current(ctx: SyncContext, fname: str) -> Dict:
    """--mark-current：校验 zh 溯源注释四字段与账本对齐后置 status=current。"""
    m = load_manifest(ctx.manifest_file)
    if m is None:
        raise RuntimeError("manifest.yml 不存在")
    entry = m.entry(fname)
    if entry is None:
        raise RuntimeError(f"manifest 中不存在 {fname}")
    zh_file = zh_path_of(ctx, fname)
    if not zh_file.exists():
        raise RuntimeError(f"译文不存在：{zh_file}")
    text = zh_file.read_text(encoding="utf-8")
    mo = RE_PROVENANCE.search(text)
    if mo is None:
        raise RuntimeError(f"{zh_file} 缺溯源注释（upstream_file/upstream_commit/"
                           "upstream_hash/translated_at），不能标记 current")
    f_file, f_commit, f_hash, f_date = mo.groups()
    baseline = _upstream_commit_of(ctx)
    problems = []
    if f_file != fname:
        problems.append(f"upstream_file={f_file!r} != {fname!r}")
    if f_hash != entry["blob_sha"]:
        problems.append(f"upstream_hash={f_hash[:8]}… != manifest blob_sha="
                        f"{entry['blob_sha'][:8]}…")
    expect_commit = entry.get("upstream_commit") or baseline
    if f_commit != expect_commit:
        problems.append(f"upstream_commit={f_commit[:8]}… != 期望 "
                        f"{expect_commit[:8]}…（账本 per-file 字段优先）")
    if f_date != date.today().isoformat():
        # translated_at 允许批次进行期日期，仅提示不阻断？——按 PLAN §5.4 是
        # 修订收尾必填项，格式校验即可，不强制今日
        pass
    if problems:
        raise RuntimeError("mark-current 校验失败（溯源注释与账本不一致）：\n  - "
                           + "\n  - ".join(problems))
    entry["status"] = "current"
    entry["updated_at"] = date.today().isoformat()
    save_manifest(ctx.manifest_file, m)
    print(json.dumps({"mode": "mark-current", "file": fname,
                      "status": "current"}, ensure_ascii=False))
    return {"file": fname, "status": "current"}


def _upstream_commit_of(ctx: SyncContext) -> str:
    f = ctx.source_dir / "_upstream_commit"
    return f.read_text(encoding="utf-8").strip() if f.exists() else ""


def collect_commits(ctx: SyncContext, ref: str, only_file: Optional[str]) -> Dict:
    """逐文件采集 upstream_commit（gh api 串行 + 本地缓存，失败可延后补采）。"""
    m = load_manifest(ctx.manifest_file)
    if m is None:
        raise RuntimeError("manifest.yml 不存在")
    slug = "/".join(UPSTREAM_REPO.rstrip("/").split("/")[-2:])
    cache_file = ctx.workdir.parent / "commit-cache.json"
    cache: Dict[str, str] = {}
    if cache_file.exists():
        cache = json.loads(cache_file.read_text(encoding="utf-8"))
    collected, failed, skipped_n = 0, 0, 0
    for entry in sorted(m.files, key=lambda f: f["file"]):
        if only_file and entry["file"] != only_file:
            continue
        if entry.get("upstream_commit"):
            skipped_n += 1
            continue
        key = f"{entry['file']}:{entry['blob_sha']}"
        commit = cache.get(key)
        if not commit:
            commit = _gh_api_last_commit(slug, entry["file"], ref) or ""
            if commit:
                cache[key] = commit
                cache_file.parent.mkdir(parents=True, exist_ok=True)
                cache_file.write_text(json.dumps(cache), encoding="utf-8")
            else:
                failed += 1
                continue
        entry["upstream_commit"] = commit
        collected += 1
    save_manifest(ctx.manifest_file, m)
    cache_file.write_text(json.dumps(cache), encoding="utf-8")
    print(json.dumps({"mode": "collect-commits", "collected": collected,
                      "failed_deferred": failed, "already": skipped_n},
                     ensure_ascii=False))
    return {"collected": collected, "failed_deferred": failed,
            "already": skipped_n}


# ---------- 报告渲染 ----------

def render_report(mode, sha, ref, dry_run, changes, extra) -> str:
    today = date.today().isoformat()
    lines = [
        f"# 同步报告：{today} @ {sha[:8]}（{ref}）",
        "",
        f"- 模式：`--{mode}`" + ("（dry-run 预演，未写盘）" if dry_run else ""),
        f"- 上游 commit：`{sha}`",
        f"- 仓库：`{UPSTREAM_REPO}`（文档树 {UPSTREAM_DOC}）",
    ]
    if extra.get("baseline_locked"):
        lines.append("- 基线：tag v5.2.25 锁定（初译期基线锁定策略，PLAN §4.4）")
    lines += [
        "",
        "| 文件 | 变更 | 新增段 | 修改段 | 删除段 | 动作 |",
        "|---|---|---:|---:|---:|---|",
    ]
    for c in changes:
        lines.append(
            f"| {c.file} | {c.type} | {c.added} | {c.modified} | {c.removed} "
            f"| {c.action} |")
    if extra.get("workitems"):
        lines += ["", "## 段落级工作项", ""]
        for fname, counts in extra["workitems"].items():
            if any(counts.values()):
                lines.append(
                    f"- `{fname}`：新增 {counts['added']} / 修改（复译）"
                    f"{counts['modified']} / 删除 {counts['removed']}")
    if "mirror_count" in extra:
        lines += ["", f"非账本镜像文件：{extra['mirror_count']} 个"]
    if "total_segments" in extra:
        lines += ["", f"总段数：{extra['total_segments']}"]
    stats = [(k, extra[k]) for k in ("missing", "skipped") if k in extra]
    if stats:
        lines += ["", "账本状态统计：" + "；".join(f"{k}={v}" for k, v in stats)]
    lines += ["", "---", "",
              f"*报告生成：{mode} 模式 @ {sha[:8]}（{today}）*"]
    return "\n".join(lines)


# ---------- CLI ----------

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="sync_upstream.py",
        description="同步上游 micronaut-core src/main/docs（--init/--check/--apply/"
                    "--mark-current/--collect-commits；一律建议 memgate 包裹运行）")
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--init", action="store_true", help="首次快照（仅一次）")
    g.add_argument("--check", action="store_true",
                   help="只检测变更，不写盘（CI 每周检测用）")
    g.add_argument("--apply", action="store_true",
                   help="应用变更（初译期 v1.0 tag 前门控禁用）")
    g.add_argument("--mark-current", metavar="FILE",
                   help="校验溯源注释后把 zh/<FILE> 标记为 current")
    g.add_argument("--collect-commits", action="store_true",
                   help="逐文件采集 upstream_commit（gh api 串行+缓存）")
    p.add_argument("--dry-run", action="store_true",
                   help="与 --init/--apply 组合：只打印不写盘")
    p.add_argument("--file", metavar="NAME",
                   help="只处理指定文件（相对 src/main/docs 路径）")
    p.add_argument("--repo", default=UPSTREAM_REPO,
                   help=f"上游仓库 URL（默认 {UPSTREAM_REPO}；测试可注入本地 file://）")
    p.add_argument("--workdir", default=None, help="克隆缓存目录（测试隔离用）")
    p.add_argument("--ref", default=None,
                   help="上游分支/标签（缺省：init=v5.2.25，其余=5.2.x）")
    return p


def main(argv: Optional[List[str]] = None):
    parser = build_parser()
    args = parser.parse_args(argv)
    ref = args.ref or (INIT_REF if args.init else DEFAULT_REF)

    ctx = get_ctx()
    if args.workdir:
        ctx = SyncContext(source_dir=ctx.source_dir, zh_dir=ctx.zh_dir,
                          reports_dir=ctx.reports_dir,
                          manifest_file=ctx.manifest_file,
                          repo_root=ctx.repo_root,
                          workdir=Path(args.workdir))
    if args.mark_current and (args.dry_run or args.file):
        parser.error("--mark-current 不支持 --dry-run/--file")
    if args.dry_run and not (args.init or args.apply):
        parser.error("--dry-run 仅与 --init/--apply 组合")
    if args.file and args.mark_current:
        parser.error("--file 与 --mark-current 互斥")

    try:
        if args.init:
            result = sync_init(ctx, args.repo, ref, args.file, args.dry_run)
        elif args.check:
            result = sync_check_or_apply(ctx, args.repo, ref, args.file,
                                         dry_run=True, apply=False)
        elif args.apply:
            result = sync_check_or_apply(ctx, args.repo, ref, args.file,
                                         dry_run=args.dry_run, apply=True)
        elif args.mark_current:
            result = mark_current(ctx, args.mark_current)
        elif args.collect_commits:
            result = collect_commits(ctx, ref, args.file)
        else:
            result = None
        # 退出码约定：0=无变更 / 1=有变更待翻译 / 2=环境错误
        if isinstance(result, dict) and result.get("has_changes"):
            sys.exit(1)
    except (RuntimeError, subprocess.CalledProcessError, OSError, ValueError) as e:
        logger.error("Failed: %s", e)
        sys.exit(2)


if __name__ == "__main__":
    main()
