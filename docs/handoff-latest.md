# 交接文档（handoff-latest）

> 更新：2026-11-21 ｜ 会话：M2 分批翻译（B07–B09 完成，config 章全章译出）｜ 下一会话任务：M2 继续分批翻译（B10 起）

## 已完成清单（全部已提交，main 分支）

| 工作单元 | 提交 | 说明 |
|---|---|---|
| M0 余项 | `67fd538` | README / LICENSE / LICENSE_TRANSLATION.md |
| M1 基建（六脚本+tests+config+CI+快照+切分） | `2fb7425`…`e72d9ef` | 见 M1 收尾报告；pytest 86 绿 |
| **B01 翻译批次** | `b03bf56` | 19 文件（Introduction 3 + Quick Start 10 + IoC 前 6 节）全绿核销；词数 3355/段落 190；报告见 `reports/batch-B01.md`；M1 缺陷×4 + assemble_zh.py；pytest 94 绿 |
| **B02 翻译批次** | `1a2b496` | 12 文件（Injection 子节 4 + Types/Qualifiers/Typed 3 + Scopes 5）全绿核销；词数 3055（实测）/段落 207；报告见 `reports/batch-B02.md`；validate ③ 指令行误报修复，pytest 95 绿；术语转正 qualifier/eager initialization/meta annotation |
| **B03 翻译批次** | `4bdd58f` | 10 文件（Factories…Introspection 前 2 节）全绿核销；词数 3417（实测）/段落 192；报告见 `reports/batch-B03.md`；术语转正 factory/introspection/graceful shutdown |
| **B04 翻译批次** | `aef8bda` | 19 文件（Introspection 全章 15 + BeanMappers 3 + BeanValidation）全绿核销；词数 2588（实测）/段落 151；报告见 `reports/batch-B04.md`；批内锚点闭环 ×2；restore 门禁拦截占位符笔误 1 处 |
| **B05 翻译批次** | `49b7a9b` | 2 文件（annotationMetadata + beanImport）全绿核销；词数 2074（实测）/段落 86；报告见 `reports/batch-B05.md`；[[annotationMetadata]] 注入后 B01 ioc.adoc 引用闭环；reviewer 脚本收紧（代码块段不计停用词漏译）；validate ⑦ 邻接违规 3 处修正 |
| **B06 翻译批次** | `2e5a662` | 11 文件（IoC 余 7 + config 章开头 4）全绿核销；词数 3482（实测）/段落 163；报告见 `reports/batch-B06.md`；锚点注入 5 处（reflection/classImport/nullabilityAnnotations/jspecify/environments），批内 classImport↔mixin 闭环；**IoC 章 55 文件全部 current——IoC 全章译出** |
| **B07 翻译批次** | `abef899` | 4 文件（config：defaultEnvironment + banner + propertySource + valueAnnotation）全绿核销；词数 2540（实测）/段落 167；报告见 `reports/batch-B07.md`；锚点注入 2 处，5 条既有 ⑤ 豁免消解 + 批内 propertySource→valueAnnotation 闭环；config 章 7/15（47%） |
| **B08 翻译批次** | `f1fa4cf` | 4 文件（config：evaluatedExpressions + configurationProperties + customTypeConverter + eachProperty）全绿核销；词数 3400（实测）/段落 260；报告见 `reports/batch-B08.md`；锚点注入 2 处 + 显式锚点 configurationPropertiesAccessorsStyle 保留，5 条豁免消解；reviewer 脚本术语检查范围修正（仅查可译段）；config 章 11/15（73%） |
| **B09 翻译批次** | 本次提交 | 8 文件（config 收尾 4：jmx/eachBean/bootstrap/immutableConfig + AOP 开头 4：aop/aroundAdvice/introductionAdvice/adapterAdvice）全绿核销；词数 2852（实测）/段落 125；报告见 `reports/batch-B09.md`；锚点注入 5 处（aop/aroundAdvice/introductionAdvice/bootstrap/jmx），aop ×3 豁免消解；reviewer 术语检查改为复用 validate ③ check_terms；**config 章 15/15 全章译出**；AOP 章 3/10 起步 |

## 状态快照（2026-11-21，B09 收尾）

- 分支 main；基线 v5.2.25（`0b46d27afdfa`，快照日期 2026-11-20）；批次期间冻结窗口遵守（未跑 --apply）
- manifest：388 条目 = 297 missing + 2 skipped + **89 current**（进度 22.9%）
- 看板：B01–B09 = current，其余 23 批 pending
- anchor-registry：121 条（不变）；validate 全量跑：PASSED（89 文件，⑤ 豁免警告 25 条，M3 清零）
- 页头溯源投影：页名=toc 英文原题、URL=`https://docs.micronaut.io/5.2.x/core/#core-<basename>`（复用 B01 实测格式）、基线锁定日期 2026-11-19、translated_at=2026-11-21
- reports/progress.md 已重新生成（IoC 55/55、introduction 2/2、quickStart 9/9、**config 15/15**、aop 3/10）
- 里程碑：**config 章全章译出**（第四个全章：introduction、quickStart、IoC、config）；AOP 章 3/10 + 章页 aop.adoc 已入账，下批 B10 继续 AOP 章

## 实测结论（本会话新增/沿用）

