# 批次报告 B03

> 完成日期：2026-11-21 ｜ 执行：M2 第三批次（串行 1，单会话编排方亲跑，与 B02 同会话）

## 范围与规模

| 指标 | 值 |
|---|---|
| 文件数 | 10（Factories/Conditional/Replaces/BeanConfigurations/Lifecycle/Shutdown/Events/Introspection 前 2 节） |
| 总词数（当前 protect 后口径，实测） | 3417（M1 inventory 报告值 3454，差异口径见 reports/batch-B02.md） |
| 非代码词（当前口径，实测） | 3377（M1 inventory 报告值 3443） |
| 段落数 | 192（manifest paragraphs 合计） |
| 上游基线 | v5.2.25（tag，2026-11-17 发布；快照 `0b46d27afdfa`） |
| 最终状态 | 10 文件全部 current（manifest 388 条目中 41/388，进度 10.6%） |

双指标达标：非代码词 3377 ≤ 3500 且总词 3417 ≤ 5500。

## 流程执行（PLAN §5.1 SOP + 固化校验链）

1. protect：10 文件（占位符合计 164）；
2. 翻译：占位符逐字节保留；`dependency::` 宏（RE_DIRECTIVE 未收录）按不译纪律逐字节保留；
   上游作者 `// TODO` 注释行按散文语义翻译（2 处：conditionalBeans、contextEvents）；
3. restore：10 文件哈希完整性校验全过（0 残留）；
4. 溯源投影：`assemble_zh.py` 注入（translated_at=2026-11-21）；
5. reviewer 五项：段落对照 10/10 一致且 0 漏译（剔除页头段与 `[[…]]` 锚点段）；
6. validate：10 文件 `--file` 全绿 + 全量 41 文件 PASSED；⑤ 豁免警告 31 条
   （29 → 31：conditionalBeans→logging、factories→aop 新增 +2）；
7. `--mark-current` 10/10 核销（hash+commit 双字段对账通过）。

## 锚点注入（PLAN §5.6，B02 精化规则）

登记表以 B03 文件为目标的锚点 5 条，全部按块锚注入文件首（第一内容之前）：

- `guide/ioc/factories.adoc` → `[[factories]]`（被 aop/aroundAdvice、httpServer/secondaryServers 引用）
- `guide/ioc/conditionalBeans.adoc` → `[[conditionalBeans]]`（被 containerArch、cloudConfiguration、annotationMetadata、**replaces（本批内）** 引用）
- `guide/ioc/replaces.adoc` → `[[replaces]]`（被 clientSideLoadBalancing、nettyHttpClient 引用）
- `guide/ioc/events.adoc` → `[[events]]`（被 httpServerArch、cloudConfiguration、netty 管道、serverEvents 引用）
- `guide/ioc/introspection.adoc` → `[[introspection]]`（被 introspectionArch、jsonBinding、beanMappers 引用）

批内引用闭环：replaces.adoc 的 `<<conditionalBeans, 条件 bean>>` 在本批内目标已译，
validate ⑤ 实机检通过（`[[conditionalBeans]]` 字面注入到位）。

## 术语滚动（先写回再继续）

**转正 glossary.yml（status: approved，3 条）**：

- `factory → 工厂`（aliases: factories；Factories 章全章 + Replaces/Lifecycle/Events 高频）
- `introspection → 内省`（B04 为 Introspection 全章 10 文件，提前锁定译名）
- `graceful shutdown → 优雅关闭`（唯一译法锁定，避免「平滑关闭/优雅停机」分歧）

**评估后不入表**：`event listener → 事件监听器`（组合词，风险低、机检价值低）。
41 文件全量安全性预检（近似散文域）通过后写回；写回后全量 validate 仍 PASSED。

## 轻量决策（不立 DR，记录于此）

- `dependency::[]` 依赖坐标宏按「指令行不译」纪律逐字节保留（RE_DIRECTIVE 未收录
  该宏，保护器未占位——validate ② 逐字节门禁实际覆盖，无需改动保护器）；
- 上游作者 `// TODO` 注释行按散文语义翻译（与 metaScopes 的 TODO 处理一致）。

## 遗留与后续

- 31 条 ⑤ 豁免警告登记于 validate 输出，M3 全量断链清零时一并处理；
- 本批次未触发 sync --apply（冻结窗口遵守）；`source/` 无写入；
- 临时脚本 `/tmp/review_b02.py`（复用，文件清单改为 B03）不入库。
