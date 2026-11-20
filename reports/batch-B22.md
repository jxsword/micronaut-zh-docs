# 批次报告 B22

> 完成日期：2026-11-21 ｜ 执行：M2 第二十二批次（串行 1，单会话编排方亲跑；与 B21 同会话接续）

## 范围与规模

| 指标 | 值 |
|---|---|
| 文件数 | 5（languageSupport/python 子组：pythonRuntime/pythonThreading/decorators/sourceRoots/typeOrdering） |
| 总词数（protect 后口径，实测） | 3045（M1 inventory 报告值 3057，差异为口径统计基数所致，以实测为准） |
| 非代码词（当前口径，实测） | 3048（M1 报告值 3062） |
| 段落数 | 104（inventory segments 口径，与既往批次 commit 口径一致） |
| 上游基线 | v5.2.25（tag，2026-11-17 发布；快照 `0b46d27afdfa`） |
| 最终状态 | 5 文件全部 current（manifest 388 条目中 291/388，进度 75.4%，剔 skipped 口径） |

双指标达标：非代码词 3048 ≤ 3500 且总词 3045 ≤ 5500。占位符合计 127
（最多 pythonThreading 55，单文件词数 pythonThreading 1565 为 python 章最重）；
源文件无显式锚（ANCLINE 0 处）；**锚点注入 0 处**（registry 实测：该 5 文件既未被登记引用、
自身也不含被引锚点）。

## 流程执行（PLAN §5.1 SOP + 固化校验链）

1. protect：5 文件（127 占位符；DIRECTIVE 2 处为 snippet::/include:: 指令行逐字节保留）；
2. 翻译：pythonRuntime（GraalPy 运行时/宿主类查找条目匹配规则 4 条 bullet）、
   pythonThreading（GIL/上下文池/prestart/asyncio 桥/池统计，40 段为组长）、
   decorators（装饰器=注解载体/自定义注解/占位主体）、sourceRoots（跨源码组导入与
   包初始化器机制）、typeOrdering（前向引用加引号）；长英文日志文案占位符
   （polyglot fallback 警告全文）按行内码保留不译；
3. restore：5/5 首轮全过；assemble 落 zh/ 5 文件（translated_at=2026-11-21）；
4. validate：逐个 `--file` 3/5 首轮全绿，pythonRuntime ⑦ ×2 与 pythonThreading ⑦ ×1
   （行内码/占位符后紧跟全角开括号，累计踩坑 11 次）修复后 5/5 全绿；
5. **glossary 滚动回流（新错误模式）**：新术语收录后全量 validate 立即触发既有文件
   ③ 回流 3 处——visitor→访问者 触发 evaluatedExpressions/annotationMetadata（宏路径
   TypeElementVisitor 误触，按 B13 先例补「（类型元素访问者）」括注）与 classImport
   （B06 真实命中，曾译「类型访问器」，统一为「访问者」）；修复后全量 291 文件 PASSED；
6. reviewer 五项：/tmp/b22_reviewer.py **5/5 PASS 首轮零缺陷**；
7. `--mark-current` 5/5 核销；pytest 95 绿。

## 术语滚动（本批重点）

- 新增 glossary 6 条（approved，均 Python 章复现项）：访问者（visitor）、装饰器（decorator）、
  全局解释器锁（Global Interpreter Lock/GIL）、上下文池（context pool）、虚拟线程（virtual thread）、
  仪表（gauge，Micrometer 语境 B27–B28 复现）；glossary 现 31 术语 / 6 禁用；
- 首现括注：存根（stub）、回退运行时（fallback runtime）、宿主类查找（Host class lookup）、
  可选加入（opt-in）、前向引用（forward reference）、构造型（stereotype）复现、
  文档字符串（docstring）、引入通知（introduction advice）复现、按键读取（keyed read）、
  借用（borrow）、敏感（sensitive，端点语境）；
- banned 黑名单 0 命中；编译期/类路径/响应式/事件循环/优雅关闭等既有术语全章一致命中。

## 里程碑与进度

- 整库进度 291/388（75.4%，剔 2 skipped）；languageSupport 章 13/50（26%）；
- python 子章 6/24（python.adoc 章页 + 本批 5 文件；B23–B25 继续 18 文件）；
- ⑤ 豁免警告维持 10 条（本批 0 消解 0 新增——5 文件无登记 xref 目标）。

## 遗留与后续

- **新会话教训（handoff 已记）**：新术语写回 glossary 后必须立即跑全量 validate——
  术语收录会使 ③ 必译检查扩及全部已译文件，回流命中的既有文件按「物化/括注」修
  （B22 实证 3 处，其中 classImport 属术语译名统一修正）；
- B23（6 文件：interfaces/standardTypes/javaCollections/runtimeTypes/javaImports/keywords）
  **需注入锚点 2 处**：`[[standardTypes]]`（被 runtimeTypes 引用——批内闭环）、
  `[[runtimeTypes]]`（被 javaCollections 引用——批内闭环）；另 interfaces→generatedClasses
  为未译目标，记 1 条新豁免（B24 落盘 generatedClasses 时消解）；
- 本批次未触发 sync --apply（冻结窗口遵守）；`source/` 无写入。
