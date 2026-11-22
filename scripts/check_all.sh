#!/usr/bin/env bash
# 遍历 config/modules.json 串行逐模块 sync --check 并汇总（DR-006 §5/§6）。
#
# - core 用缺省账本 manifest.yml；模块用 manifests/<site>.yml（未快照 → 跳过）。
# - ref 不传：sync 自动取账本顶层 ref（模块）/缺省 5.2.x（core）。
# - 退出码逐模块采集、不掩码：0=无变更 1=有变更待翻译 2=环境错误；
#   脚本最终退出码 = 最严重者（2 > 1 > 0），供 CI 判断。
# - 产出：stdout JSON 行（CI 解析）+ reports/check-all-<date>.md 汇总表。
#
# 运行：bash scripts/check_all.sh（本机脚本经 memgate 包裹由脚本内部处理）
set -u
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_ROOT" || exit 2
MODULES_JSON="config/modules.json"
STAMP="$(date +%Y-%m-%d)"
MD_REPORT="reports/check-all-${STAMP}.md"
JSONL="reports/check-all-latest.jsonl"

MEMGATE=""
if command -v memgate >/dev/null 2>&1; then
  MEMGATE="memgate 2048"
fi

SITES="$(python3 -c '
import json
cfg = json.load(open("config/modules.json", encoding="utf-8"))
sites = ["core"]
for g in cfg.get("groups", []):
    for m in g.get("modules", []):
        mod = cfg.get("modules", {}).get(m, {})
        if mod.get("external") or m == "core" or m in sites:
            continue
        sites.append(m)
print(" ".join(sites))
')"

: > "$JSONL"
printf '# check-all 上游同步检测汇总（%s）\n\n' "$STAMP" > "$MD_REPORT"
printf '| 模块 | 账本 | 退出码 | 结果 | 上游 HEAD |\n|---|---|---:|---|---|\n' >> "$MD_REPORT"

worst=0
for site in $SITES; do
  if [ "$site" = "core" ]; then
    manifest="manifest.yml"
    manifest_args=()
  else
    manifest="manifests/${site}.yml"
    if [ ! -f "$manifest" ]; then
      printf '| %s | — | — | 未快照（跳过） | — |\n' "$site" >> "$MD_REPORT"
      printf '{"site":"%s","code":-1,"sha8":"","note":"not-snapshotted"}\n' "$site" >> "$JSONL"
      continue
    fi
    manifest_args=(--manifest "$manifest")
  fi
  out="$($MEMGATE python3 scripts/sync_upstream.py "${manifest_args[@]}" --check 2>&1)"
  code=$?
  sha8="$(printf '%s\n' "$out" | python3 -c '
import json, sys
last = [l for l in sys.stdin if l.strip().startswith("{")]
try:
    print(json.loads(last[-1]).get("commit", "?")[:8])
except Exception:
    print("?")')"
  case "$code" in
    0) verdict="无变更" ;;
    1) verdict="有变更待翻译" ;;
    2) verdict="环境错误" ;;
    *) verdict="异常退出码 $code" ;;
  esac
  printf '| %s | `%s` | %d | %s | %s |\n' "$site" "$manifest" "$code" "$verdict" "$sha8" >> "$MD_REPORT"
  printf '{"site":"%s","code":%d,"sha8":"%s"}\n' "$site" "$code" "$sha8" >> "$JSONL"
  case "$code" in
    0) : ;;
    2) worst=2 ;;
    1) [ "$worst" -ne 2 ] && worst=1 ;;
    *) worst=2 ;;  # 意外退出码（如 127）视为环境错误，禁止吞掉
  esac
done

printf '\n> JSON 行：`%s`（CI 逐模块开 issue 用；code 1=有变更 2=环境错误）\n' "$JSONL" >> "$MD_REPORT"
echo "report: $MD_REPORT"
cat "$JSONL"
exit "$worst"
