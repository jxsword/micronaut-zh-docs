# 批次报告 B04

> 完成日期：2026-11-21 ｜ 执行：M2 第四批次（串行 1，单会话编排方亲跑，与 B02/B03 同会话）

## 范围与规模

| 指标 | 值 |
|---|---|
| 文件数 | 19（Introspection 全章 15 + BeanMappers 3 + BeanValidation 1） |
| 总词数（当前 protect 后口径，实测） | 2588（M1 inventory 报告值 2604，口径见 reports/batch-B02.md） |
| 非代码词（当前口径，实测） | 2545（M1 inventory 报告值 2591） |
| 段落数 | 151（manifest paragraphs 合计） |
| 上游基线 | v5.2.25（tag，2026-11-17 发布；快照 `0b46d27afdfa`） |
| 最终状态 | 19 文件全部 current（manifest 388 条目中 60/388，进度 15.5%） |

双指标达标：非代码词 2545 ≤ 3500 且总词 2588 ≤ 5500。

## 流程执行（PLAN §5.1 SOP + 固化校验链）

1. protect：19 文件（占位符合计 158）；
2. 翻译：占位符逐字节保留；`<<introspection, Bean 内省>>` 批间引用目标（B03 已译且
   `[[introspection]]` 已注入）validate ⑤ 实机检通过；
3. restore：首轮 19 文件中 9 个因译文占位符笔误被哈希完整性拦截
   （introspectionTypeArguments 第 8 行误写 `PROTECTED_CODE_6232a110`，
   源文该处为 `PROTECTED_CODE_fbd67c3f`）——修正后 19/19 全过、0 残留；
   **佐证 handoff 坑位 7：占位符必须逐个从 -protected.txt 复制，臆造/误写必被拦截**；
4. 溯源投影：`assemble_zh.py` 注入（translated_at=2026-11-21）；
5. reviewer 五项：段落对照 19/19 一致且 0 漏译；
6. validate：19 文件 `--file` 全绿 + 全量 60 文件 PASSED；⑤ 豁免警告 34 条
   （31 → 34：introspectedAccessorsStyle→configurationPropertiesAccessorsStyle、
   beanMappers→evaluatedExpressions ×2 新增）；
7. `--mark-current` 19/19 核销（hash+commit 双字段对账通过）。

## 锚点注入（PLAN §5.6，B02 精化规则）

登记表以 B04 文件为目标的锚点 4 条，块锚注入文件首：

- `guide/ioc/introspection/staticAtCreator.adoc` → `[[staticAtCreator]]`（被本批 atCreator.adoc 引用，批内闭环）
- `guide/ioc/introspection/introspectedAnnotationOnAConfigurationClass.adoc` → `[[introspectedAnnotationOnAConfigurationClass]]`（被本批 atIntrospected.adoc 引用，批内闭环）
- `guide/ioc/introspection/propertyMembers.adoc` → `[[propertyMembers]]`（被 guide/ioc/reflection.adoc 引用）
- `guide/ioc/beanValidation.adoc` → `[[beanValidation]]`（被 guide/aop/validation.adoc 引用）

## 术语滚动

- `introspection → 内省`（B03 转正）在本批全章 15 文件一致命中，validate ③ 机检通过——
  提前转正的决策得到验证；
- 本批无新增术语申请；BeanWrapper/BeanProperty/BeanMapper 等 API 名不译；
  「构建器（builder）」「内省构建器」按首现括注处理。

## 遗留与后续

- 34 条 ⑤ 豁免警告登记于 validate 输出，M3 全量断链清零时一并处理；
- 本批次未触发 sync --apply（冻结窗口遵守）；`source/` 无写入；
- 临时脚本 `/tmp/review_b02.py` 复用（文件清单改为 B04），不入库。
