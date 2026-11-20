# 批次报告 B13

> 完成日期：2026-11-21 ｜ 执行：M2 第十三批次（串行 1，单会话编排方亲跑）

## 范围与规模

| 指标 | 值 |
|---|---|
| 文件数 | 17（httpServer：plainTextResponses/datavalidation 组 2/staticResources/errorHandling 组 8/apiVersioning/formData/form 组 3） |
| 总词数（当前 protect 后口径，实测） | 3122（M1 inventory 报告值 3185，口径见 reports/batch-B02.md） |
| 非代码词（当前口径，实测） | 3076（M1 inventory 报告值 3167） |
| 段落数 | 179（manifest paragraphs 合计） |
| 上游基线 | v5.2.25（tag，2026-11-17 发布；快照 `0b46d27afdfa`） |
| 最终状态 | 17 文件全部 current（manifest 388 条目中 143/388，进度 36.9%） |

双指标达标：非代码词 3076 ≤ 3500 且总词 3122 ≤ 5500。

## 流程执行（PLAN §5.1 SOP + 固化校验链）

1. protect：17 文件（占位符合计 145）；
2. 翻译：占位符逐个从 `-protected.txt`/映射表复制；`dependency:`/`dependency::` 宏 4 处逐字节保留
   （datavalidation/validationGroups）；formBinding 的未保护 `snippet::` 指令行
   （title 含 `Publisher<byte[]>` 泛型）逐字节保留；builtInExceptionHandlers 处理器表 13 行
   全部为宏单元格（仅表头译出「异常\|处理器」）；
   `<<validation,校验通知>>`（B10 已译批间消解）、`<<binding,请求绑定注解>>`（B11 已译）、
   `<<bindingUsingPOJOs,前面的 JSON 绑定代码>>`（B12 已译）目标逐字节保留 label 译出；
3. restore：17/17 哈希完整性全过（0 残留，restored 数与输入数核对一致）；
4. 溯源投影：`assemble_zh.py` 注入（translated_at=2026-11-21）；
5. reviewer 五项：段落对译 17/17 PASS（apiVersioning 27/27 段、formBinding 35/35 段为组长）；
6. validate：逐个 `--file` 首轮 15/17 全绿 + 2 项修正：
   errorFormatting ⑦ 邻接违规 ×1（`never`（ 占位符后漏空格）；
   apiVersioning ③ 必译术语缺失（interceptor——宏路径 `api:http.client.interceptor.configuration.…`
   误触，B10/B11 同类）——补「（客户端拦截器配置）」括注后通过；
   修正后 17/17 全绿；全量 143 文件 PASSED；
   ⑤ 豁免警告 27 条（26 → 27：whatsNew→form、whatsNew→formCapable 消解 −2；
   apiVersioning→clientAnnotation、errorFormatting→i18n、formData→httpClient 新增 +3）；
7. `--mark-current` 17/17 核销（hash+commit 双字段对账通过）；pytest 95 绿。

## 锚点注入（PLAN §5.6，B02 精化规则）

- `guide/httpServer/errorHandling/exceptionHandler.adoc` → `[[exceptionHandler]]`
  （被 errorFormatting 引用——**批内引用闭环**；errorFormatting 的 `<<exceptionHandler,异常处理器>>` 随之可达）
- `guide/httpServer/form.adoc` → `[[form]]`（被 whatsNew 引用，已译——落盘后豁免消解，批间闭环）
- `guide/httpServer/form/formCapable.adoc` → `[[formCapable]]`（被 whatsNew 引用，已译——落盘后豁免消解，批间闭环）
- 其余 14 文件未被登记引用，无注入。

## 术语滚动

- 本批无新增 glossary 条目；新首现括注（按首现处理，频次待后续复核）：校验组（validation groups）、
  局部/全局错误处理器（local/global error handler）、异常处理器（exception handler）、
  背压（backpressure，formBinding）；
- 既有术语命中：校验通知（<<validation,…>>）、拦截器（apiVersioning 括注补齐）、
  bean/类路径/内省、配置属性；banned 黑名单 0 命中（validate ③ 全量扫描）。

## 里程碑

httpServer 组（guide/httpServer/，101 文件）current 55/101（55%）。
整库进度 143/388（36.9%）。已全章译出：introduction、quickStart、IoC（55）、config（15）、AOP（10）。
errorHandling 组（8 文件）与 form 组（3 文件）全组 current；B14 将继续 filters/uploads 组。

## 遗留与后续

- 27 条 ⑤ 豁免警告登记于 validate 输出，M3 全量断链清零时一并处理；
- 本批次未触发 sync --apply（冻结窗口遵守）；`source/` 无写入；
- formBinding.adoc（43 段）为 httpServer 章目前最长文件之一，含 4 级标题链与未保护 snippet 行，
  对译检查通过后确认无返工。
