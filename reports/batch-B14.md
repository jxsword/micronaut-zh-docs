# 批次报告 B14

> 完成日期：2026-11-21 ｜ 执行：M2 第十四批次（串行 1，单会话编排方亲跑）

## 范围与规模

| 指标 | 值 |
|---|---|
| 文件数 | 13（httpServer：serverIO + uploads + transfers + filters 组 10） |
| 总词数（当前 protect 后口径，实测） | 3410（M1 inventory 报告值 3476，口径见 reports/batch-B02.md） |
| 非代码词（当前口径，实测） | 3402（M1 inventory 报告值 3482） |
| 段落数 | 160（manifest paragraphs 合计） |
| 上游基线 | v5.2.25（tag，2026-11-17 发布；快照 `0b46d27afdfa`） |
| 最终状态 | 13 文件全部 current（manifest 388 条目中 156/388，进度 40.2%） |

双指标达标：非代码词 3402 ≤ 3500 且总词 3410 ≤ 5500。

## 流程执行（PLAN §5.1 SOP + 固化校验链）

1. protect：13 文件（占位符合计 148）；
2. 翻译：占位符逐个从 `-protected.txt`/映射表复制；serverIO 响应类型表 2 组 8 行仅译描述列；
   filterPatterns 模式匹配表与 errorStates 过滤器声明表仅译单元格；uploads 大文件
   （42 段、`transferTo(File)`/`transferTo(OutputStream)` 两组 callout）；
   `<<threadPools,服务器线程池>>`、`<<httpServerFilter,…>>`/`<<filtermethods,过滤器方法>>`
   批内互引目标逐字节保留 label 译出；
3. restore：13/13 哈希完整性全过（0 残留，restored 数与输入数核对一致）；
4. 溯源投影：`assemble_zh.py` 注入（translated_at=2026-11-21）；
5. reviewer 五项：段落对译 13/13 PASS（uploads 31/31 段、serverIO 27/27 段为组长）；
6. validate：逐个 `--file` 首轮 12/13 全绿 + transfers ⑦ 邻接违规 ×2
   （`` `304`（ `` 与 `` *响应式流*（ ``——加粗标记同样受 `[*_~]（` 约束）修正后 13/13 全绿；
   全量 156 文件 PASSED；⑤ 豁免警告 26 条（27 → 26：whatsNew→order、whatsNew→uploads
   消解 −2；serverIO→threadPools 新增 +1）；
7. `--mark-current` 13/13 核销（hash+commit 双字段对账通过）；pytest 95 绿。

## 锚点注入（PLAN §5.6，B02 精化规则）

- `guide/httpServer/uploads.adoc` → `[[uploads]]`（被 whatsNew 引用，已译——落盘后豁免消解，批间闭环）
- `guide/httpServer/filters.adoc` → `[[filters]]`（被 clientFilter/proxyClient 引用，未译豁免承接）
- `guide/httpServer/filters/filtermethods.adoc` → `[[filtermethods]]`（被 filters.adoc/httpServerFilter.adoc
  引用——**批内引用闭环**）
- `guide/httpServer/filters/filtermethods/order.adoc` → `[[order]]`（被 whatsNew 引用，已译——落盘后豁免消解）
- `guide/httpServer/filters/httpServerFilter.adoc` → `[[httpServerFilter]]`（被 filters.adoc 引用——**批内引用闭环**）
- 其余 8 文件未被登记引用，无注入。

## 术语滚动

- 本批无新增 glossary 条目；新首现括注（按首现处理，频次待后续复核）：流式上传/完成上传
  （streaming/completed uploads）、部件（part，uploads）、背压复现（serverIO/transfers）、
  管道断裂（broken pipe，transfers）；
- 既有术语命中：响应式（reactiveServer/serverIO 高频）、过滤器（filter 组高频）、
  编解码器（codec，uploads）、bean/内省未出现；banned 黑名单 0 命中（validate ③ 全量扫描）。

## 里程碑

httpServer 组（guide/httpServer/，101 文件）current **59/101（58%）**（B11 4 + B12 25 + B13 17 + 本批 13）。
整库进度 156/388（40.2%），进度破 40%。
已全章译出：introduction、quickStart、IoC（55）、config（15）、AOP（10）。
filters 子目录（filterPatterns/filtermethods 组 7 + httpServerFilter 组 2）全组 current。

> 口径勘误：B13 报告曾将 progress 行 missing 列误读为 current（写作「55/101（55%）」），
> B13 实际组内进度应为 46/101（46%）；本报告已按正确列位修正，并回改 B13 报告与看板。

## 遗留与后续

- 26 条 ⑤ 豁免警告登记于 validate 输出，M3 全量断链清零时一并处理；
- 本批次未触发 sync --apply（冻结窗口遵守）；`source/` 无写入；
- uploads.adoc（42 段、148 占位符中的 40+）为 httpServer 章最长文件，对译检查通过后确认无返工；
- transfers ⑦ 邻接证明 **加粗标记 `*` 与反引号同样受「标记后不得紧跟全角开括号」约束**，
  翻译期占位符与 `*…*` 结束后接 `（` 一律预留空格。
