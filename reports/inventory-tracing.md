# 模块批次切分报告：tracing（https://github.com/micronaut-projects/micronaut-tracing @d38f08c067a9）

- 基线：https://github.com/micronaut-projects/micronaut-tracing@d38f08c067a9，ref 8.4.x，快照 2026-11-23（locked_at 2026-11-23）
- 账本：25 条目，missing 25 / skipped 0
- 词数总计：非代码词 2878 / 总词 2929 / 总段 218（口径：保护后 wc -w 等价）
- 批次：1 个（双指标 非代码词 ≤3500 且 总词 ≤5500，toc 顺序贪心装箱；编号前缀 TRACING-）

## toc.yml 实测结论

- 键路径 → 文件映射：`modules/tracing/guide/<键路径>.adoc`（DFS 序即阅读顺序）；toc 覆盖 24 个文件，未入 toc 的 include 片段 0 个（按目录序追加在批次末尾）。

## 批次切分表

| 批次 | 文件数 | 非代码词 | 总词 |
|---|---:|---:|---:|
| TRACING-01 | 24 | 2878 | 2929 |

## 逐批次文件清单

### TRACING-01（非代码词 2878 / 总词 2929）

`modules/tracing/guide/introduction.adoc`、`modules/tracing/guide/releaseHistory.adoc`、`modules/tracing/guide/breaks.adoc`、`modules/tracing/guide/jaeger.adoc`、`modules/tracing/guide/zipkin.adoc`、`modules/tracing/guide/opentelemetry.adoc`、`modules/tracing/guide/opentelemetry/annotations.adoc`、`modules/tracing/guide/opentelemetry/exporters.adoc`、`modules/tracing/guide/opentelemetry/logback.adoc`、`modules/tracing/guide/opentelemetry/customization.adoc`、`modules/tracing/guide/opentelemetry/propagators.adoc`、`modules/tracing/guide/opentelemetry/idgenerator.adoc`、`modules/tracing/guide/opentelemetry/http.adoc`、`modules/tracing/guide/opentelemetry/mdc.adoc`、`modules/tracing/guide/opentelemetry/grpc.adoc`、`modules/tracing/guide/opentelemetry/jdbc.adoc`、`modules/tracing/guide/opentelemetry/r2dbc.adoc`、`modules/tracing/guide/opentelemetry/kafka.adoc`、`modules/tracing/guide/opentelemetry/ucp.adoc`、`modules/tracing/guide/opentelemetry/awsSdkInstrumentation.adoc`、`modules/tracing/guide/opentelemetry/awsResourceDetectors.adoc`、`modules/tracing/guide/opentelemetry/opentelemetryGuides.adoc`、`modules/tracing/guide/tracingGuides.adoc`、`modules/tracing/guide/repository.adoc`


---

*inventory 自动生成：scripts/inventory.py（PLAN §5.1/DR-006 §4；批次数以本报告实测为准）*