# 批次报告 B06

> 完成日期：2026-11-21 ｜ 执行：M2 第六批次（串行 1，单会话编排方亲跑）

## 范围与规模

| 指标 | 值 |
|---|---|
| 文件数 | 11（IoC 余 7 + config 章开头 4） |
| 总词数（当前 protect 后口径，实测） | 3482（M1 inventory 报告值 3489，口径见 reports/batch-B02.md） |
| 非代码词（当前口径，实测） | 3445（M1 inventory 报告值 3454） |
| 段落数 | 163（manifest paragraphs 合计） |
| 上游基线 | v5.2.25（tag，2026-11-17 发布；快照 `0b46d27afdfa`） |
| 最终状态 | 11 文件全部 current（manifest 388 条目中 73/388，进度 18.8%） |

双指标达标：非代码词 3445 ≤ 3500 且总词 3482 ≤ 5500。

## 流程执行（PLAN §5.1 SOP + 固化校验链）

1. protect：11 文件（占位符合计 173）；
2. 翻译：占位符逐个从 `-protected.txt`/映射表复制；`dependency::` 宏逐字节保留；
   `snippet::` 指令行（environments/disablingEnvironmentDetection 共 2 处）经占位符保护逐字节保留；
3. restore：11/11 哈希完整性全过（0 残留，restored 数与输入数核对一致）；
4. 溯源投影：`assemble_zh.py` 注入（translated_at=2026-11-21）；
5. reviewer 五项：段落对译 11/11 PASS（zh 侧剔除页头溯源段与纯锚点段；
   停用词漏译检测仅查 paragraph/admonition/heading/table 四类段）；
   xref/link 目标逐字节一致；锚点注入到位；
6. validate：首轮全量 73 文件 PASSED（11 新文件 `--file` 全绿含于全量）；
   ⑤ 豁免警告 36 条（35 → 36：config.adoc→configurationProperties、
   config.adoc→propertySource、environments.adoc→cloudConfiguration 新增 +3；
   whatsNew→nullabilityAnnotations、whatsNew→jspecify 因本批落盘消解 −2）；
7. `--mark-current` 11/11 核销（hash+commit 双字段对账通过）；pytest 95 绿。

## 锚点注入（PLAN §5.6，B02 精化规则）

- `guide/ioc/reflection.adoc` → `[[reflection]]`（被 languageSupport/python/generatedClasses.adoc 引用，未译，⑤ 豁免承接）
- `guide/ioc/classImport.adoc` → `[[classImport]]`（被本批 mixin.adoc `<<classImport,…>>` 引用——**批内引用闭环**）
- `guide/ioc/nullabilityAnnotations.adoc` → `[[nullabilityAnnotations]]`（被 whatsNew.adoc 引用，B01 已译——本批落盘后该 ⑤ 豁免消解，批间引用闭环）
- `guide/ioc/nullabilityAnnotations/jspecify.adoc` → `[[jspecify]]`（被 whatsNew.adoc 与本批 nullabilityAnnotations.adoc 引用——批间+批内双闭环）
- `guide/config/environments.adoc` → `[[environments]]`（被 iocArch.adoc、cloudConfiguration.adoc 引用，均未译，⑤ 豁免承接）
- mixin/springBeans/android/config/environmentPriority/disablingEnvironmentDetection 未被登记引用，无注入。

## 术语滚动

- 本批无新增 glossary 条目；新括注（按首现处理，频次待后续复核）：
  「构造型（stereotype）」（reflection，承 B05）、「属性源（property source）」
  （environmentPriority）、「mixin（混入）」、「规范构造器（canonical constructor）」、
  「类型使用注解（type-use annotation）」、「可空性注解（Nullability Annotations）」；
- 既有术语 introspection→内省（「Bean 内省」）、qualifier→限定符、factory→工厂、
  interceptor→拦截器（未出现）、eager initialization（未出现）一致命中；
- banned 黑名单 0 命中（validate ③ 全量扫描）。

## 里程碑

**IoC 章（guide/ioc，55 文件）全部 current**：B01–B06 六批完成 IoC 全章译出。
下批 B07 起 config 章持续推进（config 章 15 文件已 current 3）。

## 遗留与后续

- 36 条 ⑤ 豁免警告登记于 validate 输出，M3 全量断链清零时一并处理；
- 本批次未触发 sync --apply（冻结窗口遵守）；`source/` 无写入；
- reflection.adoc 为 IoC 章最长散文（占位符 66、段落 50），对译检查通过后确认
  无返工；该文件含大量 `api:` 宏与行内码占位符，后续修订时仍须以映射表为准。
