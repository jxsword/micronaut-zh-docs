# 批次报告 B08

> 完成日期：2026-11-21 ｜ 执行：M2 第八批次（串行 1，单会话编排方亲跑）

## 范围与规模

| 指标 | 值 |
|---|---|
| 文件数 | 4（config 章：evaluatedExpressions + configurationProperties + customTypeConverter + eachProperty） |
| 总词数（当前 protect 后口径，实测） | 3400（M1 inventory 报告值 3442，口径见 reports/batch-B02.md） |
| 非代码词（当前口径，实测） | 3336（M1 inventory 报告值 3397） |
| 段落数 | 260（manifest paragraphs 合计：141+93+12+14） |
| 上游基线 | v5.2.25（tag，2026-11-17 发布；快照 `0b46d27afdfa`） |
| 最终状态 | 4 文件全部 current（manifest 388 条目中 81/388，进度 20.9%） |

双指标达标：非代码词 3336 ≤ 3500 且总词 3400 ≤ 5500。

## 流程执行（PLAN §5.1 SOP + 固化校验链）

1. protect：4 文件（占位符合计 212：89+87+13+23）；
2. 翻译：占位符逐个从 `-protected.txt`/映射表复制；`snippet::` 宏 10 处与 `include::` 指令 2 处
   （evaluatedExpressions 上下文示例）经占位符保护逐字节保留；
   `link:{jdkapi}/…[LocalDate]` 与 `link:{api}/…` label 保留英文原名；
   `[NOTE] ====` 嵌套块 + 内嵌 `~~~` 小标题（YAML 保留字）结构保持、标题文本译出；
   表格仅译单元格（时长转换/可读字节 2 张表）；裸代码行 `List<Integer> integers;` 等逐字节保留；
3. restore：4/4 哈希完整性全过（0 残留，restored 数与输入数核对一致）；
4. 溯源投影：`assemble_zh.py` 注入（translated_at=2026-11-21）；
5. reviewer 五项：段落对译 4/4 PASS（evaluatedExpressions 94/94 段、configurationProperties 69/69 段、
   customTypeConverter 9/9、eachProperty 10/10）；首轮命中 1 条为 reviewer 脚本误报
   （`Dependency Injection` 位于 snippet:: 指令行 title 参数，validate ② 设计要求逐字节保留，
   B02 已修复 validate ③ 同类误报）——脚本检查范围修正为仅查可译段后 4/4 PASS；
6. validate：4 文件 `--file` 全绿（configurationProperties 首轮 ⑦ 邻接违规 ×2——
   `MapTransformation.FLAT`（/`NESTED`（ 占位符后漏空格，补空格重跑 restore/assemble 后通过）；
   全量 81 文件 PASSED；⑤ 豁免警告 27 条（32 → 27：config.adoc→configurationProperties、
   whatsNew→configurationProperties、introspectedAccessorsStyle→configurationPropertiesAccessorsStyle、
   beanMappers→evaluatedExpressions ×2 因本批落盘消解 −5）；
7. `--mark-current` 4/4 核销（hash+commit 双字段对账通过）；pytest 95 绿。

## 锚点注入（PLAN §5.6，B02 精化规则）

- `guide/config/evaluatedExpressions.adoc` → `[[evaluatedExpressions]]`（被 beanMappers.adoc 引用 ×2，
  已译——本批落盘后 2 条 ⑤ 豁免消解，批间引用闭环）
- `guide/config/configurationProperties.adoc` → `[[configurationProperties]]`（被 containerArch.adoc、
  config.adoc、clientConfiguration.adoc、whatsNew.adoc 引用；config.adoc/whatsNew 已译——
  本批落盘后 2 条豁免消解，其余未译豁免承接）
- 源内已有显式锚点 `[[configurationPropertiesAccessorsStyle]]` 经 ANCLINE 占位符保护逐字节保留
  （introspectedAccessorsStyle.adoc 引用随之消解）；
- customTypeConverter.adoc、eachProperty.adoc 未被登记引用，无注入。

## 术语滚动

- 本批无新增 glossary 条目；B07 括注「kebab case」在 eachProperty.adoc 复现命中（上游原文 kebap case
  按 glossary 统一译法处理）；
- 新首现括注（按首现处理，频次待后续复核）：求值表达式（evaluated expressions）、
  小驼峰式（lower camel case）、类型使用（type use，承 B06 类型使用注解）；
- 既有术语 bean（小写保留）、配置属性、依赖注入（仅指令行 title 参数，逐字节保留）、
  内省/限定符/工厂（未出现）一致命中；
- banned 黑名单 0 命中（validate ③ 全量扫描）。

## 里程碑

config 章（guide/config，15 文件）current 11/15（73%）：余 bootstrap、eachBean、
immutableConfig、jmx 4 文件未译。整库进度 81/388（20.9%）。IoC 章 55/55 保持全 current。

## 遗留与后续

- 27 条 ⑤ 豁免警告登记于 validate 输出，M3 全量断链清零时一并处理；
- 本批次未触发 sync --apply（冻结窗口遵守）；`source/` 无写入；
- evaluatedExpressions.adoc（141 段、89 占位符、2 级/3 级/4 级标题混合）为本批最长文件，
  对译检查通过后确认无返工。
