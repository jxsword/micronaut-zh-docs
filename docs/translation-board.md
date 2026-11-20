# 批次看板（translation-board）

> 批次切分与文件清单以 reports/inventory-5.2.25.md 为准（32 批，双指标 非代码词 ≤3500 且 总词 ≤5500）。
> 状态机：pending → in-progress → translated → reviewed → current（核销走 sync --mark-current）。

## 批次总览

| 批次 | 文件数 | 非代码词 | 总词 | 状态 |
|---|---:|---:|---:|---|
| B01 | 19 | 3347 | 3355 | current |
| B02 | 12 | 3049 | 3082 | current |
| B03 | 10 | 3443 | 3454 | current |
| B04 | 19 | 2591 | 2604 | current |
| B05 | 2 | 2138 | 2128 | current |
| B06 | 11 | 3454 | 3489 | current |
| B07 | 4 | 2507 | 2554 | current |
| B08 | 4 | 3397 | 3442 | current |
| B09 | 8 | 2915 | 2915 | current |
| B10 | 5 | 3086 | 3092 | current |
| B11 | 7 | 3350 | 3352 | current |
| B12 | 25 | 3454 | 3460 | current |
| B13 | 17 | 3167 | 3185 | current |
| B14 | 13 | 3482 | 3476 | in-progress |
| B15 | 13 | 3452 | 3485 | current |
| B16 | 24 | 3223 | 3291 | current |
| B17 | 15 | 3004 | 3008 | current |
| B18 | 8 | 3379 | 3379 | current |
| B19 | 14 | 3455 | 3491 | current |
| B20 | 21 | 3456 | 3512 | current |
| B21 | 35 | 2983 | 3078 | current |
| B22 | 5 | 3062 | 3057 | current |
| B23 | 6 | 3378 | 3353 | pending |
| B24 | 5 | 3257 | 3199 | pending |
| B25 | 7 | 3096 | 3070 | pending |
| B26 | 14 | 3416 | 3439 | pending |
| B27 | 17 | 3478 | 3538 | pending |
| B28 | 21 | 2955 | 3023 | pending |
| B29 | 14 | 3226 | 3257 | pending |
| B30 | 4 | 3387 | 3401 | pending |
| B31 | 3 | 955 | 960 | pending |
| B32 | 2 | 3180 | 3183 | pending |

## 批次状态明细

批次 → 文件清单：见 inventory 报告「逐批次文件清单」节（B01–B32）。

## 备注

