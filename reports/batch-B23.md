# 批次报告 B23

> 完成日期：2026-11-21 ｜ 执行：M2 第二十三批次（串行 1，单会话编排方亲跑；与 B21/B22 同会话接续）

## 范围与规模

| 指标 | 值 |
|---|---|
| 文件数 | 6（python 子组：interfaces/standardTypes/javaCollections/runtimeTypes/javaImports/keywords） |
| 总词数（protect 后口径，实测） | 3353（与 M1 inventory 报告值 3353 一致） |
| 非代码词（当前口径，实测） | 3378（与 M1 inventory 报告值 3378 一致） |
| 段落数 | 103（inventory segments 口径，与既往批次 commit 口径一致） |
| 上游基线 | v5.2.25（tag，2026-11-17 发布；快照 `0b46d27afdfa`） |
| 最终状态 | 6 文件全部 current（manifest 388 条目中 297/388，进度 77.1%，剔 skipped 口径） |

双指标达标：非代码词 3378 ≤ 3500 且总词 3353 ≤ 5500。占位符合计 236
（最多 standardTypes 58；occurrences 口径 keywords 59、standardTypes 107——复现占位符计入次数）；
源文件无显式锚（ANCLINE 0 处）。

## 流程执行（PLAN §5.1 SOP + 固化校验链）

1. protect：6 文件（236 占位符）；
2. 翻译：interfaces（接口两形态/运行时注解复制规则）、standardTypes（标准库类型映射双表）、
   javaCollections（外部 dict/实时视图/序列化五条限制/Java 持久化）、
   runtimeTypes（Class 实参/生成包装器/java.time 双路径/数值重载）、
   javaImports（星号导入/导入查找器）、keywords（尾部下划线约定/io 命名空间冲突）；
   `<<generatedClasses,生成的 Java 类>>` ×2、`<<runtimeTypes,运行时类型>>`、
   `<<standardTypes,标准类型转换>>` label 译出、目标逐字节保留；
3. restore：6/6 首轮全过；assemble 落 zh/ 6 文件（translated_at=2026-11-21）；
4. validate：逐个 `--file` 2/6 首轮全绿，standardTypes ⑦ ×2、runtimeTypes ⑦ ×1、
   keywords ⑦ ×1（行内码/占位符后紧跟全角开括号）修复后 6/6 全绿；
5. **锚点注入 2 处，均为页内标题锚**（registry 实测 title 非空，B11/B21 规则）：
   `[[standardTypes]]` 注入 `=== 带时区的日期时间（Aware datetimes）` 标题行之前
   （被 runtimeTypes 引用——**批内闭环**）；`[[runtimeTypes]]` 注入
   `=== 作为 Java Class 实参的 Python 类` 标题行之前（被 javaCollections 引用——**批内闭环**）。
   首轮曾把 [[runtimeTypes]] 误按 basename 锚置于文件首行，核对 registry title 字段后
   纠正为标题锚位置——**注入前必须核对条目 title 是否为空**；
   落盘后逐文件 grep 核对 2/2 在位且后随标题行；
6. reviewer 五项：/tmp/b23_reviewer.py **6/6 PASS 首轮零缺陷**（javaCollections 12 段，
   interfaces 含 generatedClasses 前向引用 ×2）；
7. `--mark-current` 6/6 核销；全量 297 文件 PASSED；pytest 95 绿。

## 术语滚动

- 本批无新增 glossary 条目（visitor/decorator/GIL/上下文池等 B22 已收录，全部命中复用）；
- 首现括注：星号导入（star import）、导入查找器（import finder）、外观（facade）、
  外部 dict（foreign dict）、实时视图（live view）、直写（write-through）、
  宿主互操作（host interop）、互操作视图、朴素（naive，datetime 语境）、
  带时区的（aware）、冻结 dataclass、规约（specification）复现；
- banned 黑名单 0 命中；响应式/内省/装饰器/访问者等既有术语全章一致。

## 里程碑与进度

- 整库进度 297/388（77.1%，剔 2 skipped）；languageSupport 章 19/50（38%）；
- python 子章 12/24（B22 5 + B23 6 + 章页 1；B24–B25 继续 12 文件）；
- ⑤ 豁免 10→11 条（**+1 新增**：interfaces→generatedClasses，generatedClasses 在 B24，
  落盘后消解；批内 2 闭环无新增豁免）。

## 遗留与后续

- **B24（5 文件：nestedTypes/pythonExceptions/functionalInterfaces/javaInterfaces/generatedClasses）
  需注入锚点 1 处**：`[[generatedClasses]]`（被 interfaces 引用，已译——落盘后消解上述 +1 豁免）；
  javaInterfaces→validation（B10 已注入）与 generatedClasses→reflection（B06 已注入）落盘即闭环；
- ⑦ 邻接累计踩坑增至 17 次（本批 +4）：行内码/占位符后接 `（` 加空格仍是硬习惯；
- 本批次未触发 sync --apply（冻结窗口遵守）；`source/` 无写入。
