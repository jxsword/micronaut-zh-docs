# 交接文档（handoff-latest）

> 更新：2026-11-21 ｜ 会话：M2 分批翻译（B02/B03/B04 完成）｜ 下一会话任务：M2 继续分批翻译（B05 起）

## 已完成清单（全部已提交，main 分支）

| 工作单元 | 提交 | 说明 |
|---|---|---|
| M0 余项 | `67fd538` | README / LICENSE / LICENSE_TRANSLATION.md |
| M1 基建（六脚本+tests+config+CI+快照+切分） | `2fb7425`…`e72d9ef` | 见 M1 收尾报告；pytest 86 绿 |
| **B01 翻译批次** | `b03bf56` | 19 文件（Introduction 3 + Quick Start 10 + IoC 前 6 节）全绿核销；词数 3355/段落 190；报告见 `reports/batch-B01.md`；M1 缺陷×4 + assemble_zh.py；pytest 94 绿 |
| **B02 翻译批次** | `1a2b496` | 12 文件（Injection 子节 4 + Types/Qualifiers/Typed 3 + Scopes 5）全绿核销；词数 3055（实测）/段落 207；报告见 `reports/batch-B02.md`；validate ③ 指令行误报修复，pytest 95 绿；术语转正 qualifier/eager initialization/meta annotation |
| **B03 翻译批次** | `4bdd58f` | 10 文件（Factories…Introspection 前 2 节）全绿核销；词数 3417（实测）/段落 192；报告见 `reports/batch-B03.md`；术语转正 factory/introspection/graceful shutdown |
| **B04 翻译批次** | 本次提交 | 19 文件（Introspection 全章 15 + BeanMappers 3 + BeanValidation）全绿核销；词数 2588（实测）/段落 151；报告见 `reports/batch-B04.md`；批内锚点闭环 ×2；restore 门禁拦截占位符笔误 1 处 |

## 状态快照（2026-11-21，B04 收尾）

- 分支 main；基线 v5.2.25（`0b46d27afdfa`，快照日期 2026-11-20）；批次期间冻结窗口遵守（未跑 --apply）
- manifest：388 条目 = 326 missing + 2 skipped + **60 current**（进度 15.5%）
- 看板：B01–B04 = current，其余 28 批 pending
- anchor-registry：121 条（不变）；validate 全量跑：PASSED（60 文件，⑤ 豁免警告 34 条，M3 清零）
- 页头溯源投影：页名=toc 英文原题、URL=`https://docs.micronaut.io/5.2.x/core/#core-<basename>`（复用 B01 实测格式）、基线锁定日期 2026-11-19、translated_at=2026-11-21
- reports/progress.md 已重新生成；mimosa 深度安全扫描 ×2 均 0 findings（最新封印 `sha256:151d7d2a…`，2026-11-21）

## 实测结论（本会话新增）

1. **锚点注入位置规则精化**：B01 的「无标题片段文件首 / 有标题片段标题上方」两分法在 upgrading.adoc（首行即标题）上无法区分。B02 确认统一规则：**basename 约定锚点 = 官方站 `core-<basename>` = 片段首内容之前的块锚**——对首行即标题的文件等同于标题上方，对正文先行的文件（B02 四例、B03 五例、B04 四例）注入于第一段之前，使锚点覆盖整个片段。
2. **词数口径差异**：M1 inventory 报告值生成于 B01 snippet:: 保护修复之前；**后续批次词数以批次执行时实测为准**（inventory.py word_counts 现行实现：B02 3055/2991、B03 3417/3377、B04 2588/2545），M1 报告值仅作切分参考。
3. **validate ③ strip_code 缺陷已修**：`snippet::` 宏参数含 `qualifier` 子串，术语转正后触发「必译术语缺失」误报 → strip_code 剔除指令行（复用 segment_adoc.RE_DIRECTIVE），回归测试 +1，pytest 95 绿。
4. **scope→作用域、event listener→事件监听器 评估后不入 glossary 机检**：前者 substring 会命中 whatsNew 的 "scoped values"（JDK ScopedValue API）；后者为低风险组合词。「作用域/监听器」作为工作约定使用。
5. reviewer 段落对照的 zh 侧剔除口径：页头溯源段 + `[[…]]` 纯锚点注入段（方法记录于批次报告，临时脚本不入库）。
6. **术语转正前必须做已译文件全量安全性预检**（近似散文域检索 en 词 vs zh 词），防追溯性误伤；B02/B03 各转正 3 条均经此流程；B04 验证 introspection 提前转正价值（全章 15 文件一致命中）。
7. `dependency::` 依赖坐标宏不在 RE_DIRECTIVE 保护清单内，按「指令行不译」纪律逐字节保留（validate ② 逐字节门禁实际覆盖）。
8. 上游作者 `// TODO` 注释行（conditionalBeans/contextEvents/metaScopes 共 3 处）按散文语义翻译。
9. **restore 哈希门禁实战拦截占位符笔误**（B04：译文误写 6232a110，源文为 fbd67c3f）——占位符必须逐个从 `-protected.txt` 复制；另外组合命令中 restore 失败会静默中断后续（错误信息只出现一次），**restore 后必须核对 restored 文件数与输入文件数一致**再 assemble。

## 待办（下一会话）

1. **M2 继续**：B05 起（2 文件：annotationMetadata 2138 词 + beanImport，双指标达标），看板改 in-progress 后按 §5.1 SOP + 固化校验链执行；启动提示词见 `docs/新会话启动提示词.md`（已更新至 B05）；annotationMetadata 被 ioc.adoc（B01 已译）引用（当前为 ⑤ 豁免警告），落盘后警告消解
2. 术语滚动：context propagation（B01 括注）继续待复核；B05 annotationMetadata 涉及 AnnotationMapper/Stereon 等术语注意首现括注
3. M3+：断链豁免清零（当前 34 条）、抽检、sync drill、tag v1.0

## 调试经验与坑位（累计）

1. 长输出损坏处置：立即读回文件 → 修损坏行 → pytest 全绿 → 再提交（M1 经验）
2. gh api commits?path= 须用全仓路径 `src/main/docs/<rel>`
3. 网络直连 github.com 失败 → git/curl 走 `http://192.168.33.1:10808`；gh api 直连可用；**11MB 级大页 curl 直连会超时截断，必须代理 + 后台跑**
4. validate ⑤ 段落对照机检：zh 侧剔除页头溯源段（引用行+注释行合并为一段，恒 +1 偏差）
5. PreToolUse hook 拒绝 Bash 直写源码/测试文件（heredoc/append/sed -i）→ 一律 Write/Edit 提交
6. zh 译文页头 `> ` 引用行与 `<!-- -->` 注释行不参与 ⑦/③ 校验，溯源字段以 ⑥/manifest 对账为准
7. **translator 必须使用受保护文本中的真实占位符哈希**：B02 实测一次臆造占位符（refreshable）被 restore 哈希完整性拦下，重写后通过——切勿照源文裸写、占位符以 `-protected.txt` 为准逐个复制
8. restore 输出 JSON 无 ok 字段（成功时含 `restored` 键）；解析时勿以 `ok` 判成败

## 硬性纪律清单（继承）

1. `docs/翻译计划.md` 为唯一权威规范；改架构走 decision_log（DR-004 起递增）
2. 所有脚本 memgate 包裹；`source/` 只读；`manifest.yml` 禁人工直改（--mark-current 除外）
3. 门禁硬性化，禁止 `|| true`
4. 每批次 squash commit + 批次报告；决策类提交末行 `Decision: DR-编号`
5. agent 并发上限 = 串行 1；上下文过半立即交接
