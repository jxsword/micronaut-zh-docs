# 交接文档（handoff-latest）

> 更新：2026-11-23 ｜ 会话：M4.1 会话 4——**M4.1 P0 层收官（hibernate-validator + tracing + session 三模块全 100%，tag v1.1）**｜ 下一会话任务：**M4.2 P1 数据与消息**（启动提示词见 `docs/新会话启动提示词.md`）

## 已完成清单（M4.1 会话 4，全部随收尾提交入库）

| 工作单元 | 说明 |
|---|---|
| 周检 | check_all 全 0 变更（core cca2a1ce / security cc524538 / micrometer c4d064ee / validation 079f75dc），无需开 issue |
| 三模块前置（4f4642d） | gh api 实测补填 modules.json：hibernate-validator=micronaut-projects/micronaut-hibernate-validator @ 5.2.x（0ae7293d）、tracing=micronaut-projects/micronaut-tracing @ **8.4.x**（d38f08c0，无 5.2.x 分支按 SOP §4 用默认分支；**8.3.x/8.4.x docs blob 逐 sha 一致实测**，官方 /5.2.x/tracing/ 徽标 v8.3.0，ref 无漂移）、session=micronaut-projects/micronaut-session @ 5.2.x（14290594）；三快照均 0 壳 0 图；inventory 三单批（76/2878/689 非代码词，全 ≤3500 双指标） |
| HV-01（37e931b） | 4 文件+toc 七步全流程；validate 5 文件全绿零豁免；setup.adoc 全文件即 dependency: 指令行逐字节保留；URL+ATTRREF 复合占位符 SEC-04 同款处置；「Bean Validation」保留英文规范名（core 既译口径，不收录 glossary）；批次报告 reports/batch-HV-01.md |
| TRACING-01（24aae73） | 24 文件+toc 七步全流程；restore 24/24 首轮全过；validate 首轮 3 错误全真缺陷修复（logback ③ classpath→类路径 + ③ instrumentation 触发源为 dependency 行 groupId 属性文本——「MDC 集成」补述「MDC 插桩集成」；mdc ④ 标题补「（映射诊断上下文）」括注）；25 文件全绿；**glossary +6**（distributed tracing→分布式追踪、span→跨度、exporter→导出器、propagator→传播器、instrumentation→插桩、sampler→采样器）；批内锚 [[jdbc]]（ucp→<<jdbc,JDBC>>）译文首行注入；批次报告 reports/batch-TRACING-01.md |
| SESSION-01（20db6f4） | 13 文件+toc 七步全流程；restore 13/13 首轮全过；validate 14 文件全绿零豁免；语言切换属性行 [.lang-*] 整体保留、双语言变体分别译出；**glossary +1**（session resolution→会话解析）；批次报告 reports/batch-SESSION-01.md |
| 渲染冒烟 + P0 收口 | tracing 24/24、session 13/13、HV 4/4 全渲染 failureCount 0；三新页 href→id 悬空 0（[[jdbc]] 闭环实测）；**五页回归差异穷举核对全部为预期产物**（4 模块页各仅 module-bar +3 链接 1 行、landing 仅 3 处 todo→链接转换）；HTTP 冒烟 6 页全 200；看板+handoff 收口、tag v1.1、push(SSH) |

## 已完成清单（M4.1 会话 3，保留供追溯）

