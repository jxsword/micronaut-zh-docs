# 批次报告 B10

> 完成日期：2026-11-21 ｜ 执行：M2 第十批次（串行 1，单会话编排方亲跑）

## 范围与规模

| 指标 | 值 |
|---|---|
| 文件数 | 5（AOP 章：lifecycleAdvice + interceptorLifecycle + validation + caching + retry） |
| 总词数（当前 protect 后口径，实测） | 3022（M1 inventory 报告值 3092，口径见 reports/batch-B02.md） |
| 非代码词（当前口径，实测） | 3002（M1 inventory 报告值 3086） |
| 段落数 | 140（manifest paragraphs 合计：31+26+8+26+49） |
| 上游基线 | v5.2.25（tag，2026-11-17 发布；快照 `0b46d27afdfa`） |
| 最终状态 | 5 文件全部 current（manifest 388 条目中 94/388，进度 24.2%） |

双指标达标：非代码词 3002 ≤ 3500 且总词 3022 ≤ 5500。

## 流程执行（PLAN §5.1 SOP + 固化校验链）

1. protect：5 文件（占位符合计 124：34+24+7+24+35）；
2. 翻译：占位符逐个从 `-protected.txt`/映射表复制；`dependency:…`/`dependency::…` 宏 3 处
   （validation ×3、retry ×1）逐字节保留；interceptorLifecycle 2 张表格（拦截类型/持有者）与
   caching `[NOTE] ====` 嵌套块（.缓存命名）结构保持；
   `<<interceptorLifecycle,拦截器生命周期>>` 与 `<<lifecycleAdvice,bean 生命周期通知>>`
   批内互引、目标逐字节保留 label 译出；
3. restore：5/5 哈希完整性全过（0 残留，restored 数与输入数核对一致）；
4. 溯源投影：`assemble_zh.py` 注入（translated_at=2026-11-21）；
5. reviewer 五项：段落对译首轮 4/5——**retry.adoc 漏注入 [[retry]] 锚点被 reviewer 抓出**（本批唯一
   真缺陷），补注入后重走 restore→assemble→mark-current，5/5 PASS（lifecycleAdvice 25/25 段、
   interceptorLifecycle 22/22 段等）；
6. validate：首轮 3/5 全绿 + caching ③ 必译术语缺失（interceptor：宏路径命中，补首现括注
   「CacheInterceptor（缓存拦截器）」）+ retry ⑦ 邻接违规 ×1（`` `Publisher`（ `` 占位符后漏空格）——
   修正后 5/5 全绿；全量 94 文件 PASSED；⑤ 豁免警告 23 条（25 → 23：whatsNew→retry、
   annotationMetadata→validation 因本批落盘消解 −2）；
7. `--mark-current` 5/5 核销（retry 补锚点后二次核销，hash+commit 双字段对账通过）；pytest 95 绿。

## 锚点注入（PLAN §5.6，B02 精化规则）

- `guide/aop/lifecycleAdvice.adoc` → `[[lifecycleAdvice]]`（被 interceptorLifecycle 引用——**批内互引闭环**）
- `guide/aop/interceptorLifecycle.adoc` → `[[interceptorLifecycle]]`（被 lifecycleAdvice 引用——**批内互引闭环**）
- `guide/aop/retry.adoc` → `[[retry]]`（被 whatsNew/clientFallback/clientRetry/clientSideLoadBalancing 引用；
  whatsNew 已译——落盘后豁免消解；首轮遗漏由 reviewer 抓出后补齐）
- `guide/aop/validation.adoc` → `[[validation]]`（被 annotationMetadata/datavalidation/javaInterfaces 引用；
  annotationMetadata 已译——落盘后豁免消解）
- caching.adoc 未被登记引用，无注入。

## 术语滚动

- 本批无新增 glossary 条目；新首现括注（按首现处理，频次待后续复核）：校验通知（validation advice）、
  缓存拦截器（CacheInterceptor）、weigher（权重计算器）、断路器（Circuit Breaker）、
  拦截类型（Interception Kinds，章内标题）；
- 既有术语命中：饿汉式初始化（lifecycleAdvice「eager initialization」）、拦截器/拦截器链、
  响应式（reactive types）、bean/工厂、编译期；CacheInterceptor 括注使 interceptor→拦截器 命中；
- banned 黑名单 0 命中（validate ③ 全量扫描）。

## 里程碑

AOP 章（guide/aop，10 文件）current 8/10（80%，余 scheduling/springAop）+ 章页 aop.adoc 已入账。
整库进度 94/388（24.2%）。已全章译出：introduction、quickStart、IoC（55）、config（15）。

## 遗留与后续

- 23 条 ⑤ 豁免警告登记于 validate 输出，M3 全量断链清零时一并处理；
- 本批次未触发 sync --apply（冻结窗口遵守）；`source/` 无写入；
- retry.adoc 首轮漏锚点教训：**锚点注入清单须在写译文前逐文件列出并在 Write 后立即自查**；
  reviewer 抓出后补救链路（补注入 → restore → assemble → mark-current 重跑）顺畅，门禁体系有效。
