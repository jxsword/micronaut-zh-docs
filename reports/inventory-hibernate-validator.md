# 模块批次切分报告：hibernate-validator（https://github.com/micronaut-projects/micronaut-hibernate-validator @0ae7293d6bc9）

- 基线：https://github.com/micronaut-projects/micronaut-hibernate-validator@0ae7293d6bc9，ref 5.2.x，快照 2026-11-23（locked_at 2026-11-23）
- 账本：5 条目，missing 5 / skipped 0
- 词数总计：非代码词 76 / 总词 76 / 总段 8（口径：保护后 wc -w 等价）
- 批次：1 个（双指标 非代码词 ≤3500 且 总词 ≤5500，toc 顺序贪心装箱；编号前缀 HV-）

## toc.yml 实测结论

- 键路径 → 文件映射：`modules/hibernate-validator/guide/<键路径>.adoc`（DFS 序即阅读顺序）；toc 覆盖 4 个文件，未入 toc 的 include 片段 0 个（按目录序追加在批次末尾）。

## 批次切分表

| 批次 | 文件数 | 非代码词 | 总词 |
|---|---:|---:|---:|
| HV-01 | 4 | 76 | 76 |

## 逐批次文件清单

### HV-01（非代码词 76 / 总词 76）

`modules/hibernate-validator/guide/introduction.adoc`、`modules/hibernate-validator/guide/releaseHistory.adoc`、`modules/hibernate-validator/guide/setup.adoc`、`modules/hibernate-validator/guide/repository.adoc`


---

*inventory 自动生成：scripts/inventory.py（PLAN §5.1/DR-006 §4；批次数以本报告实测为准）*