| 工作单元 | 说明 |
|---|---|
| 周检 | check_all 四快照模块全 0 变更（core cca2a1ce / security cc524538 / micrometer c4d064ee / validation 079f75dc），无需开 issue |
| SEC-03（35bb691） | 29 文件七步全流程；validate 112 文件全绿；注入 4 锚（[[oauth]]/[[openid-authorization-code]]/[[keys]] 消解 SEC-01/02 遗留豁免 3 条 + [[openid-configuration]] 批内闭环）；validate 拦 ⑦ 邻接 ×1、③ bean 口径 ×13 文件 18 处（新译大写 Bean 统一改小写）；术语 +4（refresh token/access token/Client Credentials Grant/nonce 不译；state/issuer 试用撤回）；批次报告 reports/batch-SEC-03.md |
| SEC-04（0289b8d） | 28 文件七步全流程；validate 140 文件全绿；**security 145 条目全部处置完成（140 current + 5 skipped = 100%）**；注入 [[protectedResourceMetadata]] + 回溯补注入 5 锚（runAs/jwks/ipPattern/interceptUrlMap/builtInEndpointsAccess）；③ bean 口径修正 ×4；批次报告 reports/batch-SEC-04.md |
| 全量渲染冒烟 + render 修复（3ee6dde） | security.html 144/144 片段全渲染、failureCount 0、产物时间戳实测更新；**10 锚 href↔id 全闭环**；实测发现 render.mjs 两处内容缺口并修复：①无页 toc 分组键官方站有 h2 锚而本站无 → 5 导航死链 → 分组键缺页输出标题级页头；②根层 securityRule/ldap.adoc 未入 toc → 已译内容静默缺失 → 未入 toc 片段按 basename 挂载同名分组键；③「部分译文」横幅改 missingPage 条件（100% 模块不再误显 139/144）；回归对照 core/micrometer/validation/landing 四页修复前后逐字节一致；悬空 href 终态 1 条（loginController，上游悬空官方亦无，M3 跟踪） |

## 已完成清单（M4.1 会话 1–2，保留供追溯）

| 工作单元 | 说明 |
|---|---|
| 周检 | check_all 三模块全 0 变更（core cca2a1ce / security cc524538 / validation 079f75dc），无需开 issue；未快照模块按预期跳过（退出码 1 系 -1 聚合，非异常） |
| SEC-02（32c25a0） | 40 文件七步全流程；validate 83 文件全绿（豁免 6 条=4 预期中间态 + loginController 悬空跟踪 + wwwAuthenticate 上游不平衡 xref 未登记豁免）；restore 首轮拦 2 处译丢段、validate 首轮拦 4 项（classpath×2 + csrfConfiguration 批内锚缺失 ×2）全部修复；**回溯补注入 4 处**（basicAuth/session/micronautSecurityAuthenticationCookie/IdToken，B16/B30 先例）；批内 csrfConfiguration 锚走译文首行路径（对 re-assemble 幂等）；术语 +2（sanitizer→净化器、token propagation→令牌传播）；批次报告 reports/batch-SEC-02.md |

| 工作单元 | 说明 |
|---|---|
| 周检双缺陷修复（a29e59d） | check_all.sh `${MEMGATE}` 引号致 127（4de82c6 起从未真正跑通，意外退出码聚合还会吞掉 127）；sync_upstream.py `--check/--apply` repo 解析曾一律取 --repo 缺省值（core），模块账本误比对 core 文档树产整树伪 diff（micrometer/validation 虚报 22+68 文件变更）——repo 解析改三级：--repo 显式 > 账本 upstream.remote > core 缺省；修复后三模块 check 全 0，无需开 issue |
| security 快照（0e2a358） | micronaut-security 5.2.x @ cc524538（默认分支实为 5.5.x，按 SOP 优先 5.2.x）；145 条目=144 adoc+toc.yml、33 图 5.9MB、5 壳 skipped；**.sketch 3.3MB 白名单外不入库**（坑位 25）；modules.json 补填 repo/SEC；inventory 切批 SEC-01…04（13173 非代码词） |
| SEC-01（016ecd3 + 5b2c185） | 42 文件+toc.yml 七步全流程；43 条目全 current；裸 `<<target>>` xref 11 目标确立「译显示文本+目标页注入 [[basename]]」口径（8 处注入，href↔id 渲染闭环实测）；glossary modules 分节 +9 条 security 术语；validate 43 文件全绿（豁免 2 条）；⑤ 登记表路径双前缀缺陷修复（016ecd3） |
| 渲染上线 | security.html（SEC-01 片段，55/144 渲染）0 真实失败；id="login"/"authenticationProviders"/"secured" 与对应 href 闭环实测通过；core/micrometer/validation 页无回归；**render 门禁修复（ca0c0f8）**：部分翻译模块不再硬拦 CI（missingPage 警告+诚实导航+部分译文提示），deploy-pages 曾被 8 条「zh 镜像缺失」拦死 |
| 图片体量复测 | security 单模块 resources 5.9MB（不含 .sketch）；71 模块外推 <300MB 结论维持，**git-lfs 不启用** |

## 状态快照（2026-11-23，M4.1 收官/会话 4 收尾）

