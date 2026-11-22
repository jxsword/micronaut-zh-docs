# 模块批次切分报告：session（https://github.com/micronaut-projects/micronaut-session @14290594e9a9）

- 基线：https://github.com/micronaut-projects/micronaut-session@14290594e9a9，ref 5.2.x，快照 2026-11-23（locked_at 2026-11-23）
- 账本：14 条目，missing 14 / skipped 0
- 词数总计：非代码词 689 / 总词 705 / 总段 58（口径：保护后 wc -w 等价）
- 批次：1 个（双指标 非代码词 ≤3500 且 总词 ≤5500，toc 顺序贪心装箱；编号前缀 SESSION-）

## toc.yml 实测结论

- 键路径 → 文件映射：`modules/session/guide/<键路径>.adoc`（DFS 序即阅读顺序）；toc 覆盖 13 个文件，未入 toc 的 include 片段 0 个（按目录序追加在批次末尾）。

## 批次切分表

| 批次 | 文件数 | 非代码词 | 总词 |
|---|---:|---:|---:|
| SESSION-01 | 13 | 689 | 705 |

## 逐批次文件清单

### SESSION-01（非代码词 689 / 总词 705）

`modules/session/guide/introduction.adoc`、`modules/session/guide/breaks.adoc`、`modules/session/guide/sessions.adoc`、`modules/session/guide/sessions/sessionFilter.adoc`、`modules/session/guide/sessions/enablingSessions.adoc`、`modules/session/guide/sessions/redisSessions.adoc`、`modules/session/guide/sessions/configuringSessionResolution.adoc`、`modules/session/guide/sessions/workingWithSessions.adoc`、`modules/session/guide/sessions/sessionClients.adoc`、`modules/session/guide/sessions/sessionValue.adoc`、`modules/session/guide/sessions/sessionEvents.adoc`、`modules/session/guide/releaseHistory.adoc`、`modules/session/guide/repository.adoc`


---

*inventory 自动生成：scripts/inventory.py（PLAN §5.1/DR-006 §4；批次数以本报告实测为准）*