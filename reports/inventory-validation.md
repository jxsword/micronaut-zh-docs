# 模块批次切分报告：validation（https://github.com/micronaut-projects/micronaut-validation @079f75dc6ba8）

- 基线：https://github.com/micronaut-projects/micronaut-validation@079f75dc6ba8，ref 5.2.x，快照 2026-11-23（locked_at 2026-11-23）
- 账本：12 条目，missing 12 / skipped 0
- 词数总计：非代码词 1463 / 总词 1479 / 总段 106（口径：保护后 wc -w 等价）
- 批次：1 个（双指标 非代码词 ≤3500 且 总词 ≤5500，toc 顺序贪心装箱；编号前缀 VALID-）

## toc.yml 实测结论

- 键路径 → 文件映射：`modules/validation/guide/<键路径>.adoc`（DFS 序即阅读顺序）；toc 覆盖 11 个文件，未入 toc 的 include 片段 0 个（按目录序追加在批次末尾）。

## 批次切分表

| 批次 | 文件数 | 非代码词 | 总词 |
|---|---:|---:|---:|
| VALID-01 | 11 | 1463 | 1479 |

## 逐批次文件清单

### VALID-01（非代码词 1463 / 总词 1479）

`modules/validation/guide/introduction.adoc`、`modules/validation/guide/releaseHistory.adoc`、`modules/validation/guide/quickStart.adoc`、`modules/validation/guide/methodsValidation.adoc`、`modules/validation/guide/dataClassesValidation.adoc`、`modules/validation/guide/configurationValidation.adoc`、`modules/validation/guide/additionalConstraints.adoc`、`modules/validation/guide/builtInConstraints.adoc`、`modules/validation/guide/compileTimeValidation.adoc`、`modules/validation/guide/breaks.adoc`、`modules/validation/guide/repository.adoc`


---

*inventory 自动生成：scripts/inventory.py（PLAN §5.1/DR-006 §4；批次数以本报告实测为准）*