- 分支 main，本会话 7 个提交（4f4642d 三模块快照 → 37e931b HV-01 → 24aae73 TRACING-01 → 20db6f4 SESSION-01 → docs 收口 + tag v1.1），已推送（SSH）；远程 https://github.com/jxsword/micronaut-zh-docs（push 走 SSH——坑位 14）
- **P0 安全与观测层 7 模块全部 100%（tag v1.1 已打）：core 388（387 current + 1 skipped）、security 145（140 current + 5 skipped）、micrometer 30/30、validation 12/12、hibernate-validator 5/5、tracing 25/25、session 14/14；validate/pytest 全绿无回归**
- 聚合站：index.html + **tracing.html / session.html / hibernate-validator.html（本会话新增）** + micrometer.html + validation.html + security.html + landing.html，全站 failureCount 0；五页旧页回归差异全部为 module-bar/landing 新增三模块链接（预期产物）
- glossary：45 通用 + 6 banned + modules.terms **25 条**（micrometer 2、validation 1、security 15、tracing 6、session 1——**修正：handoff 原记载「20 条/security 17」系过时口径**，SEC 批次中条目有合并，以本会话 YAML 实核为准）
- anchor-registry：148 锚未重扫（security wwwAuthenticate ×2 不平衡 xref 盲区维持实测结论 12 口径；tracing ucp→jdbc 的 ⑤ 警告同为 registry core 域盲区，[[jdbc]] 注入 + 冒烟闭环兜底）
- security 模块终态豁免跟踪 3 条维持：endpoints→loginController（上游悬空）+ wwwAuthenticate ×2（上游不平衡 xref）
- **预存在噪音备案（实测结论 18）**：core languageSupport/python/overloads.adoc 未入 toc 且无同名分组键（WARN、内容未渲染）——3ee6dde 起即存在，非本会话回归，随 core 批次/render 治理单独处理
- 下一会话首要：**M4.2 P1 数据与消息**（17 模块按组推进，详见待办）

## 实测结论（M4.0 结论 1–7 + M4.1 会话 1 结论 8–10 + 会话 2 结论 12–14 + 会话 3 结论 15–17 + 会话 4 结论 18–19，继承 M3 结论 1–8 与 B01–B32 全部结论）

