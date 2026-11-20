# 批次报告 B26

> 完成日期：2026-11-21 ｜ 执行：M2 第二十六批次（串行 1，单会话编排方亲跑；与 B21–B25 同会话接续）

## 范围与规模

| 指标 | 值 |
|---|---|
| 文件数 | 14（asyncio 组 3 + kotlin 章 11） |
| 总词数（protect 后口径，实测） | 3407（M1 inventory 报告值 3439，口径基数差异以实测为准） |
| 非代码词（当前口径，实测） | 3379（M1 报告值 3416） |
| 段落数 | 160（inventory segments 口径，与既往批次 commit 口径一致） |
| 上游基线 | v5.2.25（tag，2026-11-17 发布；快照 `0b46d27afdfa`） |
| 最终状态 | 14 文件全部 current（manifest 388 条目中 323/388，进度 83.7%，剔 skipped 口径） |

双指标达标：非代码词 3379 ≤ 3500 且总词 3407 ≤ 5500。占位符合计 269
（最多 asyncioNetworking 116、occurrences 口径 147——asyncioNetworking 1215 非代码词/25 段
为 python 章最重文件）；源文件无显式锚（ANCLINE 0 处）。

## 流程执行（PLAN §5.1 SOP + 固化校验链）

1. protect：14 文件（269 占位符）；
2. 翻译：asyncioNetworking（地址族与名称解析/服务器契约/传输/错误校验/回调与关闭/
   传输选择/TLS/附加信息八节）、asyncioStreaming（as_async_iterable/as_publisher/
   异步生成器路由三节）、asyncioUnsupported（未实现 API 清单）、kotlin 章
   （kaptOrKsp/kapt/ksp/controller/kaptintellij/gradlekapt/openandaop/kotlinretainparamnames/
   coroutines/coroutineTracingContextPropagation）；
   `<<cli,命令行界面>>`、`<<aop,AOP 通知>>`、`<<incrementalannotationgradle,Gradle 增量注解处理>>`
   目标逐字节保留、label 译出；`____` 引用块占位符（kaptOrKsp/ksp）保留；
3. restore：14/14 全过；assemble 落 zh/ 14 文件（translated_at=2026-11-21）；
4. **占位符多重集校验拦截 2 处真缺陷（restore 之前）**：asyncioNetworking 与 kapt 各多写 1 个
   占位符出现（原文复指「one/a」处不该重复占位符）——修正后多重集一致，restore 14/14 首轮全过；
5. validate：逐个 `--file` 11/14 首轮全绿，asyncioNetworking ⑦ ×1、asyncioUnsupported ⑦ ×1、
   kaptintellij ⑦ 中英文缺空格 ×1（「完全{{URL}}[...]」）修复后 14/14 全绿；
6. 锚点注入 2 处（注入前核对 title 字段，均页内标题锚）：`[[asyncioNetworking]]`
   （注入「== 地址族与名称解析」之前；被 asyncAwait 引用，已译——消解 B25 新增豁免）、
   `[[asyncioStreaming]]`（注入「== 以 async for 消费 Publisher」之前；被 asyncAwait 引用（消解）
   + asyncioUnsupported **批内闭环**）；落盘后 grep 核对 2/2 在位；
7. reviewer 五项：/tmp/b26_reviewer.py **14/14 PASS 首轮零缺陷**（asyncioNetworking 23 段）；
8. `--mark-current` 14/14 核销；全量 323 文件 PASSED；pytest 95 绿。

## 术语滚动

- 本批无新增 glossary 条目；B22–B25 术语全章复用命中；
- 首现括注：水位线（water mark，Netty 写缓冲语境）、冷（cold，Publisher 语境）、
  存根（stub）复现、及时（eagerly，任务启动语境）；
- banned 黑名单 0 命中。

## 里程碑与进度

- 整库进度 323/388（83.7%，剔 2 skipped）；languageSupport 章 45/50（90%），
  余 5 文件（graal 组 3 + kotlinContextPropagation 在 B27，overloads 在 B32）；
- **kotlin 子章 14/14 全章译出**（kotlin 章页 + 13 子文件，第十五个全章组）；
- asyncio 组 6/6 全部译出（asyncAwait + asyncioRuntime/Networking/Streaming/Unsupported）；
- ⑤ 豁免 11→11 条（**−2 消解**：asyncAwait→asyncio{Networking,Streaming}；
  **+1 新增**：kotlin→cli——cli 在 B28；净 0）。

## 遗留与后续

- **B27（17 文件：kotlinContextPropagation + graal 组 3 + management 章 13）需注入锚点 6 处**
  （registry 实测）：`[[graal]]`（title='Getting Started'——标题锚；被 breaks ×2（未译豁免承接）+
  serializationUsingJacksonDatabind 引用，已译——**落盘后消解既有豁免**）、
  `[[endpointConfiguration]]`（title 空——basename 锚，被 endpointAnnotation 批内闭环）、
  `[[providedEndpoints]]`（title='Management Port'——标题锚，被 buildingEndpoints 批内闭环）、
  `[[beansEndpoint]]`（title='Configuration'——标题锚，被 providedEndpoints 批内闭环）、
  `[[healthEndpoint]]`（title 空——basename 锚，被 providedEndpoints 批内闭环）、
  `[[infoEndpoint]]`（title='Configuration'——标题锚，被 providedEndpoints 批内闭环）；
  jmx→providedEndpoints（B09 在位）、kotlinContextPropagation→contextPropagation（B19 在位）
  落盘即闭环；
- **新错误模式（多重集校验拦截）**：原文复指（"a `sendto` after that, or one whose..."）
  处翻译时不得重复占位符——译文用代词/名词回指，占位符只出现一次；
- ⑦ 邻接累计踩坑增至 25 次（本批 +3，含 1 次中英文缺空格变体）；
- 本批次未触发 sync --apply（冻结窗口遵守）；`source/` 无写入。
