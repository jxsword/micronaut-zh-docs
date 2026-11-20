# 批次报告 B07

> 完成日期：2026-11-21 ｜ 执行：M2 第七批次（串行 1，单会话编排方亲跑）

## 范围与规模

| 指标 | 值 |
|---|---|
| 文件数 | 4（config 章：defaultEnvironment + banner + propertySource + valueAnnotation） |
| 总词数（当前 protect 后口径，实测） | 2540（M1 inventory 报告值 2554，口径见 reports/batch-B02.md） |
| 非代码词（当前口径，实测） | 2484（M1 inventory 报告值 2507） |
| 段落数 | 167（manifest paragraphs 合计：5+8+107+47） |
| 上游基线 | v5.2.25（tag，2026-11-17 发布；快照 `0b46d27afdfa`） |
| 最终状态 | 4 文件全部 current（manifest 388 条目中 77/388，进度 19.8%） |

双指标达标：非代码词 2484 ≤ 3500 且总词 2540 ≤ 5500。

## 流程执行（PLAN §5.1 SOP + 固化校验链）

1. protect：4 文件（占位符合计 169：7+6+123+33）；
2. 翻译：占位符逐个从 `-protected.txt`/映射表复制；`snippet::` 宏 6 处经占位符保护逐字节保留；
   `<<valueAnnotation,Configuration Injection>>` label 译出（配置注入，与 nullableInjection.adoc 用语一致）、目标逐字节保留；
   `<<distributedConfigurationVault, HashiCorp Vault>>` 产品名 label 保留；
   表格仅译单元格文本（`|===` 定界与 `\|` 分隔经占位符保护保留）；上游半角引号 `'micronaut.config.files'` 原样保留；
3. restore：4/4 哈希完整性全过（0 残留，restored 数与输入数核对一致）；
4. 溯源投影：`assemble_zh.py` 注入（translated_at=2026-11-21）；
5. reviewer 五项：段落对译 4/4 PASS（propertySource 75/75 段、valueAnnotation 29/29 段；
   zh 侧剔除页头溯源段与纯锚点段；停用词漏译检测仅查 paragraph/admonition/heading/table 四类段）；
   代码块逐字节 diff 一致；术语命中（glossary 全文件级）全过；xref/link 目标逐字节一致；
   溯源四字段与 manifest 对账通过；
6. validate：4 文件 `--file` 全绿；全量 77 文件 PASSED；
   ⑤ 豁免警告 32 条（36 → 32：config.adoc→propertySource、whatsNew→propertySource、
   whatsNew→configImport、whatsNew→customPropertySourceImporter、
   nullableInjection→valueAnnotation 因本批落盘消解 −5；
   propertySource→distributedConfigurationVault 新增 +1）；
7. `--mark-current` 4/4 核销（hash+commit 双字段对账通过）；pytest 95 绿。

## 锚点注入（PLAN §5.6，B02 精化规则）

- `guide/config/propertySource.adoc` → `[[propertySource]]`（被 config.adoc、bootstrap.adoc、whatsNew.adoc 引用；
  config.adoc/whatsNew 已译——本批落盘后 2 条 ⑤ 豁免消解，bootstrap.adoc 未译仍豁免承接）
- `guide/config/valueAnnotation.adoc` → `[[valueAnnotation]]`（被 containerArch.adoc、httpServerArch.adoc、
  propertySource.adoc、nullableInjection.adoc 引用；nullableInjection 已译——本批落盘后豁免消解并形成批内闭环
  propertySource→valueAnnotation；appendix 两文件未译仍豁免承接）
- defaultEnvironment.adoc、banner.adoc 未被登记引用，无注入。
- 源内已有显式锚点 `[[configImport]]`、`[[customPropertySourceImporter]]`、`[[duplicateConfigurationResources]]`
  经占位符保护逐字节保留（whatsNew 引用的前两者随之消解豁免）。

## 术语滚动

- 本批无新增 glossary 条目；B06 括注「属性源（property source）」在 propertySource.adoc 高频命中（语境一致）；
- 新首现括注（按首现处理，频次待后续复核）：banner（横幅）、kebab case（小写并以连字符分隔）、
  驼峰式（camel-case）、提供者（provider）、默认环境（default environment）；
- 既有术语 AOT（不译，Ahead-of-Time）、bean（小写保留）、配置属性/内省/限定符等未出现或一致命中；
- banned 黑名单 0 命中（validate ③ 全量扫描）。

## 里程碑

config 章（guide/config，15 文件）current 7/15（47%）：B06 起持续推进入度 3 → 7。
IoC 章 55/55 保持全 current；整库进度 77/388（19.8%）。

## 遗留与后续

- 32 条 ⑤ 豁免警告登记于 validate 输出，M3 全量断链清零时一并处理；
- 本批次未触发 sync --apply（冻结窗口遵守）；`source/` 无写入；
- propertySource.adoc 为 config 章最长文件（107 段、123 占位符，含 2 张表格与 11 个代码块占位符），
  对译检查通过后确认无返工；该文件含大量行内码占位符，后续修订时仍须以映射表为准。
