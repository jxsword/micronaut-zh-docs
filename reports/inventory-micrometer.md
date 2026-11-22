# 模块批次切分报告：micrometer（https://github.com/micronaut-projects/micronaut-micrometer @c4d064ee3af4）

- 基线：https://github.com/micronaut-projects/micronaut-micrometer@c4d064ee3af4，ref 5.2.x，快照 2026-11-23（locked_at 2026-11-23）
- 账本：30 条目，missing 30 / skipped 0
- 词数总计：非代码词 3566 / 总词 3634 / 总段 324（口径：保护后 wc -w 等价）
- 批次：2 个（双指标 非代码词 ≤3500 且 总词 ≤5500，toc 顺序贪心装箱；编号前缀 MICRO-）

## toc.yml 实测结论

- 键路径 → 文件映射：`modules/micrometer/guide/<键路径>.adoc`（DFS 序即阅读顺序）；toc 覆盖 29 个文件，未入 toc 的 include 片段 0 个（按目录序追加在批次末尾）。

## 批次切分表

| 批次 | 文件数 | 非代码词 | 总词 |
|---|---:|---:|---:|
| MICRO-01 | 27 | 3239 | 3307 |
| MICRO-02 | 2 | 327 | 327 |

## 逐批次文件清单

### MICRO-01（非代码词 3239 / 总词 3307）

`modules/micrometer/guide/introduction.adoc`、`modules/micrometer/guide/releaseHistory.adoc`、`modules/micrometer/guide/metricsEndpoint.adoc`、`modules/micrometer/guide/metricsConcepts.adoc`、`modules/micrometer/guide/metricsAnnotations.adoc`、`modules/micrometer/guide/metricsAndReporters.adoc`、`modules/micrometer/guide/metricsAndReporters/metricsAndReportersAppOptics.adoc`、`modules/micrometer/guide/metricsAndReporters/metricsAndReportersAtlas.adoc`、`modules/micrometer/guide/metricsAndReporters/metricsAndReportersAzureMonitor.adoc`、`modules/micrometer/guide/metricsAndReporters/metricsAndReportersCloudWatch.adoc`、`modules/micrometer/guide/metricsAndReporters/metricsAndReportersDatadog.adoc`、`modules/micrometer/guide/metricsAndReporters/metricsAndReportersDynatrace.adoc`、`modules/micrometer/guide/metricsAndReporters/metricsAndReportersElastic.adoc`、`modules/micrometer/guide/metricsAndReporters/metricsAndReportersGanglia.adoc`、`modules/micrometer/guide/metricsAndReporters/metricsAndReportersGraphite.adoc`、`modules/micrometer/guide/metricsAndReporters/metricsAndReportersHumio.adoc`、`modules/micrometer/guide/metricsAndReporters/metricsAndReportersInflux.adoc`、`modules/micrometer/guide/metricsAndReporters/metricsAndReportersJmx.adoc`、`modules/micrometer/guide/metricsAndReporters/metricsAndReportersKairos.adoc`、`modules/micrometer/guide/metricsAndReporters/metricsAndReportersNewRelic.adoc`、`modules/micrometer/guide/metricsAndReporters/metricsAndReportersNewRelicTelemetry.adoc`、`modules/micrometer/guide/metricsAndReporters/metricsAndReportersOracleCloud.adoc`、`modules/micrometer/guide/metricsAndReporters/metricsAndReportersPrometheus.adoc`、`modules/micrometer/guide/metricsAndReporters/metricsAndReportersSignalFx.adoc`、`modules/micrometer/guide/metricsAndReporters/metricsAndReportersStackdriver.adoc`、`modules/micrometer/guide/metricsAndReporters/metricsAndReportersStatsD.adoc`、`modules/micrometer/guide/metricsAndReporters/metricsAndReportersWavefront.adoc`

### MICRO-02（非代码词 327 / 总词 327）

`modules/micrometer/guide/observation.adoc`、`modules/micrometer/guide/repository.adoc`


---

*inventory 自动生成：scripts/inventory.py（PLAN §5.1/DR-006 §4；批次数以本报告实测为准）*