# 批次报告 B19

> 完成日期：2026-11-21 ｜ 执行：M2 第十九批次（串行 1，单会话编排方亲跑）

## 范围与规模

| 指标 | 值 |
|---|---|
| 文件数 | 14（httpClient 客户端注解余下 9 + certificates + contextPropagation 组 3 + cloud 章页） |
| 总词数（当前 protect 后口径，实测） | 3471（M1 inventory 报告值 3491，口径见 reports/batch-B02.md） |
| 非代码词（当前口径，实测） | 3424（M1 inventory 报告值 3455） |
| 段落数 | 199（manifest paragraphs 合计） |
| 上游基线 | v5.2.25（tag，2026-11-17 发布；快照 `0b46d27afdfa`） |
| 最终状态 | 14 文件全部 current（manifest 388 条目中 230/388，进度 59.3%） |

双指标达标：非代码词 3424 ≤ 3500 且总词 3471 ≤ 5500。

## 流程执行（PLAN §5.1 SOP + 固化校验链）

1. protect：14 文件（占位符合计 139）；
2. 翻译：占位符逐个从 `-protected.txt`/映射表复制；certificates 源内显式锚
   `[[certificates]]`（ANCLINE 占位符）逐字节保留；`dependency:`/`dependency::` 宏 3 处逐字节保留；
   `<<retry,重试通知>>`（B10 已译批间消解）、`<<clientFilter,客户端过滤器>>`（本批批内闭环）、
   `<<filters,服务器过滤器文档>>`（B14 已译）目标逐字节保留 label 译出；
3. restore：首轮 clientFilter 门禁拦截译丢段（`snippet::` 指令占位符缺失，第 4 次拦截真缺陷），
   补齐后 14/14 哈希完整性全过（0 残留）；
4. 溯源投影：`assemble_zh.py` 注入（translated_at=2026-11-21）；
5. reviewer 五项：段落对译 14/14 PASS（contextPropagation 31/31 段为组长）；
   脚本新增 SOURCE_EXPLICIT_ANCHOR 核对（源内显式锚保留检查）；
6. validate：逐个 `--file` 首轮 11/14 全绿 + nettyPooling ⑦ ×4、contextPropagation ⑦ ×2
   （均占位符/加粗后漏空格）+ certificates ③ classpath→类路径（正文物化）修正后 14/14 全绿；
   全量 230 文件 PASSED；⑤ 豁免警告 18 条（22 → 18：https→certificates ×2、whatsNew→clientHttp3、
   whatsNew→contextPropagation 共 −4 消解，无新增）；
7. `--mark-current` 14/14 核销（hash+commit 双字段对账通过）；pytest 95 绿。

## 锚点注入（PLAN §5.6，B02 精化规则）

- `guide/httpClient/clientFilter.adoc` → `[[clientFilter]]`（被 clientHeaders 引用——**批内引用闭环**）
- `guide/httpClient/clientHttp3.adoc` → `[[clientHttp3]]`（被 whatsNew 引用，已译——落盘后豁免消解，批间闭环）
- `guide/contextPropagation.adoc` → `[[contextPropagation]]`（被 breaks/whatsNew/kotlinContextPropagation 引用；
  whatsNew 已译——落盘后豁免消解；breaks/kotlinContextPropagation 未译豁免承接）
- `guide/certificates.adoc` 源内已有显式锚 `[[certificates]]` 经 ANCLINE 占位符保留
  （https.adoc 引用的 2 条豁免随之消解——批间闭环）
- 其余 10 文件未被登记引用，无注入。

## 术语滚动

- 本批无新增 glossary 条目；新首现括注（按首现处理，频次待后续复核）：传播上下文（Propagated Context）、
  连接池复现（nettyPooling 连接池/待处理请求队列/待处理连接）、证书提供者复现、
  fallback（保留，clientFallback 高频）、访问日志未涉及；
- 既有术语命中：类路径（classpath 正文物化命中）、重试/断路器（clientRetry）、
  响应式（contextPropagation/reactor）、bean/内省（@Introspected）、MDC（保留）；
- banned 黑名单 0 命中（validate ③ 全量扫描）。

## 里程碑

**httpClient 章（guide/httpClient，26 文件）全部 current——httpClient 全章译出**
（第七个全章：introduction、quickStart、IoC、config、AOP、httpServer、httpClient）。
contextPropagation 组 2/2 全组 current；cloud 章 1/17 起步（章页 cloud.adoc）。
整库进度 230/388（59.3%）。

## 遗留与后续

- 18 条 ⑤ 豁免警告登记于 validate 输出，M3 全量断链清零时一并处理；
- 本批次未触发 sync --apply（冻结窗口遵守）；`source/` 无写入；
- restore 译丢段门禁第四次拦截真缺陷（clientFilter 漏 snippet 占位符）——门禁体系持续有效；
- contextPropagation.adoc（50 段）为 Propagated Context API 长文件（5.0 新特性），对译检查通过后确认无返工。