1. **dest 前缀约定**：`--manifest manifests/<site>.yml` ⇔ `source/modules/<site>/` ⇔ `zh/modules/<site>/` ⇔ 账本 file 字段 `modules/<site>/…` ⇔ 页 `<site>.html` ⇔ 锚 `<site>-<basename>`——全部由 manifest 文件名 stem 一一推导，无第二处配置。
2. **模块结构同构性**：micrometer/validation 与 core 完全同构（guide/toc.yml + 嵌套 dict + title 键），segment/protect/validate/assemble/inventory 零改动复用成立；但**源文件可能是纯导读页**（metricsAndReporters.adoc 仅标题+一段，21 个 reporter 各为独立页）——切批后先 cat 源文件确认边界，勿按文件名推测内容。
3. **模块图片可为零**：试点两模块无 resources/；渲染 imagesdir=modules/<site>/img/ 仅在存在图片时可见（copyImages 摊平 resources/img → site modules/<site>/img/）。
4. **per-file commit 采集**：模块账本也走 `--collect-commits`（gh api 42 条全成功，串行+缓存按 remote slug 命名）；assemble 在 per-file commit 缺失时回退账本 baseline（与 mark-current 期望一致，两级兜底）。
5. **⑦ 邻接规则高频违规模式**：reporter 表格「默认值：`X`（1 分钟）」模式——统一改写「…，即 1 分钟」；「`X`（或某个…」枚举括注——重排列举顺序让（ 跟随 CJK 词。模块批次初稿先用 grep `}}（` 自查可省一轮 validate。
6. **④ 标题未译规则的 API 名处理**：≥2 英文词的标题（Micrometer Observation）保留 API 名 + 中文括注「（观测）」通过；单英文词标题（Configuration）可直接译中文。
7. **check_all 退出码聚合**：脚本内部逐模块采集退出码不掩码，最终取最严重值（2>1>0）——`set -e` 不能用，采集模式与「禁止 || true」纪律兼容。
8. **模块裸 `<<target>>` xref 口径**（security 首现，11 个页级目标）：译文译显示文本、保留 `<<target,译文>>` 原样，并在目标页 zh 片段首内容之前原位注入 `[[target]]`（B02 同款规则）；渲染端 href="#target" ↔ id="target" 天然闭环（idprefix=security- 只影响自动 id）；上游悬空引用（如 endpoints.adoc 的 <<loginController>>，官方站亦无此 id）保持原样走 ⑤ 豁免跟踪，不虚构目标。
9. **sync 模块账本 repo 解析口径**：`--check/--apply` 的上游仓库一律「--repo 显式 > 账本 upstream.remote > core 缺省」三级解析；`--manifest manifests/<site>.yml` 而不传 `--repo` 现在正确比对模块自身仓库（修复前整树伪 diff）。
10. **快照白名单口径**：read_upstream 仅入库 .adoc + toc/toc-python.yml + 图片白名单（.png/.svg/.gif/.jpg/.jpeg/.webp/.ico/.pdf）；白名单外扩展名（如 security 的 3.3MB .sketch 设计源）跳过并告警不入库——SOP §4「快照仅 .adoc+toc+resources 图片入库」的落地实现；新增类型需求时先在白名单显式添加再重快照。
11. **render 部分翻译模块口径**：toc 叶页 zh 镜像缺失=多批次推进的预期中间态，不再计渲染失败硬拦 CI（此前 deploy-pages 被 8 条「zh 镜像缺失」拦死，连带阻塞整站部署）；改计 missingPage 警告 + 跳过片段 + 导航只显示已译叶页 + 页头「部分译文 N/M 页」提示；退出码只看真实渲染失败。预存在噪音：asciidoctor「no callout found」警告 core 时代就有（M4.0 成功部署 540 条），非回归。
12. **上游不平衡 xref 是 check_anchors 的扫描盲区**：security 上游存在 `<<basicAuth, basic auth>` 缺右 `>` 的笔误（wwwAuthenticate.adoc），check_anchors 的 xref 正则按平衡括号匹配，扫描不到该引用 → registry 无条目 → validate ⑤ 走「裸锚点未登记，豁免（M3 跟踪）」警告分支而非目标存在性检查。渲染层闭环不依赖 registry：显式锚注入（[[basicAuth]]）后 href↔id 天然闭环，由渲染冒烟实测兜底。SEC-04 的 protectedResourceMetadata 同型（`<<protectedResourceMetadata, Resource Metadata>`），届时同口径处理。不为此改 check_anchors 正则（上游笔误语义等价保留，改脚本需走基建冒烟纪律）。
13. **批内目标锚走译文首行注入路径**：被批内文件引用的目标页（如 csrfConfiguration），其 [[basename]] 写在 `-translated.txt` 首行，restore→assemble 后自动落位于 zh 片段首内容之前——与 SEC-01 直接 Edit zh 片段等价且对后续 re-assemble 幂等（SEC-01 直接 Edit zh 的注入会在该页被重新 assemble 时丢失，本批 4 处回溯注入亦落 zh，若未来 re-assemble 需按批次报告口径重放）。
14. **restore 门禁对 URL 显示文本占位符同样生效**：译显示文本时若把 {{PROTECTED_URL_*}}[...] 的占位符整体丢弃（只译了文字），restore 按「映射项在译文中缺失」拦截——本批 jwtValidation（qualified）与 doubleSubmitCookiePattern（Cookie prefix）各 1 处。自查模式：翻译带 [显示文本] 的 URL/XREF 占位符时，占位符必须原样保留在译文中。
15. **render.mjs 对无页 toc 分组键的官方口径**（SEC-04 全量冒烟实测）：官方构建为无自身 .adoc 的 toc 分组键（如 security 的 flows/oauth-endpoints/reader/securityRule/ldap）生成 `<h2 id="security-<键>">` 标题页头；模块渲染此前不生成 → 导航分组标签死链。修复口径：toc dict 节点（group）缺页时输出标题级页头（depth>0 用 `===` 模板，h2 与官方一致；depth=0 走原章页路径），missingChapter 计数、missingPage 不计。同批实测发现根层 securityRule.adoc/ldap.adoc 未入 toc → 片段清单不含 → **已译内容静默缺失**；官方站将其内容渲染在同名分组标题下——修复为未入 toc 片段按 basename 匹配挂载同名分组键（host = f.rel.endsWith("/<basename>.adoc") 的缺页分组），无匹配打印 WARN。回归纪律：改动后 core/micrometer/validation/landing 逐字节对照（备份 /tmp/render-smoke-before 口径）全一致才可提交。
16. **「部分译文」横幅条件以 missingPage（真实未译叶页）为准**：skipped 壳与分组键页头不计入分母/条件——security 100% 后横幅自动消失；模块推进中途真实未译页存在时横幅仍按设计出现。重复自动 id（多模块同名 CJK 标题如「自定义」，core 8 处/micrometer 1 处）为预存在噪音，无 href 指向、导航不受影响，暂不处理。
17. **③ 必译术语对通用英文词会系统性误报**（B22 滚动回流教训的通用化）：SEC-03 曾将 state/issuer 写入 glossary 又撤回——"state"/"issuer" 在既有 7 文件散文中各有语境（csrfMitigations「状态」、whatsNew 等），③ 按「en 词出现→zh 词必须命中」检查必然误报。收录判定口径：**词形独特（nonce/Claims 级）或限定词组（refresh token/Client Credentials Grant 级）才收；单词通用词（state/issuer/bean 除外——bean 有 glossary 显式口径）不收**，句内首现括注即可。另：新译文件中大写「Bean」是 ③ 高频误报源（SEC-03 ×13 文件 18 处、SEC-04 ×3 文件 4 处），译文遇 bean 概念一律小写「bean」（glossary 上游惯例口径）。
18. **新模块入站会使五页回归对照出现预期差异**（TRACING-01 冒烟实测）：modules.json 补填/快照落地后，重渲染的旧页 module-bar 与 landing 导航会新增该模块链接/解除 todo 态——实测结论 15 的「逐字节一致」判定须升级为「**差异穷举核对**」：行级 diff 穷举全部差异行，确认每行均为预期的导航增链（4 模块页各 1 行 module-bar + landing 3 处 todo→链接），无其他字节变化即视为回归干净。另一实测口径：1.4MB 单行大 HTML 上 SequenceMatcher 穷举会超时，行级 diff（`tr '>' '>\n'` 切行后 diff/uniq）是分钟级以下的可行口径。同批 WARN 备案：core languageSupport/python/overloads.adoc 未入 toc 且无同名分组键可挂载（内容未渲染）——备份页同样缺失，3ee6dde 起即存在，属预存在缺口非回归，随 core 批次/render 治理单独处理。
19. **dependency: 宏行是 ③ 术语检查的扫描盲区来源**：dependency 行不被 protect 占位符化（逐字节保留），其 groupId="io.opentelemetry.instrumentation" 属性文本会触发 ③ 的必译术语检查（logback ③ instrumentation 实测）——处置口径：按语义在该文件散文中合法落出对应中文术语（「MDC 集成」→「MDC 插桩集成」，mdc.adoc 原文即称 instrumentation），不为此改保护器/校验器。同类触发源预判：groupId=io.micronaut.tracing（tracing 术语 ③ 首现于批内已闭环）、io.opentelemetry.contrib 等非词组 id 不触发。

