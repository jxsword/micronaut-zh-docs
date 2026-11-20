# 批次报告 B21

> 完成日期：2026-11-21 ｜ 执行：M2 第二十一批次（全程最大批次，串行 1，单会话编排方亲跑，逐组推进）

## 范围与规模

| 指标 | 值 |
|---|---|
| 文件数 | 35（azureFunction 1 + messaging 组 4 + commandLineApps 组 2 + configurations/reactiveConfigs 组 4 + dataAccess 组 10 + logging 组 5 + languageSupport/java 组 7 + groovy/python 章页 2） |
| 总词数（protect 后口径，实测） | 3078（与 M1 inventory 报告值 3078 一致） |
| 非代码词（当前口径，实测） | 2983（与 M1 inventory 报告值 2983 一致） |
| 段落数 | 298（inventory segments 口径，与既往批次 commit 口径一致） |
| 上游基线 | v5.2.25（tag，2026-11-17 发布；快照 `0b46d27afdfa`） |
| 最终状态 | 35 文件全部 current（manifest 388 条目中 286/388，进度 74.1%，剔 skipped 口径） |

双指标达标：非代码词 2983 ≤ 3500 且总词 3078 ≤ 5500。占位符合计 227
（最多 groovy 43、dataAccess 28）；源文件无显式锚（ANCLINE 0 处，grep/map 双重核实）。

## 流程执行（PLAN §5.1 SOP + 固化校验链）

1. protect：35 文件一次全量保护（227 占位符）；
2. 翻译：逐组推进（8 组）；占位符逐个从 `-protected.txt` 复制并回读核对；
   `dependency:`/`dependency::` 宏行与 `<<aop,…>>`/`<<serverlessFunctions,…>>` 目标逐字节保留、
   label 译出；`*before*` 加粗、表格 `|`/`|===`、`.标题`、`<1>` callout 等结构按纪律保留；
   中文语序导致 6 文件占位符出现顺序与源不同（多重集一致，restore/validate 均只要求哈希多重集，
   /tmp/b21_phcheck.py 改为多重集校验 + 顺序差异仅提示）；
3. restore：35/35 哈希完整性首轮全过（0 残留，restored 文件数 = 输入文件数 35）；
   B20 的「复制后回读核对花括号」习惯生效，本批未再出现丢花括号；
4. 溯源投影：`assemble_zh.py` 注入（translated_at=2026-11-21），zh 落盘 35 文件；
5. reviewer 五项：/tmp/b21_reviewer.py（b20 模板 + sqlSupport 标题锚位置检查适配）
   **35/35 PASS 首轮零缺陷**；段落对齐 groovy 35/35 段为组长；
6. validate：逐个 `--file` 33/35 首轮全绿，2 处命中已知错误模式并即时修复——
   mongoSupport ③（Reactive Streams→响应式流物化）、java9 ⑦（占位符后漏空格）；
   修复后 35/35 全绿；全量 286 文件 PASSED；
7. `--mark-current` 35/35 核销（hash+commit 双字段对账通过）；pytest 95 绿。

## 锚点注入（PLAN §5.6，B02 精化规则，registry 实测 7 处）

- `guide/commandLineApps.adoc` → `[[commandLineApps]]`（被 cli/createProject 引用，未译豁免承接）
- `guide/configurations/dataAccess.adoc` → `[[dataAccess]]`（被 cli/features 引用，未译豁免承接）
- `guide/configurations/dataAccess/hibernateSupport.adoc` → `[[hibernateSupport]]`（被 aop/springAop 引用，已译——落盘后豁免消解）
- `guide/configurations/dataAccess/sqlSupport.adoc` → `[[sqlSupport]]`（页内标题锚，位于 `== 配置 JDBC DataSource` 标题行之前；被 hibernateSupport 引用——**批内引用闭环**）
- `guide/languageSupport.adoc` → `[[languageSupport]]`（被 appendix/problems 引用，未译豁免承接）
- `guide/languageSupport/java/incrementalannotationgradle.adoc` → `[[incrementalannotationgradle]]`（被 kotlin/gradlekapt 引用，未译豁免承接）
- `guide/logging.adoc` → `[[logging]]`（被 ioc/conditionalBeans 引用，已译——落盘后豁免消解；loggersEndpoint 未译豁免承接）
- 其余 28 文件未被登记引用，无注入。
- 合计 **7 处注入**（5 basename 片段锚 + 2 标题锚）；注入后逐文件 grep 核对 zh 实际在位（B16 教训）。

## 术语滚动

- 新增 glossary 2 条（approved）：消息代理（message broker）、发布者确认（publisher confirms）——
  首现括注于 rabbitmq.adoc；glossary 现 25 术语 / 6 禁用；
- 首现括注：消息驱动（message-driven）、连接池（connection pool）、
  日志系统（logging system）、领域特定语言（Domain Specific Language）、
  Gradle 增量注解处理（Gradle incremental annotation processing）、响应式流（Reactive Streams）物化；
- **CLI 语境 feature 保留不译**口径复核：本批 sqlSupport/hibernateSupport/mongoSupport/
  neo4jSupport/postgresSupport/redisSupport/cassandraSupport/groovy 8 文件 feature 一律保留，
  与 B20 Consul 一致；
- 既有术语命中：编译期 AOP（banned「编译时间」0 命中）、响应式、元注解、内省、
  类路径、通知（advice→通知，`<<aop,自定义 AOP 通知>>`）、Serverless、Netty 不涉及；
- banned 黑名单 0 命中（validate ③ 全量扫描）。

## 里程碑

**五个组全章译出**（第九至第十三个全章）：
- **serverlessFunctions 4/4**（azureFunction 收尾，第九个全章）
- **messaging 全章**（messaging.adoc + kafka/rabbitmq/nats 3/3）
- **commandLineApps 全章**（commandLineApps.adoc + picocli 1/1）
- **configurations 全章**（configurations.adoc + reactiveConfigs 组 3 + dataAccess 组 10，13/13）
- **logging 全章**（logging.adoc + logging 组 4/4）

整库进度 286/388（74.1%，剔 2 skipped）；languageSupport 章 8/50 起步（java 组 6 + groovy/python 章页）。

## ⑤ 豁免增减明细

11 → 10 条（**−2 消解**：springAop→hibernateSupport、conditionalBeans→logging，
均为 B20 交接预测并兑现；**+1 新增**：groovy→cli（cli.adoc 未译，锚点已登记））。
其余 8 条承接不变，M3 全量断链清零时处理。

## 遗留与后续

- 10 条 ⑤ 豁免警告登记于 validate 输出；其中 2 条裸锚点 M3 跟踪项不变；
- 本批次未触发 sync --apply（冻结窗口遵守）；`source/` 无写入；
- 下一批 B22（5 文件：languageSupport/python 子组 pythonRuntime 等）为 python 章 24 文件系列的第一批，
  languageSupport 章剩余 42 文件横跨 B22–B27；
- groovy.adoc 59 占位符/53 段为全程单文件占位符次高，结构复杂（表格+交互模式输出块），
  翻译期占位符多重集校验 + restore 门禁双保险有效。
