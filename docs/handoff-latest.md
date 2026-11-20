# 交接文档（handoff-latest）

> 更新：2026-11-21 ｜ 会话：M2 分批翻译（B07–B14 完成，进度破 40%）｜ 下一会话任务：M2 继续分批翻译（B15 起）

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
| **B09 翻译批次** | `a18c135` | 8 文件（config 收尾 4：jmx/eachBean/bootstrap/immutableConfig + AOP 开头 4：aop/aroundAdvice/introductionAdvice/adapterAdvice）全绿核销；词数 2852（实测）/段落 125；报告见 `reports/batch-B09.md`；锚点注入 5 处（aop/aroundAdvice/introductionAdvice/bootstrap/jmx），aop ×3 豁免消解；reviewer 术语检查改为复用 validate ③ check_terms；**config 章 15/15 全章译出**；AOP 章 3/10 起步 |
| **B10 翻译批次** | `cb89326` | 5 文件（AOP：lifecycleAdvice + interceptorLifecycle + validation + caching + retry）全绿核销；词数 3022（实测）/段落 140；报告见 `reports/batch-B10.md`；锚点注入 4 处（lifecycleAdvice↔interceptorLifecycle 批内互引 + retry/validation）；**retry 首轮漏锚点被 reviewer 抓出补齐**；豁免 25→23；AOP 章 8/10（80%） |
| **B11 翻译批次** | `ca907e4` | 7 文件（AOP 收尾 2：scheduling/springAop + httpServer 章页与前 4 节）全绿核销；词数 3270（实测）/段落 206；报告见 `reports/batch-B11.md`；锚点注入 4 处 + **页内标题锚 [[_uri_path_variables]] 原位注入首实践**；httpServer ③ netty→Netty 修正；**AOP 章 10/10 全章译出** |
| **B12 翻译批次** | `d1dbc49` | 25 文件（httpServer：customArgumentBinding…reactiveServer 组 11 + jsonBinding 组 14，本工程最大批次）全绿核销；词数 3363（实测）/段落 168；报告见 `reports/batch-B12.md`；锚点注入 4 处（jsonBinding 批内 5 文件闭环 + 3 个豁免承接）；jsonBinding 漏锚点被 validate ⑤ 门禁抓出补齐；大批次工作法验证（先全量 protect 207 占位符再分文件翻译） |
| **B13 翻译批次** | `83a4fa0` | 17 文件（httpServer：plainTextResponses/datavalidation 组 2/staticResources/errorHandling 组 8/apiVersioning/formData/form 组 3）全绿核销；词数 3122（实测）/段落 179；报告见 `reports/batch-B13.md`；锚点注入 3 处（exceptionHandler 批内 errorFormatting 闭环 + form/formCapable 消解 whatsNew ×2）；validate 首轮 ⑦×1 与 ③×1 修正；errorHandling 组与 form 组全组 current |
| **B14 翻译批次** | 本次提交 | 13 文件（httpServer：serverIO/uploads/transfers/filters 组 10）全绿核销；词数 3410（实测）/段落 160；报告见 `reports/batch-B14.md`；锚点注入 5 处（filtermethods/httpServerFilter 批内闭环 + uploads/order 消解 whatsNew ×2 + filters）；transfers ⑦ 邻接 ×2（含加粗标记）修正；httpServer 组 59/101（58%） |

## 状态快照（2026-11-21，B14 收尾）

- 分支 main；基线 v5.2.25（`0b46d27afdfa`，快照日期 2026-11-20）；批次期间冻结窗口遵守（未跑 --apply）
- manifest：388 条目 = 230 missing + 2 skipped + **156 current**（进度 40.2%）
- 看板：B01–B14 = current，其余 18 批 pending
- anchor-registry：121 条（不变）；validate 全量跑：PASSED（156 文件，⑤ 豁免警告 26 条，M3 清零）
- 页头溯源投影：页名=toc 英文原题、URL=`https://docs.micronaut.io/5.2.x/core/#core-<basename>`（复用 B01 实测格式）、基线锁定日期 2026-11-19、translated_at=2026-11-21
- reports/progress.md 已重新生成（IoC 55/55、introduction 2/2、quickStart 9/9、config 15/15、aop 10/10、**httpServer 59/101**）
- 里程碑：已全章译出 introduction、quickStart、IoC、config、AOP 五个章；httpServer 组 59/101（58%），下批 B15 继续（serverConfiguration 组）

## 实测结论（本会话新增/沿用）