## 待办（下一会话：M4.2 P1 数据与消息，17 模块）

1. **开工前置（P1 逐模块）**：data★ / sql / r2dbc / mongodb / redis / neo4j / cassandra / coherence / eclipsestore / liquibase / flyway / kafka / rabbitmq / nats / jms / pulsar / mqtt——逐一 gh api 核实 repo slug 与分支（modules.json 均 repo=null，分支优先 5.2.x，缺失用默认分支并实测 docs 树一致性），补填 modules.json → 快照 → inventory 切批；jackson-xml/sql/kotlin 类 slug 404 教训（M4.0 实测）提示部分模块文档可能不在预期仓库，开工先实测。
2. **分组推进顺序**（按组穿插避免单仓库长驻）：data 单独 2–3 会话级（≥40 页头部模块按章节化批次）；sql+liquibase+flyway / mongodb+redis+neo4j+cassandra / coherence+eclipsestore / messaging 6 模块（kafka/rabbitmq/nats/jms/pulsar/mqtt）。每批七步流程 + squash commit + 批次报告。
3. **渲染冒烟**：每模块收口跑 render + 回归对照（**实测结论 18 口径：差异穷举核对**——新模块入站必致旧页 module-bar/landing 增链，逐字节一致不再可期）；未入 toc 片段 WARN 需人工核对；图片模块（mongodb/redis/kafka 等可能有 resources/）留意快照体量与 imagesdir 渲染。
4. **M4.2 收口**：17 模块 100% 后 progress 全绿 → 看板收口 → **tag v1.2**（层间收尾，主动产出交接并建议开新会话——纪律 9）。
5. **周检例行**：`bash scripts/check_all.sh`（现 7 模块有账本）；检出变更开 issue `[upstream-sync][<site>] <sha>`；core 增量优先（DR-006 §6，同会话不混排）。
6. 届时单独决策（DR-007 起）：5.3.x 基线切换、guides 二期、Maven/Platform 外链、configuration-reference、render 重复自动 id 噪音、**core overloads 未入 toc 缺口（实测结论 18 备案）**。

