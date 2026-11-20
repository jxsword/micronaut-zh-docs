# 批次报告 B25

> 完成日期：2026-11-21 ｜ 执行：M2 第二十五批次（串行 1，单会话编排方亲跑；与 B21–B24 同会话接续）

## 范围与规模

| 指标 | 值 |
|---|---|
| 文件数 | 7（python 子组：aopProxies/extendingJavaClasses/moduleScripts+testing/graalTools/asyncAwait/asyncioRuntime） |
| 总词数（protect 后口径，实测） | 2996（M1 inventory 报告值 3070，差异为口径统计基数所致，以实测为准） |
| 非代码词（当前口径，实测） | 3007（M1 报告值 3096） |
| 段落数 | 111（inventory segments 口径，与既往批次 commit 口径一致） |
| 上游基线 | v5.2.25（tag，2026-11-17 发布；快照 `0b46d27afdfa`） |
| 最终状态 | 7 文件全部 current（manifest 388 条目中 309/388，进度 80.1%，剔 skipped 口径） |

双指标达标：非代码词 3007 ≤ 3500 且总词 2996 ≤ 5500。占位符合计 166
（最多 asyncAwait 47，其中 snippet:: 指令行 11 处逐字节保留）；extendingJavaClasses
1082 非代码词为本批最重；源文件无显式锚（ANCLINE 0 处）。

## 流程执行（PLAN §5.1 SOP + 固化校验链）

1. protect：7 文件（166 占位符）；
2. 翻译：aopProxies（AOP 通知/隐式校验/关键字实参/self 调用分发规则六条）、
   extendingJavaClasses（继承 Java 类全生命周期：受检异常/工作原理/局限六条）、
   moduleScripts+testing（模块级注解与 JUnit 5 模块测试）、graalTools（CPU 采样器/
   Chrome 检查器/调试适配协议）、asyncAwait（协程桥接/await 语义/Publisher 单条目/
   订阅适配/结构化并发）、asyncioRuntime（Netty 事件循环集成/优雅关闭/事件循环 API 清单）；
   `<<aop,AOP 通知>>`、`<<extendingJavaClasses,继承 Java 类>>`、`<<validation,校验>>`、
   `<<reflection,反射模块>>`、`<<asyncioNetworking>>`/`<<asyncioStreaming>>`（无 label 短格式，
   B20 `<<bootstrap>>` 先例）目标逐字节保留；
3. restore：7/7 首轮全过；assemble 落 zh/ 7 文件（translated_at=2026-11-21）；
4. validate：逐个 `--file` 4/7 首轮全绿，aopProxies ⑦ ×1、asyncioRuntime ⑦ ×2、
   **graalTools ④ ×2（标题未译——「Chrome Inspector」「Debug Adapter Protocol」为工具名，
   补译「Chrome 检查器（Chrome Inspector）」「调试适配协议（Debug Adapter Protocol）」）**，
   修复后 7/7 全绿；
5. 锚点注入 2 处（注入前核对 title 字段）：`[[extendingJavaClasses]]` 页内标题锚
   （title='Checked exceptions'，注入「== 受检异常（Checked exceptions）」之前；被 javaInterfaces
   引用，已译——落盘后消解 B24 新增豁免）；`[[moduleScripts]]` basename 片段锚
   （title 空，注入文件首内容之前；被 httpServer/routing 引用，已译——**消解既有豁免**）；
   落盘后 grep 核对 2/2 在位；
6. reviewer 五项：/tmp/b25_reviewer.py **7/7 PASS 首轮零缺陷**（extendingJavaClasses 17 段）；
7. `--mark-current` 7/7 核销；全量 309 文件 PASSED；pytest 95 绿。

## 术语滚动

- 本批无新增 glossary 条目；B22–B24 术语全章复用命中；
- 首现括注：元数（arity）复现、宿主适配器（host adapter）复现、结构化并发（structured concurrency）、
  Chrome 检查器（Chrome Inspector）、调试适配协议（Debug Adapter Protocol）、CPU 采样器（CPU sampler）；
- ④ 新案例：工具/协议专名标题不能保留英文原题，须译名+括注（validate ④ 硬门禁）；
- banned 黑名单 0 命中。

## 里程碑与进度

- 整库进度 309/388（80.1%，剔 2 skipped）；languageSupport 章 31/50（62%）；
- **python 子章 24/24 全部译出（第十四个全章：python 章页 + 23 子文件）**；
  languageSupport 余 19 文件：kotlin 组 14 + graal 组 3 + overloads 1（B26–B27 + B32）；
- ⑤ 豁免 11→11 条（**−2 消解**：javaInterfaces→extendingJavaClasses、routing→moduleScripts；
  **+2 新增**：asyncAwait→asyncio{Networking,Streaming}，B26 消解——净 0）。

## 遗留与后续

- **B26（14 文件：asyncio 组 3 + kotlin 组 11）需注入锚点 2 处**（registry 实测，均为标题锚）：
  `[[asyncioNetworking]]`（title='Address families and name resolution'；被 asyncAwait 引用，
  已译——落盘后消解）、`[[asyncioStreaming]]`（title='Consuming a Publisher with async for'；
  被 asyncAwait 引用（消解）+ asyncioUnsupported 批内闭环）；openandaop→aop（B09 在位）、
  gradlekapt→incrementalannotationgradle（B21 在位）落盘即闭环；kotlin→cli（cli 未译）+1 新豁免；
- commit message 含反引号内容时必须用 `git commit -F <文件>` 提交（B24 曾因命令替换吞字，
  已 amend 修复）；
- 本批次未触发 sync --apply（冻结窗口遵守）；`source/` 无写入。