1. **锚点注入位置规则（B02 精化，B07–B14 复用验证）**：basename 约定锚点 = 官方站 `core-<basename>` = 片段首内容之前的块锚——对正文先行的文件注入于第一段之前。B07–B14 共 29 处注入；页内标题锚（如 routing 的 `<<_uri_path_variables,…>>`）按 PLAN §5.6 原位注入于标题行之前（B11 首实践）。
2. **词数口径差异**：M1 inventory 报告值生成于 B01 snippet:: 保护修复之前；后续批次词数以批次执行时实测为准（B02 3055/2991、B03 3417/3377、B04 2588/2545、B05 2074/2076、B06 3482/3445、B07 2540/2484、B08 3400/3336、B09 2852/2835、B10 3022/3002、B11 3270/3240、B12 3363/3336、B13 3122/3076、B14 3410/3402），M1 报告值仅作切分参考。
3. **批间前向引用消解模式**：先行文件对未译目标的 xref 记为 ⑤ 豁免；后续批次落盘目标文件后豁免自动消解。B07 −5、B08 −5、B09 净 −2、B10 −2、B11 净 −1、B12 净 +2、B13 净 +1、B14 净 −1（order/uploads 消解 −2；serverIO→threadPools 新增 +1）；批次报告须核对豁免增减明细。
4. **reviewer 术语检查自 B09 起与 validate ③ 同源**：直接 `import validate_translation as vt` 复用 `vt.check_terms`（含 banned）；/tmp/b14_reviewer.py 为当前模板（临时不入库，逐批复制改 FILES/NEED_ANCHOR；**写临时脚本一律用 Write 工具并先 py_compile 再运行**——B14 实测 Bash 内联生成被 hook 拒绝且分段拼写易出错）。
5. **锚点漏注入的两道防线（B10/B12 双验证）**：批内互引目标漏注入时，validate ⑤ 会以「锚点在已译目标的译文中不存在」**直接报错拦截**；跨页前向引用仍靠 reviewer 清单自查。补救链路（补注入 → restore → assemble → validate/mark-current 重跑）顺畅；mark-current 对已核销文件可幂等重跑。
6. **③ 必译术语的三类误触与修法**：(a) 宏路径命中（B10：`…/interceptor/CacheInterceptor` → 补首现括注「缓存拦截器」；B13：`api:http.client.interceptor.configuration.…` → 补「（客户端拦截器配置）」括注）；(b) 指令行未被 strip 命中小写 API 名而 zh 侧链接 label 被 RE_URL 连带剥除（B11：`dependency:…-netty[]` → 正文普通词物化）——均以正确译法过门禁，不绕过机检。
7. **advice 译法自 B09 统一为「通知（advice）」**（承 B06 reflection 先例）；eagerly initialize/eager initialization 命中 approved 术语「饿汉式初始化」。
8. **源内已有显式锚点（ANCLINE 占位符）与 shorthand xref（`<<target,label>>`，未被 protect 捕获）均按纪律手保**：锚点行逐字节保留；xref target 逐字节保留、label 译出（产品名/规范链接 label 保留）。**复合 xref（label 内嵌行内码占位符）与未保护 `snippet::` 指令行（title 含泛型）同样逐字节保留**。
9. **validate ⑦ 邻接规则（B08/B10/B12/B13/B14 五次踩坑）**：占位符/行内码/加粗标记后紧跟全角开括号必拒（B14 transfers `` `304`（ `` 与 `` *响应式流*（ `` 双违规）；宏 `[]` 后接全角开括号不在机检范围。占位符与 `*…*` 之后接 `（` 一律预留空格必须作为翻译期硬习惯。
10. **大批次工作法（B12/B13/B14 验证）**：先全量 protect（核对占位符总数）→ 逐文件写译文 → 批量 restore → 批量 assemble → 逐文件 validate。protect 输出目录含子目录，restore 时显式列全路径。
11. `[NOTE] ====` 嵌套块、`[.lang-…]`+`--` 开放块、`{blank}` 列表项（ATTRREF 占位符）、块标题、原生表格（`\|=======` 与 `\|===`）结构保持、标题文本译出；裸代码行与 `dependency:…`/`dependency::…` 宏逐字节保留；validate ④ 仅拦「≥2 英文词且未翻译」的标题。
12. **progress 行列位读法**：progress.md 行格式为 `\| 章节 \| 文件数 \| missing \| stale \| partial \| current \| skipped \| 进度 \|`——B13 曾将 missing 列误读为 current（55/101），B14 以完整行核对发现并勘误（B13 实为 46/101，B14 后 59/101）。读表必须核对列位。
13. restore 后必须核对 restored 文件数与输入数一致（B04 教训沿用）；B07–B14 占位符笔误 0。

## 待办（下一会话）

1. **M2 继续**：B15 起（13 文件：httpServerFilterErrorStates/responseHeaderPopulator/byteBody 组 4/sessions/sse/websocket 组 3/http2Server/http3Server，双指标达标），看板改 in-progress 后按 §5.1 SOP + 固化校验链执行；启动提示词已更新至 B15 起（`docs/新会话启动提示词.md`）。注意：whatsNew→http3Server 豁免将由 http3Server.adoc 落盘消解。
2. 术语滚动：B05–B14 括注待复核（构造型 stereotype、可保留 retainable、别名 alias、属性源 property source、mixin、规范构造器 canonical constructor、类型使用注解 type-use annotation、可空性注解、banner、kebab case、驼峰式 camel-case、提供者 provider、默认环境 default environment、求值表达式 evaluated expressions、小驼峰式 lower camel case、通知 advice、切面 aspect、环绕通知/引入通知、存根值 stubbed value、校验通知 validation advice、缓存拦截器 CacheInterceptor、weigher 权重计算器、断路器 Circuit Breaker、规约 specification、展开操作符 exploded operator、编解码器 codec、事件循环 Event Loop、数据类 Data Classes、校验组 validation groups、局部/全局错误处理器、异常处理器 exception handler、背压 backpressure、流式上传/完成上传、部件 part、管道断裂 broken pipe）；context propagation（B01 括注）继续待复核
3. M3+：断链豁免清零（当前 26 条）、抽检、sync drill、tag v1.0

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