## 调试经验与坑位（M4.1 会话 1 增补 24–25，继承 1–23）

24. **包装变量必须不加引号展开**：check_all.sh `out="$("$MEMGATE" python3 …)"` 中 `"$MEMGATE"` 把 `memgate 2048` 当单个命令名查找 → 127，且聚合 case 无 `0)` 分支时补 `*)` 会把 0 也吞成 2（本次两改三错后收敛）；包装变量一律 `$MEMGATE`（依赖分词语义）。4de82c6 起该脚本从未真正跑通过——**「基建脚本提交前必须实跑一遍带产物核对的冒烟」**升级为硬性纪律。
25. **快照硬上限与白名单口径**：security 的 resources/img/security_diagramms.sketch（3.3MB）触发 2MB 单文件硬上限导致 --init 直接失败；按 SOP §4 口径改 read_upstream：白名单外扩展名跳过并告警不入库（guide/ 0 引用、core 全为白名单类型实测无回归）。2MB 上限仍护账本跟踪文件（解析保护本意），不再误伤镜像二进制。
26. **CLI 契约须先 --help 核对再调用**：protect --restore 的 FILE 参数是「译文文件路径」而非源路径——传源路径时 map 路径回退成源文件自身（名称无 -translated.txt 后缀不替换）→ 把 .adoc 当 JSON 解析报 JSONDecodeError，报错形态与真实原因相距甚远。
27. **toc.yml 注释头的溯源字段必须从账本取值，禁止凭记忆手写**（SESSION-01 实测险情）：upstream_commit 与 upstream_hash 双字段手写时 hash 写错（账本真值 57baa510…，手写值不符）——mark-current 会按 hash+commit 双字段校验拒绝核销，属门禁可拦缺陷，但正确做法是先 grep 账本再落笔；--mark-current 是最后一道闸，不应作为取数途径。
28. **P0 三模块开工实测补充**：repo slug 命名规律 micronaut-projects/micronaut-<site>（三模块全命中，与 security/micrometer/validation 一致）；tracing 类自有版本线仓库（6.x/7.x/8.x，无框架对齐分支）判定口径=「SOP §4 默认分支回退 + docs 树与官方 5.2.x 页一致性实测（blob sha 比对/官方页徽标）」，双重验证后即可安全使用非框架线 ref。
|---|---|
| 基建套件（4de82c6） | sync_upstream.py `--doc-root/--manifest` 参数化（manifests/<site>.yml ↔ modules/<site>/ 前缀一一对应，账本顶层 ref+locked_at，克隆缓存按仓库 slug 分目录）；validate `--manifest` + ⑤ 模块文档树前缀 + ③ 扫描集=通用+当前模块术语；assemble_zh 模块账本/toc/官方 URL（core 引用块格式 385 文件逐字节不变实测）；inventory `--manifest`+批次前缀（modules.json batch_prefix）；progress 多账本聚合按模块分组；render.mjs 聚合（modules.json 驱动逐模块单页 + landing.html 官方 18 组导航复刻 + 各页顶部模块切换条）；新增 check_all.sh；CI validate/sync workflows 模块化；pytest 100→123 绿 |
| 试点快照（6e33c11） | micrometer（30 文件，基线 c4d064ee3af4）+ validation（12 文件，基线 079f75dc6ba8），ref 5.2.x + locked_at 2026-11-23；无 0 字节壳、无图片；inventory 切批 MICRO-01(27 文件 3239 词)/MICRO-02(2 文件 327 词)/VALID-01(11 文件 1463 词) |
| MICRO-01（9fac35a） | 27 文件七步全流程；⑦ 行内码紧跟全角括号 41 处改写；② 门禁拦下 metricsAndReporters 误并内容（导读页实为标题+一段）；toc.yml 导航标题随批译出 |
| MICRO-02（bdc535c） | observation/repository；④ 标题保留 API 名加括注；模块 30 条目全 current |
| VALID-01（c9601ae） | 11 文件全模块；③ constraint→约束 module 作用域术语生效；④ 版本标题「…的破坏性变更」；模块 12 条目全 current |
| 渲染上线 | 聚合站 core+micrometer+validation+landing 0 失败；core 剔除模块条后与 DR-005 版逐字节一致、809 个 core- 锚点零差集；本地 http://127.0.0.1:8321 冒烟 4 页 200 |
| 图片体量实测（LFS 决策） | 试点两模块 0 图；gh api 抽样：security 8.9MB/34 图、oracle-cloud 4.5MB/28 图、aws 0.9MB/4 图、openapi/data ≤0.1MB（jackson-xml/sql/kotlin 等仓库 slug 或分支 404 未计入）——**外推 71 模块 <300MB，暂不启用 git-lfs**；security 快照落地时（P0）复测 |
| 看板模块维度 | translation-board.md 增「模块批次总览」节（MICRO-01/02、VALID-01 + LFS 结论 + M4.1 待办） |

