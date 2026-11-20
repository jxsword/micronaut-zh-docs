# 批次报告 B28

> 完成日期：2026-11-21 ｜ 执行：M2 第二十八批次（串行 1，单会话编排方亲跑；与 B21–B27 同会话接续）

## 范围与规模

| 指标 | 值 |
|---|---|
| 文件数 | 21（management 余 15 + security + multitenancy + cli 组 3） |
| 总词数（protect 后口径，实测） | 3023（与 M1 inventory 报告值 3023 一致） |
| 非代码词（当前口径，实测） | 2955（与 M1 inventory 报告值 2955 一致） |
| 段落数 | 213（inventory segments 口径，与既往批次 commit 口径一致） |
| 上游基线 | v5.2.25（tag，2026-11-17 发布；快照 `0b46d27afdfa`） |
| 最终状态 | 21 文件全部 current（manifest 388 条目中 361/388，进度 93.5%，剔 skipped 口径） |

双指标达标：非代码词 2955 ≤ 3500 且总词 3023 ≤ 5500。占位符合计 206
（最多 createProject 59、occurrences 口径 environmentEndpoint 37）；createProject 883 非代码词/51 段
（含 5×5 命令表格，单元格内嵌 bash 代码块）为本批最重；源文件无显式锚（ANCLINE 0 处）。

## 流程执行（PLAN §5.1 SOP + 固化校验链）

1. protect：21 文件（206 占位符）；
2. 翻译：health 子组 7（端点定制/监视任务/提供指示器表/磁盘/JDBC/发现客户端/死锁线程）、
   端点 8（metrics/refresh/routes/loggers/caches/stop/environment/threadDump）、
   security、multitenancy、cli 组 3（交互模式/createProject 大表/comparingVersions）；
   `<<providedEndpoints,内置端点>>`、`<<buildCLI,…>>`、`<<commandLineApps,…>>`、
   `<<serverlessFunctions,…>>`、`<<dataAccess,数据访问配置>>`、`<<logging,日志章节>>`、
   `<<jmx,JMX>>` 目标逐字节保留、label 译出；单元格内嵌 `[source,bash]` 代码块逐字节保留；
3. restore：21/21 首轮全过；assemble 落 zh/ 21 文件（translated_at=2026-11-21）；
4. validate：逐个 `--file` **首轮 21/21 全绿（B20 以来第二次批次内零修正，
   与 B20 并列批次内零修正纪录）**；
5. 锚点注入 8 处（注入前核对 title 字段）：`[[cli]]`（标题锚「== 交互模式」之前；被 groovy/kotlin
   引用，已译——**消解既有豁免 ×2**）、`[[cachesEndpoint]]`（basename 锚）、
   `[[environmentEndpoint]]`/`[[loggersEndpoint]]`/`[[refreshEndpoint]]`/`[[routesEndpoint]]`/
   `[[stopEndpoint]]`（标题锚「== 配置」，stopEndpoint 消解 B27 新增豁免）、
   `[[metricsEndpoint]]`（basename 锚）——其余 5 处均为批内闭环；
   落盘后 grep 核对 8/8 在位且位置正确（标题锚后随标题行、basename 锚居首）；
6. reviewer 五项：/tmp/b28_reviewer.py **21/21 PASS 首轮零缺陷**（createProject 33 段）；
7. `--mark-current` 21/21 核销；全量 361 文件 PASSED；pytest 95 绿。

## 术语滚动

- 本批无新增 glossary 条目；B20 CLI 语境 feature 保留口径在 cli 章 3 文件全面沿用；
- 首现括注：健康指示器（health indicator）复现、活性指示器/活性检查复现、
  注册表（registry，Micrometer 语境）、租户解析（tenant resolution）、
  交互模式（Interactive Mode）、Tab 补全（Tab-completion）；
- banned 黑名单 0 命中。

## 里程碑与进度

- 整库进度 361/388（93.5%，剔 2 skipped）；
- **management 章 27/27 全章译出（第十六个全章）**；
- cli 章 3/10 起步（commands/reloading/proxy 组 7 在 B29）；
- guide 行 20/25（security/multitenancy/cli/createProject/comparingVersions/features 6 文件落账）；
- **⑤ 豁免 11→7 条（−4 消解 +0 新增）**：groovy→cli、kotlin→cli、providedEndpoints→stopEndpoint
  及 1 条早期登记项随落盘消解；剩余 7 条 = proxy（B29）+ i18n（skipped，M3 专项）+ breaks ×3（B32）
  + 裸锚点 ×2（M3 跟踪）——断链豁免清零已在射程内。

## 遗留与后续

- **B29（14 文件：cli 组 commands/reloading/proxy 等）需注入锚点以 registry 实测为准**
  （jakenHttpClient→proxy 的既有豁免随 proxy.adoc 落盘消解）；B30（appendix/architecture 4）+
  B31（faq/usingsnapshots/problems 3）+ B32（breaks + overloads 2）三批合计 9 文件即可完成全库初译；
- 本批次未触发 sync --apply（冻结窗口遵守）；`source/` 无写入。
