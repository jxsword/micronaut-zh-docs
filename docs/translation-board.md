# 批次看板（translation-board）

> 批次切分与文件清单以 reports/inventory-5.2.25.md 为准（32 批，双指标 非代码词 ≤3500 且 总词 ≤5500）。
> 状态机：pending → in-progress → translated → reviewed → current（核销走 sync --mark-current）。

## 批次总览

| 批次 | 文件数 | 非代码词 | 总词 | 状态 |
|---|---:|---:|---:|---|
| B01 | 19 | 3347 | 3355 | current |
| B02 | 12 | 3049 | 3082 | current |
| B03 | 10 | 3443 | 3454 | pending |
| B04 | 19 | 2591 | 2604 | pending |
| B05 | 2 | 2138 | 2128 | pending |
| B06 | 11 | 3454 | 3489 | pending |
| B07 | 4 | 2507 | 2554 | pending |
| B08 | 4 | 3397 | 3442 | pending |
| B09 | 8 | 2915 | 2915 | pending |
| B10 | 5 | 3086 | 3092 | pending |
| B11 | 7 | 3350 | 3352 | pending |
| B12 | 25 | 3454 | 3460 | pending |
| B13 | 17 | 3167 | 3185 | pending |
| B14 | 13 | 3482 | 3476 | pending |
| B15 | 13 | 3452 | 3485 | pending |
| B16 | 24 | 3223 | 3291 | pending |
| B17 | 15 | 3004 | 3008 | pending |
| B18 | 8 | 3379 | 3379 | pending |
| B19 | 14 | 3455 | 3491 | pending |
| B20 | 21 | 3456 | 3512 | pending |
| B21 | 35 | 2983 | 3078 | pending |
| B22 | 5 | 3062 | 3057 | pending |
| B23 | 6 | 3378 | 3353 | pending |
| B24 | 5 | 3257 | 3199 | pending |
| B25 | 7 | 3096 | 3070 | pending |
| B26 | 14 | 3416 | 3439 | pending |
| B27 | 17 | 3478 | 3538 | pending |
| B28 | 21 | 2955 | 3023 | pending |
| B29 | 14 | 3226 | 3257 | pending |
| B30 | 4 | 3387 | 3401 | pending |
| B31 | 3 | 955 | 960 | pending |
| B32 | 2 | 3180 | 3183 | pending |

## 批次状态明细

批次 → 文件清单：见 inventory 报告「逐批次文件清单」节（B01–B32）。

## 备注

- B01（2026-11-20 完成）：validate 七项全绿 + 19/19 --mark-current 核销 + squash commit。实测修复 M1 缺陷 4 处（check_anchors http 前缀裸锚点误跳过 → registry 116→121；validate ⑤ 裸锚点误报 + reg_ids 放行收紧；禁繁体表简繁共用字误报）与 segment_adoc snippet:: 指令行补录；新增 scripts/assemble_zh.py（溯源投影装配）。官方站单页锚点实测为 core-<basename>；上游 httpServer/httpClient/certificates 三章未被官方站渲染（详见 reports/batch-B01.md）。冻结窗口遵守：批次期间未运行 sync --apply。
- B02（2026-11-21 完成）：validate 全量 31 文件 PASSED + 12/12 --mark-current 核销 + squash commit；进度 31/388（8.0%）。锚点注入 4 处（types/qualifiers/scopes/refreshable，统一规则：basename 锚点 = 片段首内容之前）。术语转正 3 条（qualifier/eager initialization/meta annotation）；修复 validate ③ strip_code 指令行误报（snippet:: 宏参数触发必译术语，pytest 95 绿）。词数以批次实测为准（3055/2991，M1 报告值系 snippet:: 修复前口径）。⑤ 豁免警告 29 条（详见 reports/batch-B02.md）。冻结窗口遵守。

## 硬性纪律（每批次必守）

1. 认领批次先在本表改状态为 in-progress；同一文件严禁两个 agent 并发写（agent 并发上限 = 串行 1）
2. 批次进行期间为冻结窗口：禁止 sync --apply（初译期本就被门控禁用）；检测到的变更记录于本表备注
3. SOP 按 PLAN §5.1 七步走：protect → translator → restore → reviewer 五项 → validate 全绿 → --mark-current 核销 → squash commit + 批次报告
4. 术语先写回 glossary.yml 再继续；banned 0 命中是硬门禁
5. 被引用标题按 config/anchor-registry.yml 原位注入 [[原锚点]]
6. 每批次 squash commit（message 含批次号/段数/词数/上游日期）+ reports/batch-<N>.md 报告
7. 收尾更新本看板与 docs/handoff-latest.md