- B01（2026-11-20 完成）：validate 七项全绿 + 19/19 --mark-current 核销 + squash commit。实测修复 M1 缺陷 4 处（check_anchors http 前缀裸锚点误跳过 → registry 116→121；validate ⑤ 裸锚点误报 + reg_ids 放行收紧；禁繁体表简繁共用字误报）与 segment_adoc snippet:: 指令行补录；新增 scripts/assemble_zh.py（溯源投影装配）。官方站单页锚点实测为 core-<basename>；上游 httpServer/httpClient/certificates 三章未被官方站渲染（详见 reports/batch-B01.md）。冻结窗口遵守：批次期间未运行 sync --apply。
- B02（2026-11-21 完成）：validate 全量 31 文件 PASSED + 12/12 --mark-current 核销 + squash commit；进度 31/388（8.0%）。锚点注入 4 处（types/qualifiers/scopes/refreshable，统一规则：basename 锚点 = 片段首内容之前）。术语转正 3 条（qualifier/eager initialization/meta annotation）；修复 validate ③ strip_code 指令行误报（snippet:: 宏参数触发必译术语，pytest 95 绿）。词数以批次实测为准（3055/2991，M1 报告值系 snippet:: 修复前口径）。⑤ 豁免警告 29 条（详见 reports/batch-B02.md）。冻结窗口遵守。
- B03（2026-11-21 完成）：validate 全量 41 文件 PASSED + 10/10 --mark-current 核销 + squash commit；进度 41/388（10.6%）。锚点注入 5 处（factories/conditionalBeans/replaces/events/introspection，批内引用 conditionalBeans 闭环）。术语转正 3 条（factory/introspection/graceful shutdown）；dependency:: 宏与上游 TODO 注释按纪律处理。词数实测 3417/3377。⑤ 豁免警告 31 条（详见 reports/batch-B03.md）。冻结窗口遵守。
- B04（2026-11-21 完成）：validate 全量 60 文件 PASSED + 19/19 --mark-current 核销 + squash commit；进度 60/388（15.5%）。锚点注入 4 处（staticAtCreator/introspectedAnnotationOnAConfigurationClass 批内闭环 + propertyMembers/beanValidation）。introspection→内省 全章一致命中（B03 提前转正得到验证）。restore 哈希门禁拦截 1 处占位符笔误（6232a110↔fbd67c3f），修正后 19/19 全过。词数实测 2588/2545。⑤ 豁免警告 34 条（详见 reports/batch-B04.md）。冻结窗口遵守。
- B05（2026-11-21 完成）：validate 全量 62 文件 PASSED + 2/2 --mark-current 核销 + squash commit；进度 62/388（16.0%）。锚点注入 1 处（[[annotationMetadata]]，B01 ioc.adoc 引用闭环）。reviewer 脚本收紧（代码块段不计停用词漏译检测）；validate ⑦ 邻接违规 3 处修正后全绿。词数实测 2074/2076。⑤ 豁免警告 35 条（详见 reports/batch-B05.md）。冻结窗口遵守。B02–B05 完成后 IoC 章核心（注入/限定符/作用域/生命周期/事件/内省/元数据）已全部译出。
- B06（2026-11-21 完成）：validate 全量 73 文件 PASSED + 11/11 --mark-current 核销 + squash commit；进度 73/388（18.8%）。锚点注入 5 处（reflection/classImport/nullabilityAnnotations/jspecify/environments；classImport 批内 mixin 引用闭环、nullabilityAnnotations+jspecify 与 whatsNew 批间闭环）。对译 reviewer 11/11 PASS。词数实测 3482/3445（总词/非代码）。⑤ 豁免警告 36 条（+3 新增 −2 消解，详见 reports/batch-B06.md）。冻结窗口遵守。**IoC 章 55 文件全部 current——IoC 全章译出。**
- B07（2026-11-21 完成）：validate 全量 77 文件 PASSED + 4/4 --mark-current 核销 + squash commit；进度 77/388（19.8%）。锚点注入 2 处（propertySource/valueAnnotation，片段首内容之前；config.adoc/whatsNew/nullableInjection 5 条既有豁免消解，批内 propertySource→valueAnnotation 闭环）。对译 reviewer 4/4 PASS（propertySource 75 段/123 占位符为 config 章最长文件）。词数实测 2540/2484。⑤ 豁免警告 32 条（+1 新增 −5 消解，详见 reports/batch-B07.md）。冻结窗口遵守。config 章 current 7/15（47%）。
- B08（2026-11-21 完成）：validate 全量 81 文件 PASSED + 4/4 --mark-current 核销 + squash commit；进度 81/388（20.9%）。锚点注入 2 处（evaluatedExpressions/configurationProperties）+ 源内显式锚点 configurationPropertiesAccessorsStyle 保留；5 条既有豁免消解（config.adoc/whatsNew/introspectedAccessorsStyle/beanMappers×2）。reviewer 4/4 PASS（首轮 1 条为脚本对指令行 title 的误报，检查范围修正）。validate ⑦ 邻接违规 ×2 修复（占位符后漏空格）。词数实测 3400/3336。⑤ 豁免警告 27 条（−5 消解，详见 reports/batch-B08.md）。冻结窗口遵守。config 章 current 11/15（73%）。
- B09（2026-11-21 完成）：validate 全量 89 文件 PASSED + 8/8 --mark-current 核销 + squash commit；进度 89/388（22.9%）。锚点注入 5 处（aop/aroundAdvice/introductionAdvice/bootstrap/jmx）；aop ×3 豁免消解（whatsNew/annotationMetadata/factories 批间闭环）+1 新增（bootstrap→distributedConfiguration）。reviewer 8/8 PASS（脚本术语检查改为复用 validate ③ 同源 check_terms）。词数实测 2852/2835。⑤ 豁免警告 25 条（详见 reports/batch-B09.md）。冻结窗口遵守。**config 章 15/15 全部 current——config 全章译出**；AOP 章 3/10 起步。
- B10（2026-11-21 完成）：validate 全量 94 文件 PASSED + 5/5 --mark-current 核销 + squash commit；进度 94/388（24.2%）。锚点注入 4 处（lifecycleAdvice↔interceptorLifecycle 批内互引闭环 + retry/validation）；**retry 首轮漏注入被 reviewer 抓出后补齐**（唯一真缺陷）；validate 首轮 caching ③（补 CacheInterceptor（缓存拦截器）括注）与 retry ⑦（占位符后漏空格）修正。词数实测 3022/3002。⑤ 豁免警告 23 条（−2 消解，详见 reports/batch-B10.md）。冻结窗口遵守。AOP 章 8/10（80%）。
- B11（2026-11-21 完成）：validate 全量 101 文件 PASSED + 7/7 --mark-current 核销 + squash commit；进度 101/388（26.0%）。锚点注入 4 处（httpServer/runningSpecificPort 批间消解 +2 + routing/binding）+ **页内标题锚 [[_uri_path_variables]] 原位注入首实践**（PLAN §5.6）；httpServer ③ netty→Netty 误报修正（正文普通词物化）。词数实测 3270/3240。⑤ 豁免警告 24 条（−2 消解 +3 新增，详见 reports/batch-B11.md）。冻结窗口遵守。**AOP 章 10/10 全部 current——AOP 全章译出**；httpServer 章 5/15 起步。
- B12（2026-11-21 完成）：validate 全量 126 文件 PASSED + 25/25 --mark-current 核销 + squash commit；进度 126/388（32.5%，本工程最大批次）。锚点注入 4 处（jsonBinding 批内 5 文件闭环 + localeResolution/bindingUsingPOJOs/serializationUsingJacksonDatabind）；jsonBinding 漏锚点被 validate ⑤ 门禁抓出补齐 + ⑦ 邻接 ×1 修正。词数实测 3363/3336。⑤ 豁免警告 26 条（−1 消解 +3 新增，详见 reports/batch-B12.md）。冻结窗口遵守。httpServer 章 11/15 + jsonBinding 组 11 文件 current。
- B13（2026-11-21 完成）：validate 全量 143 文件 PASSED + 17/17 --mark-current 核销 + squash commit；进度 143/388（36.9%）。锚点注入 3 处（exceptionHandler 批内 errorFormatting 闭环 + form/formCapable 消解 whatsNew ×2）；validate 首轮 errorFormatting ⑦（占位符后漏空格）与 apiVersioning ③（宏路径误触 interceptor，补「（客户端拦截器配置）」括注）修正。词数实测 3122/3076。⑤ 豁免警告 27 条（−2 消解 +3 新增，详见 reports/batch-B13.md）。冻结窗口遵守。httpServer 组 46/101（46%）；errorHandling 组与 form 组全组 current。
- B14（2026-11-21 完成）：validate 全量 156 文件 PASSED + 13/13 --mark-current 核销 + squash commit；进度 156/388（40.2%）。锚点注入 5 处（filtermethods/httpServerFilter 批内闭环 + uploads/order 消解 whatsNew ×2 + filters）；transfers ⑦ 邻接 ×2（含加粗标记 `*响应式流*（`）修正。词数实测 3410/3402。⑤ 豁免警告 26 条（−2 消解 +1 新增，详见 reports/batch-B14.md）。冻结窗口遵守。httpServer 组 59/101（58%）；filters 子目录全组 current。
- B15（2026-11-21 完成）：validate 全量 169 文件 PASSED + 13/13 --mark-current 核销 + squash commit；进度 169/388（43.6%）。锚点注入 2 处（sessions 批内 websocketServer 闭环 + http3Server 消解 whatsNew）；byteBodySplitting/websocketClient ⑦ 邻接 ×3（占位符后漏空格）修正。词数实测 3457/3416。⑤ 豁免警告 31 条（−1 消解 +6 新增，详见 reports/batch-B15.md）。冻结窗口遵守。httpServer 组 72/101（71%）；byteBody 与 websocket 子目录全组 current。
- B16（2026-11-21 完成）：validate 全量 193 文件 PASSED + 24/24 --mark-current 核销 + squash commit；进度 193/388（49.7%）。锚点注入 8 处（threadPools/listener/cors/corsConfiguration/corsCrossOrigin* ×2/https/serverConfiguration，9 条豁免消解）；**回溯补注入 [[events]]**（B03 报告声称注入但实际缺失，本批 netty* 引用触发 validate ⑤ 硬拦后补齐）；⑦ 邻接 ×3 与 https ③ netty→Netty 修正。词数实测 3265/3193。⑤ 豁免警告 24 条（详见 reports/batch-B16.md）。冻结窗口遵守。httpServer 组 96/101（95%）；serverConfiguration 子目录全组 current。
- B17（2026-11-21 完成）：validate 全量 208 文件 PASSED + 15/15 --mark-current 核销 + squash commit；进度 208/388（53.6%）**过半**。锚点注入 5 处（httpClient 批间消解 ×3 + nettyHttpClient/jdkHttpClient 批间+批内闭环 + lowLevelHttpClient 批间消解 + clientStreaming 承接）；restore 译丢段门禁拦截 clientBasics 漏 callout（补齐）；clientPostRequests ⑦ ×1 修正。词数实测 2893/2870。⑤ 豁免警告 21 条（−6 消解 +3 新增，详见 reports/batch-B17.md）。冻结窗口遵守。**httpServer 章 101/101 全章译出**（第六个全章）；httpClient 章 9/26 起步。
- B18（2026-11-21 完成）：validate 全量 216 文件 PASSED + 8/8 --mark-current 核销 + squash commit；进度 216/388（55.7%）。锚点注入 2 处（clientAnnotation/proxyClient，4 条豁免消解）；**reviewer 段落对齐第三次拦截真缺陷**（proxyClient 尾段与 clientAnnotation 首段跨文件错位，互相归位）；clientParameters 上游 `////` 注释块逐字节保留（启发式 3 条误报已文档化）；proxyClient ⑦ ×1 修正。词数实测 3303/3282。⑤ 豁免警告 22 条（−4 消解 +5 新增，详见 reports/batch-B18.md）。冻结窗口遵守。httpClient 组 17/26（65%）。
- B19（2026-11-21 完成）：validate 全量 230 文件 PASSED + 14/14 --mark-current 核销 + squash commit；进度 230/388（59.3%）。锚点注入 3 处（clientFilter 批内闭环 + clientHttp3/contextPropagation 批间消解）+ 源内显式锚 certificates 保留（https ×2 消解）；restore 第 4 次拦截译丢段（clientFilter 漏 snippet 占位符）；nettyPooling ⑦ ×4、contextPropagation ⑦ ×2、certificates ③ classpath 修正。词数实测 3471/3424。⑤ 豁免警告 18 条（−4 消解，详见 reports/batch-B19.md）。冻结窗口遵守。**httpClient 章 26/26 全章译出（第七个全章）**；contextPropagation 组 2/2；cloud 章 1/17 起步。
- B20（2026-11-21 完成）：validate 全量 251 文件 PASSED + 21/21 --mark-current 核销 + squash commit；进度 251/388（64.7%）。锚点注入 7 处（cloudConfiguration/distributedConfiguration/distributedConfigurationVault/serviceDiscovery/serviceDiscoveryManual/serverlessFunctions 批间消解 7 条豁免 + clientSideLoadBalancing 批内闭环）；validate 逐个 --file **首轮 21/21 全绿（B01 以来首次批次内零修正）**；restore 第 5 次拦截真缺陷（Route53 两占位符丢右花括号，修复后全过）。词数实测 3512/3456（与 M1 inventory 一致）；段落 277。⑤ 豁免警告 11 条（−7 消解 +0 新增，详见 reports/batch-B20.md）。冻结窗口遵守。**cloud 章 17/17 全章译出（第八个全章）**；serverlessFunctions 组 3/4。
- B21（2026-11-21 完成）：validate 全量 286 文件 PASSED + 35/35 --mark-current 核销 + squash commit；进度 286/388（74.1%，剔 skipped 口径）。**全程最大批次（35 文件）逐组推进**；锚点注入 7 处（5 basename 片段锚 + 2 标题锚——sqlSupport 页内标题锚注入标题行之前；hibernateSupport/logging 消解 2 条豁免 + sqlSupport 批内闭环，groovy→cli +1 新增豁免）；restore 35/35 首轮全过（B20 回读习惯生效，零花括号缺陷）；validate 首轮 33/35（mongoSupport ③ Reactive Streams→响应式流物化、java9 ⑦ 占位符后漏空格），修复后全绿；reviewer 35/35 PASS 首轮零缺陷；占位符多重集校验发现 6 文件语序重排（合法）。词数实测 3078/2983（与 M1 inventory 一致）；段落 298。glossary +2（消息代理/发布者确认，现 25 术语）。⑤ 豁免 11→10 条（详见 reports/batch-B21.md）。冻结窗口遵守。**五个组全章译出（第九至第十三个全章）：serverlessFunctions 4/4、messaging、commandLineApps、configurations、logging**；languageSupport 章 8/50 起步。
- B22（2026-11-21 完成）：validate 全量 291 文件 PASSED + 5/5 --mark-current 核销 + squash commit；进度 291/388（75.4%，剔 skipped 口径）。锚点注入 0 处（registry 实测该 5 文件无登记引用）；validate 首轮 3/5（pythonRuntime ⑦ ×2、pythonThreading ⑦ ×1——行内码/占位符后紧跟全角开括号）修复后全绿；reviewer 5/5 PASS 首轮零缺陷。**glossary 滚动回流新错误模式**：新术语 visitor 收录触发既有文件 ③ ×3（evaluatedExpressions/annotationMetadata 宏路径误触补括注、classImport B06 旧译「访问器」统一为「访问者」）。词数实测 3045/3048（M1 值 3057/3062，口径基数差异以实测为准）；段落 104。glossary +6（访问者/装饰器/GIL/上下文池/虚拟线程/仪表，现 31 术语）。⑤ 豁免维持 10 条（0 消解 0 新增）。冻结窗口遵守。python 子章 6/24（B23–B25 继续 18 文件）；languageSupport 章 13/50（26%）。

## 硬性纪律（每批次必守）

1. 认领批次先在本表改状态为 in-progress；同一文件严禁两个 agent 并发写（agent 并发上限 = 串行 1）
2. 批次进行期间为冻结窗口：禁止 sync --apply（初译期本就被门控禁用）；检测到的变更记录于本表备注
3. SOP 按 PLAN §5.1 七步走：protect → translator → restore → reviewer 五项 → validate 全绿 → --mark-current 核销 → squash commit + 批次报告
4. 术语先写回 glossary.yml 再继续；banned 0 命中是硬门禁
5. 被引用标题按 config/anchor-registry.yml 原位注入 [[原锚点]]
6. 每批次 squash commit（message 含批次号/段数/词数/上游日期）+ reports/batch-<N>.md 报告
7. 收尾更新本看板与 docs/handoff-latest.md
