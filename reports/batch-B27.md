# 批次报告 B27

> 完成日期：2026-11-21 ｜ 执行：M2 第二十七批次（串行 1，单会话编排方亲跑；与 B21–B26 同会话接续）

## 范围与规模

| 指标 | 值 |
|---|---|
| 文件数 | 17（kotlinContextPropagation 1 + graal 组 3 + management 章 13） |
| 总词数（protect 后口径，实测） | 3469（M1 inventory 报告值 3538，口径基数差异以实测为准） |
| 非代码词（当前口径，实测） | 3399（M1 报告值 3478） |
| 段落数 | 273（inventory segments 口径，与既往批次 commit 口径一致） |
| 上游基线 | v5.2.25（tag，2026-11-17 发布；快照 `0b46d27afdfa`） |
| 最终状态 | 17 文件全部 current（manifest 388 条目中 340/388，进度 88.0%，剔 skipped 口径） |

双指标达标：非代码词 3399 ≤ 3500 且总词 3469 ≤ 5500。占位符合计 239
（最多 graalServices 44、occurrences 口径 63；graalServices 761 非代码词/78 段为批次最重）；
源文件无显式锚（ANCLINE 0 处）。

## 流程执行（PLAN §5.1 SOP + 固化校验链）

1. protect：17 文件（239 占位符）；
2. 翻译：kotlinContextPropagation（Reactor→协程上下文传播）、graal 章
   （GraalVM 入门/graalServices 原生镜像构建全流程/graalFAQ 四问）、management 章
   （章页/buildingEndpoints 组 5/providedEndpoints 组 7：端点注解、方法、敏感性、配置、
   默认端点表、beans/info/health 三端点及 health 配置/状态码/日志）；
   `<<contextPropagation,上下文传播 API>>`、`<<endpointConfiguration,端点配置>>` ×3、
   `<<providedEndpoints,内置端点>>`、`<<jmx,JMX>>`、`<<beansEndpoint,…>>` 等
   目标逐字节保留、label 译出；
3. restore：17/17 全过；assemble 落 zh/ 17 文件（translated_at=2026-11-21）；
4. validate：逐个 `--file` 13/17 首轮全绿，graalFAQ ⑦ 中英文缺空格 ×4、
   endpointMethod ⑦ ×3、endpointSensitivity ⑦ ×1、infoEndpoint ⑦ ×1 修复后 17/17 全绿；
5. **锚点注入 6 处（注入前核对 title 字段）**：`[[graal]]`（标题锚，「=== 入门」之前；
   被 serializationUsingJacksonDatabind 引用，已译——**消解既有豁免**）、
   `[[endpointConfiguration]]`（basename 锚，批内闭环）、`[[providedEndpoints]]`
   （标题锚「== 管理端口」，批内闭环）、`[[beansEndpoint]]`（标题锚「== 配置」）、
   `[[healthEndpoint]]`（basename 锚）、`[[infoEndpoint]]`（标题锚「== 配置」）——
   **beansEndpoint/infoEndpoint 首轮误置文件首，自查 registry title 后纠正为标题锚位置**
   （B23 教训二次生效）；落盘后 grep 核对 6/6 在位且位置正确；
6. reviewer 五项：/tmp/b27_reviewer.py **17/17 PASS 首轮零缺陷**（graalServices 52 段）；
7. `--mark-current` 17/17 核销；全量 340 文件 PASSED；pytest 95 绿。

## 术语滚动

- 本批无新增 glossary 条目；B22–B25 术语全章复用命中；
- 首现括注：健康指示器（health indicator）、活性检查（liveness check）、就绪检查（readiness check）、
  原生镜像（native image）、服务发现（Service Discovery）复现；
- banned 黑名单 0 命中。

## 里程碑与进度

- 整库进度 340/388（88.0%，剔 2 skipped）；**languageSupport 章 49/50（98%，仅剩 overloads 在 B32）**；
- management 章 12/27（44%）；**graal 组 3/3 全部译出**；
- ⑤ 豁免 11→11 条（**−1 消解**：serializationUsingJacksonDatabind→graal；
  **+1 新增**：providedEndpoints→stopEndpoint，B28 消解——净 0）。

## 遗留与后续

- **B28（21 文件：management 余 15 + security + multitenancy + cli 组 3）需注入锚点 8 处**
  （registry 实测）：`[[cli]]`（title='Interactive Mode'——标题锚；被 groovy/kotlin 引用，已译——
  **落盘后消解既有豁免 ×2**）、`[[cachesEndpoint]]`（basename 锚，批内闭环）、
  `[[environmentEndpoint]]`（标题锚，批内闭环）、`[[loggersEndpoint]]`（标题锚，批内闭环；
  其对 logging 的引用随 B21 锚点自动闭环）、`[[metricsEndpoint]]`（basename 锚，批内闭环）、
  `[[refreshEndpoint]]`/`[[routesEndpoint]]`/`[[stopEndpoint]]`（标题锚，批内闭环，
  stopEndpoint 消解 B27 新增豁免）；createProject→commandLineApps/serverlessFunctions、
  features→dataAccess 落盘即闭环（B20/B21 锚点在位）；
- ⑦ 邻接累计踩坑增至 30 次（本批 +5，含 URL 宏直贴汉字变体 4 处）；
- 本批次未触发 sync --apply（冻结窗口遵守）；`source/` 无写入。