## 调试经验与坑位（M4.0 增补 19–23）

19. **asciidoctor fragment 渲染冒烟要看「产物时间戳」而非退出码**：render.mjs 曾因 `esc` 函数作用域错误在 moduleBar 处 ReferenceError 退出，但旧 index.html 仍在位——「对比无回归」变成新旧同文件的空验证。核对 `ls -la build/site/*.html` 时间戳或 diff 前先确认产物确已重写。
20. **scripts/preview/.gitignore 相对路径**：其内模式相对该目录解析（`scripts/preview/node_modules/` 写在其内永不生效）；node_modules/ 已上收至根 .gitignore 全局兜底。
21. **workdir/protect 是会话工作区不入库**：*-translated.txt / *-restored.txt / map.json 均为临时件；批次收尾只落盘 zh/ 与报告，需要复跑时按批次报告口径从 source/ 重新 protect。
22. **memgate 包裹 setsid 长驻服务**：`setsid memgate 2048 python3 -m http.server 8321 >/dev/null 2>&1 < /dev/null & disown`（坑位 15 的成熟变体）；memgate 在 PATH 时 check_all.sh 自动采用，CI 无 memgate 直跑（脚本内 command -v 判断）。
23. **git add 通配漏交子目录与 .yml（M4.0 实际事故，两个 fix commit 才补齐）**：`git add zh/modules/micrometer/guide/*.adoc` 根级通配不递归子目录、也不匹配 toc.yml——21 个 reporter 译文 + 导航 toc 全部漏交，CI 渲染只剩 8 个片段而本地 29 个（本地磁盘文件齐全、render 成功，掩盖了漏交）；上线后 404 才暴露。**纪律升级：模块批次 add 一律整目录（`git add zh/modules/<site>/ …`），提交前 `git status --short` 复核零遗漏，再以 CI 渲染 fragments 数与本地 render JSON 对照。**

## 硬性纪律清单（继承，持续有效）

1. `docs/翻译计划-模块扩展.md`（范围/架构）+ `docs/翻译计划.md` v1.1（流程）为唯一权威规范；改架构走 decision_log（DR-007 起递增）
2. 所有脚本 memgate 包裹；`source/` 只读（仅 sync 写入）；`manifest.yml` 与 `manifests/*.yml` 禁人工直改（--mark-current 除外）
3. 门禁硬性化，禁止 `|| true`
4. 每批次 squash commit（消息含模块批次号/段数/词数/上游日期）+ 批次报告；决策类提交末行 `Decision: DR-编号`
5. agent 并发上限 = 串行 1；上下文过半立即交接；里程碑收尾主动建议开新会话
6. git push 走 SSH；网络直连失败走代理 http://192.168.33.1:10808
7. 基建脚本提交前必须实跑一遍带产物核对的冒烟（坑位 24：check_all.sh 4de82c6 起从未真正跑通）；调用脚本子命令前先 `--help` 核对参数契约（坑位 26）
