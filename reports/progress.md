# 翻译进度报表（自动生成，禁手改）

> 生成: 2026-11-23 06:30:55 ｜ 数据源: manifest.yml + manifests/*.yml（DR-006 M4 聚合）

## 总览（按模块）

| 模块 | 文件数 | missing | stale | partial | current | skipped | 进度 |
|---|---:|---:|---:|---:|---:|---:|---:|
| core | 388 | 0 | 0 | 0 | 387 | 1 | 100.0% |
| hibernate-validator | 5 | 0 | 0 | 0 | 5 | 0 | 100.0% |
| micrometer | 30 | 0 | 0 | 0 | 30 | 0 | 100.0% |
| security | 145 | 0 | 0 | 0 | 140 | 5 | 100.0% |
| session | 14 | 14 | 0 | 0 | 0 | 0 | 0.0% |
| tracing | 25 | 25 | 0 | 0 | 0 | 0 | 0.0% |
| validation | 12 | 0 | 0 | 0 | 12 | 0 | 100.0% |

## core

> 基线: 0b46d27afdfa，快照 2026-11-20

| 章节 | 文件数 | missing | stale | partial | current | skipped | 进度 |
|---|---:|---:|---:|---:|---:|---:|---:|
| aop | 10 | 0 | 0 | 0 | 10 | 0 | 100% |
| appendix | 12 | 0 | 0 | 0 | 12 | 0 | 100% |
| cli | 10 | 0 | 0 | 0 | 10 | 0 | 100% |
| cloud | 17 | 0 | 0 | 0 | 17 | 0 | 100% |
| commandLineApps | 1 | 0 | 0 | 0 | 1 | 0 | 100% |
| config | 15 | 0 | 0 | 0 | 15 | 0 | 100% |
| configurations | 13 | 0 | 0 | 0 | 13 | 0 | 100% |
| contextPropagation | 2 | 0 | 0 | 0 | 2 | 0 | 100% |
| guide | 25 | 0 | 0 | 0 | 24 | 1 | 100% |
| httpClient | 26 | 0 | 0 | 0 | 26 | 0 | 100% |
| httpServer | 101 | 0 | 0 | 0 | 101 | 0 | 100% |
| i18n | 2 | 0 | 0 | 0 | 2 | 0 | 100% |
| introduction | 2 | 0 | 0 | 0 | 2 | 0 | 100% |
| ioc | 55 | 0 | 0 | 0 | 55 | 0 | 100% |
| languageSupport | 50 | 0 | 0 | 0 | 50 | 0 | 100% |
| logging | 4 | 0 | 0 | 0 | 4 | 0 | 100% |
| management | 27 | 0 | 0 | 0 | 27 | 0 | 100% |
| messaging | 3 | 0 | 0 | 0 | 3 | 0 | 100% |
| quickStart | 9 | 0 | 0 | 0 | 9 | 0 | 100% |
| serverlessFunctions | 4 | 0 | 0 | 0 | 4 | 0 | 100% |
| **合计** | **388** | **0** | **0** | **0** | **387** | **1** | **100.0%** |

## hibernate-validator

> 基线: 0ae7293d6bc9，快照 2026-11-23，ref 5.2.x（locked_at 2026-11-23）

| 章节 | 文件数 | missing | stale | partial | current | skipped | 进度 |
|---|---:|---:|---:|---:|---:|---:|---:|
| guide | 5 | 0 | 0 | 0 | 5 | 0 | 100% |
| **合计** | **5** | **0** | **0** | **0** | **5** | **0** | **100.0%** |

## micrometer

> 基线: c4d064ee3af4，快照 2026-11-23，ref 5.2.x（locked_at 2026-11-23）

| 章节 | 文件数 | missing | stale | partial | current | skipped | 进度 |
|---|---:|---:|---:|---:|---:|---:|---:|
| guide | 9 | 0 | 0 | 0 | 9 | 0 | 100% |
| metricsAndReporters | 21 | 0 | 0 | 0 | 21 | 0 | 100% |
| **合计** | **30** | **0** | **0** | **0** | **30** | **0** | **100.0%** |

## security

> 基线: cc524538f059，快照 2026-11-23，ref 5.2.x（locked_at 2026-11-23）

| 章节 | 文件数 | missing | stale | partial | current | skipped | 进度 |
|---|---:|---:|---:|---:|---:|---:|---:|
| aot | 3 | 0 | 0 | 0 | 3 | 0 | 100% |
| authenticationProviders | 3 | 0 | 0 | 0 | 3 | 0 | 100% |
| authenticationStrategies | 27 | 0 | 0 | 0 | 26 | 1 | 100% |
| csrf | 12 | 0 | 0 | 0 | 12 | 0 | 100% |
| dataAuditing | 2 | 0 | 0 | 0 | 2 | 0 | 100% |
| endpoints | 9 | 0 | 0 | 0 | 9 | 0 | 100% |
| guide | 26 | 0 | 0 | 0 | 24 | 2 | 100% |
| oauth | 31 | 0 | 0 | 0 | 29 | 2 | 100% |
| ojdbcExtensions | 8 | 0 | 0 | 0 | 8 | 0 | 100% |
| rejection | 1 | 0 | 0 | 0 | 1 | 0 | 100% |
| retrievingAuthenticatedUser | 3 | 0 | 0 | 0 | 3 | 0 | 100% |
| securityConfiguration | 4 | 0 | 0 | 0 | 4 | 0 | 100% |
| securityFilter | 13 | 0 | 0 | 0 | 13 | 0 | 100% |
| tokenendpoints | 3 | 0 | 0 | 0 | 3 | 0 | 100% |
| **合计** | **145** | **0** | **0** | **0** | **140** | **5** | **100.0%** |

## session

> 基线: 14290594e9a9，快照 2026-11-23，ref 5.2.x（locked_at 2026-11-23）

| 章节 | 文件数 | missing | stale | partial | current | skipped | 进度 |
|---|---:|---:|---:|---:|---:|---:|---:|
| guide | 6 | 6 | 0 | 0 | 0 | 0 | 0% |
| sessions | 8 | 8 | 0 | 0 | 0 | 0 | 0% |
| **合计** | **14** | **14** | **0** | **0** | **0** | **0** | **0.0%** |

## tracing

> 基线: d38f08c067a9，快照 2026-11-23，ref 8.4.x（locked_at 2026-11-23）

| 章节 | 文件数 | missing | stale | partial | current | skipped | 进度 |
|---|---:|---:|---:|---:|---:|---:|---:|
| guide | 9 | 9 | 0 | 0 | 0 | 0 | 0% |
| opentelemetry | 16 | 16 | 0 | 0 | 0 | 0 | 0% |
| **合计** | **25** | **25** | **0** | **0** | **0** | **0** | **0.0%** |

## validation

> 基线: 079f75dc6ba8，快照 2026-11-23，ref 5.2.x（locked_at 2026-11-23）

| 章节 | 文件数 | missing | stale | partial | current | skipped | 进度 |
|---|---:|---:|---:|---:|---:|---:|---:|
| guide | 12 | 0 | 0 | 0 | 12 | 0 | 100% |
| **合计** | **12** | **0** | **0** | **0** | **12** | **0** | **100.0%** |