1. **锚点注入位置规则（B02 精化，B07–B09 复用验证）**：basename 约定锚点 = 官方站 `core-<basename>` = 片段首内容之前的块锚——对正文先行的文件注入于第一段之前。B07–B09 共 9 处注入一次通过（B09 五处：aop/aroundAdvice/introductionAdvice/bootstrap/jmx）。
2. **词数口径差异**：M1 inventory 报告值生成于 B01 snippet:: 保护修复之前；后续批次词数以批次执行时实测为准（B02 3055/2991、B03 3417/3377、B04 2588/2545、B05 2074/2076、B06 3482/3445、B07 2540/2484、B08 3400/3336、B09 2852/2835），M1 报告值仅作切分参考。
3. **批间前向引用消解模式**：先行文件对未译目标的 xref 记为 ⑤ 豁免；后续批次落盘目标文件后豁免自动消解。B07 消解 5 条、B08 消解 5 条、B09 净消解 2 条（aop ×3 消解 − bootstrap→distributedConfiguration 新增 1）；批次报告须核对豁免增减明细。
4. **reviewer 术语检查自 B09 起与 validate ③ 同源**：直接 `import validate_translation as vt` 复用 `vt.check_terms`（含 banned），不重写裸正则——裸正则会误报别名子串（DI↔distributed）与宏路径（`api:aop.`↔AOP）；/tmp/b09_reviewer.py 为当前模板（临时不入库，逐批复制改 FILES/NEED_ANCHOR）。
5. **advice 译法自 B09 统一为「通知（advice）」**（承 B06 reflection 先例）；环绕通知（Around Advice）/引入通知（Introduction Advice）为章内首现括注；eagerly initialize 命中 approved 术语「饿汉式初始化」。
6. **源内已有显式锚点（ANCLINE 占位符）与 shorthand xref（`<<target,label>>`，未被 protect 捕获）均按纪律手保**：锚点行逐字节保留；xref target 逐字节保留、label 译出（产品名/规范链接 label 保留）。
7. **validate ⑦ 邻接规则（B08 踩坑、B09 全程预留空格零违规）**：占位符/行内码后紧跟全角开括号必拒；宏 `[]` 后接全角开括号不在机检范围（`[`*_~`]（` 正则），既有译文 `]（` 先例可行。占位符后接 `（` 一律预留空格应作为翻译期习惯。
8. `[NOTE] ====` 嵌套块与内嵌 `~~~` 小标题结构保持、标题文本译出；裸代码行（无围栏的 `List<Integer> integers;` 等）与 `dependency::` 宏逐字节保留。
9. restore 后必须核对 restored 文件数与输入文件数一致（B04 教训沿用）；B07–B09 restore 16/16 一次通过（占位符笔误 0）。
10. `dependency::`/`snippet::` 宏不在 protect 显式清单时也会被 RE_DIRECTIVE 捕获为占位符或按指令行纪律逐字节保留（validate ② 逐字节门禁覆盖）。

## 待办（下一会话）

1. **M2 继续**：B10 起（5 文件：aop/lifecycleAdvice + interceptorLifecycle + validation + caching + retry，双指标达标），看板改 in-progress 后按 §5.1 SOP + 固化校验链执行；启动提示词已更新至 B10 起（`docs/新会话启动提示词.md`）。注意：validation/retry 均在 registry 被 whatsNew 等引用——落盘后预计消解 ≥2 条豁免；lifecycleAdvice（title: Exceptions Thrown by Construct Advice）与 interceptorLifecycle（title: Interception Kinds）也在 registry。
2. 术语滚动：B05–B09 括注待复核（构造型 stereotype、可保留 retainable、别名 alias、属性源 property source、mixin、规范构造器 canonical constructor、类型使用注解 type-use annotation、可空性注解、banner、kebab case、驼峰式 camel-case、提供者 provider、默认环境 default environment、求值表达式 evaluated expressions、小驼峰式 lower camel case、通知 advice、切面 aspect、环绕通知/引入通知、存根值 stubbed value）；context propagation（B01 括注）继续待复核
3. M3+：断链豁免清零（当前 25 条）、抽检、sync drill、tag v1.0

## 调试经验与坑位（累计）

1. 长输出损坏处置：立即读回文件 → 修损坏行 → pytest 全绿 → 再提交（M1 经验）
2. gh api commits?path= 须用全仓路径 `src/main/docs/<rel>`
3. 网络直连 github.com 失败 → git/curl 走 `http://192.168.33.1:10808`；gh api 直连可用；**11MB 级大页 curl 直连会超时截断，必须代理 + 后台跑**
4. validate ⑤ 段落对照机检：zh 侧剔除页头溯源段（引用行+注释行合并为一段，恒 +1 偏差）
5. PreToolUse hook 拒绝 Bash 直写源码/测试文件（heredoc/append/sed -i）→ 一律 Write/Edit 提交；**临时 reviewer 脚本同样走 Write**（B08 实测 sed/heredoc 生成被拒）
6. zh 译文页头 `> ` 引用行与 `<!-- -->` 注释行不参与 ⑦/③ 校验，溯源字段以 ⑥/manifest 对账为准
7. **translator 必须使用受保护文本中的真实占位符哈希**（B02 臆造、B04 笔误均被门禁拦下）——占位符以 `-protected.txt` 为准逐个复制
8. restore 输出 JSON 无 ok 字段（成功时含 `restored` 键）；解析时勿以 `ok` 判成败
9. validate_translation.py `--file` 为单参数（B07 实测多文件报 unrecognized arguments），多文件逐个跑

## 硬性纪律清单（继承）

1. `docs/翻译计划.md` 为唯一权威规范；改架构走 decision_log（DR-004 起递增）
2. 所有脚本 memgate 包裹；`source/` 只读；`manifest.yml` 禁人工直改（--mark-current 除外）
3. 门禁硬性化，禁止 `|| true`
4. 每批次 squash commit + 批次报告；决策类提交末行 `Decision: DR-编号`
5. agent 并发上限 = 串行 1；上下文过半立即交接
