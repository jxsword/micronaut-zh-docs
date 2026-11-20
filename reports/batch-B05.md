# 批次报告 B05

> 完成日期：2026-11-21 ｜ 执行：M2 第五批次（串行 1，单会话编排方亲跑，与 B02–B04 同会话）

## 范围与规模

| 指标 | 值 |
|---|---|
| 文件数 | 2（annotationMetadata + beanImport） |
| 总词数（当前 protect 后口径，实测） | 2074（M1 inventory 报告值 2128，口径见 reports/batch-B02.md） |
| 非代码词（当前口径，实测） | 2076（M1 inventory 报告值 2138；本文件非代码词 > 总词系口径特性：CODEBLOCK 占位符在总词侧计 1 词） |
| 段落数 | 86（manifest paragraphs 合计） |
| 上游基线 | v5.2.25（tag，2026-11-17 发布；快照 `0b46d27afdfa`） |
| 最终状态 | 2 文件全部 current（manifest 388 条目中 62/388，进度 16.0%） |

双指标达标：非代码词 2076 ≤ 3500 且总词 2074 ≤ 5500。

## 流程执行（PLAN §5.1 SOP + 固化校验链）

1. protect：2 文件（占位符合计 89）；
2. 翻译：占位符逐字节保留；`dependency::` 宏逐字节保留；
3. restore：2/2 哈希完整性全过（0 残留，restored 数与输入数核对一致）；
4. 溯源投影：`assemble_zh.py` 注入（translated_at=2026-11-21）；
5. reviewer 五项：段落对照 2/2 一致且 0 漏译——首轮 annotationMetadata 段 7 误报
   为「疑似漏译」，实为代码块段（含英文注释，逐字节相同是 validate ② 的设计要求），
   reviewer 脚本已收紧为仅检查 paragraph/admonition/heading/table 四类段；
6. validate：首轮 3 处 ⑦ 邻接违规（行内码后紧跟全角开括号，L96/L170/L176），
   于译文工作文件修正（行内码与「（」之间加空格）→ restore → assemble 后
   2 文件 `--file` 全绿 + 全量 62 文件 PASSED；⑤ 豁免警告 35 条
   （34 → 35：ioc.adoc→annotationMetadata 因本批落盘消解 −1，
   annotationMetadata→aop、annotationMetadata→validation 新增 +2）；
7. `--mark-current` 2/2 核销（hash+commit 双字段对账通过）。

## 锚点注入（PLAN §5.6，B02 精化规则）

- `guide/ioc/annotationMetadata.adoc` → `[[annotationMetadata]]`（被 guide/ioc.adoc 引用，
  B01 已译——本批落盘后该 ⑤ 豁免警告消解，批间引用闭环）
- beanImport.adoc 未被登记引用，无注入。

## 术语滚动

- 本批无新增术语；「构造型（stereotype）」「可保留（retainable）」「别名（alias）」
  按首现括注处理，频次待后续批次复核是否转正；
- 既有术语 introspection→内省、factory→工厂、qualifier→限定符 均一致命中。

## 遗留与后续

- 35 条 ⑤ 豁免警告登记于 validate 输出，M3 全量断链清零时一并处理；
- 本批次未触发 sync --apply（冻结窗口遵守）；`source/` 无写入；
- reviewer 脚本误报收紧的方法（代码块/指令段不计入停用词漏译检测）随本报告记录。
