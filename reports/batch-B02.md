# 批次报告 B02

> 完成日期：2026-11-21 ｜ 执行：M2 第二批次（串行 1，单会话编排方亲跑）

## 范围与规模

| 指标 | 值 |
|---|---|
| 文件数 | 12（IoC Injection 子节 4 + Types/Qualifiers/Typed 3 + Scopes 5） |
| 总词数（当前 protect 后口径，实测） | 3055（M1 inventory 报告值 3082，差异原因见下「词数口径」） |
| 非代码词（当前口径，实测） | 2991（M1 inventory 报告值 3049） |
| 段落数 | 207（manifest paragraphs 合计） |
| 上游基线 | v5.2.25（tag，2026-11-17 发布；快照 `0b46d27afdfa`） |
| 最终状态 | 12 文件全部 current（manifest 388 条目中 31/388，进度 8.0%） |

双指标达标：非代码词 2991 ≤ 3500 且总词 3055 ≤ 5500。

## 词数口径差异（记录，不阻断）

M1 inventory 报告值（3082/3049）生成于 B01 的 `snippet::` 指令行保护修复
**之前**；B01 修复后 snippet 行计 1 词而原口径按宏参数逐词计数。按当前
inventory.py 口径复算本批为 3055/2991。后续批次词数以「批次执行时实测」
为准并在报告注明；M1 报告值仅作切分参考。

## 流程执行（PLAN §5.1 SOP + B01 固化校验链）

1. protect：12 文件生成受保护文本 + 映射表（占位符合计 206）；
2. 翻译：占位符逐字节保留；`<<anchor,label>>` 目标保留、label 译出；
   表格仅译单元格文本；代码块（含 CODEBLOCK 占位符整块）逐字节不动；
3. restore：12 文件哈希完整性校验全过（无残留/无丢失）；
4. 溯源投影：`assemble_zh.py` 注入页头引用块 + HTML 注释四字段
   （页名取 toc.yml 英文原题，URL 锚点 `core-<basename>`，translated_at=2026-11-21）；
5. reviewer 五项：段落对照 12/12 一致且 0 漏译（逐段 zip + 停用词检测；
   剔除页头溯源段与 `[[…]]` 锚点注入段后段数全等）；
6. validate：先 12 文件 `--file` 全绿，后全量 31 文件 PASSED；
   ⑤ 豁免警告 29 条（28 → 29：whatsNew→types 因本批目标落盘而消解 −1，
   nullableInjection→valueAnnotation、eagerInit→serverlessFunctions 新增 +2）；
7. `--mark-current` 12/12 核销（溯源 hash+commit 双字段对账通过）。

## 锚点注入（PLAN §5.6）

登记表中以 B02 文件为目标的锚点 4 条，全部按块锚注入**文件首（第一内容之前）**：

- `guide/ioc/types.adoc` → `[[types]]`（被 guide/introduction/whatsNew.adoc 引用）
- `guide/ioc/qualifiers.adoc` → `[[qualifiers]]`（被 constructorInjection.adoc、annotationMetadata.adoc 引用）
- `guide/ioc/scopes.adoc` → `[[scopes]]`（被 annotationMetadata/factories/lifecycle 引用）
- `guide/ioc/scopes/refreshable.adoc` → `[[refreshable]]`（被 immutableConfig.adoc 引用）

**注入位置规则精化（轻量决策，不立 DR）**：B01 的「无标题片段注入文件首 /
有标题片段注入标题上方」两种表述，在 upgrading.adoc（首行即标题）上无法区分。
本批确认统一规则：**basename 约定锚点 = 官方站 `core-<basename>` = 片段首内容
之前的块锚**——对首行即标题的文件等同于「标题上方」，对正文先行的文件
（qualifiers/types/scopes/refreshable）注入于第一段之前，使锚点覆盖整个片段
（上游 `<<qualifiers,Qualifiers>>` 语义指向整个 Qualifiers 小节，含标题前导语）。

## 官方站锚点

复用 B01 实测结论（`core-<basename>`、子标题 auto-id `core-_xxx_yyy`），本批未
重新抓取 11.4MB 大页；四文件页头 URL 均按该格式生成。

## 缺陷修复（本批次实测发现，已补回归测试）

1. **validate_translation.py ③ strip_code 未剔指令行**：`snippet::` 宏参数
   （如 `io.micronaut.docs.inject.qualifiers.named.V8Engine`）包含
   `qualifier` 子串，术语转正 qualifier 后触发「③ 必译术语缺失」误报。
   修复：strip_code 增加指令行剔除（复用 segment_adoc.RE_DIRECTIVE），
   指令行本身受 ② 逐字节门禁保护、非散文，不参与 ③④⑦ 匹配。
   回归测试 `test_check3_directive_line_not_prose`；pytest 94 → 95 全绿。

## 术语滚动（先写回再继续）

**转正 glossary.yml（status: approved，3 条）**：

- `qualifier → 限定符`（qualifiers.adoc 全章 + constructorInjection/types 等高频）
- `eager initialization → 饿汉式初始化`（aliases: eagerly initialize / eager init）
- `meta annotation → 元注解`（aliases: meta-annotation）

**评估后不入表**：`scope → 作用域`——substring 机检会命中 whatsNew.adoc 的
"scoped values"（JDK ScopedValue API 术语，不译「作用域值」），追溯性误伤；
「作用域」作为工作约定继续使用，不设机检强制。

B01 遗留复核项「qualifier/eager initialization 是否转正」在本批闭环；
context propagation（B01 whatsNew 首现括注）暂无新增命中文件，维持待复核。

## 轻量决策汇总（均记录于上两节，不立 DR）

1. 锚点注入位置统一为「片段首内容之前」；
2. 词数以批次执行时实测口径为准；
3. scope 不入 glossary 机检、保留工作约定。

## 遗留与后续

- 29 条 ⑤ 豁免警告登记于 validate 输出，M3 全量断链清零时一并处理；
- 本批次未触发 sync --apply（冻结窗口遵守）；工作目录无 `source/` 写入；
- 临时脚本 `/tmp/review_b02.py`（reviewer 段落对照）不入库，方法已记录于本报告。
