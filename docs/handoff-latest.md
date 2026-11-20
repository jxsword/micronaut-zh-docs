# 交接文档（handoff-latest）

> 更新：2026-11-21 ｜ 会话：M2 分批翻译（**B07–B19 共十三批全部完成并提交**，进度 59.3%）｜ 下一会话任务：M2 继续分批翻译（B20 起）

## 已完成清单（全部已提交，main 分支）

| 工作单元 | 提交 | 说明 |
|---|---|---|
| M0 余项 | `67fd538` | README / LICENSE / LICENSE_TRANSLATION.md |
| M1 基建（六脚本+tests+config+CI+快照+切分） | `2fb7425`…`e72d9ef` | pytest 86 绿 |
| **B01–B06 翻译批次** | `b03bf56`…`2e5a662` | 74 文件：Introduction/QuickStart/IoC 全章 + config 开头；详见各自 `reports/batch-B0{1..6}.md`；B06 后 IoC 章 55/55 全章译出 |
| **B07 翻译批次** | `abef899` | 4 文件（config：defaultEnvironment/banner/propertySource/valueAnnotation）；词数 2540/段落 167；锚点 2 处；⑤ 豁免 36→32 |
| **B08 翻译批次** | `f1fa4cf` | 4 文件（config：evaluatedExpressions/configurationProperties/customTypeConverter/eachProperty）；词数 3400/段落 260；锚点 2 处；⑦ ×2 修复 |
| **B09 翻译批次** | `a18c135` | 8 文件（config 收尾 4 + AOP 开头 4）；词数 2852/段落 125；锚点 5 处；**config 章 15/15 全章译出**；advice 统一译「通知」；reviewer 术语检查改与 validate ③ 同源 |
| **B10 翻译批次** | `cb89326` | 5 文件（AOP：lifecycleAdvice/interceptorLifecycle/validation/caching/retry）；词数 3022/段落 140；锚点 4 处（批内互引）；retry 漏锚点被 reviewer 抓出补齐 |
| **B11 翻译批次** | `ca907e4` | 7 文件（AOP 收尾 2 + httpServer 章页与前 4 节）；词数 3270/段落 206；锚点 4 处 + **页内标题锚 [[_uri_path_variables]] 原位注入首实践**；**AOP 章 10/10 全章译出** |
| **B12 翻译批次** | `d1dbc49` | 25 文件（reactiveServer 组 11 + jsonBinding 组 14，最大批次）；词数 3363/段落 260；锚点 4 处；jsonBinding 漏锚点被 validate ⑤ 拦截补齐；大批次工作法验证 |
| **B13 翻译批次** | `83a4fa0` | 17 文件（errorHandling 组 8 + form 组 3 等）；词数 3122/段落 179；锚点 3 处（exceptionHandler 批内闭环 + form/formCapable 消解） |
| **B14 翻译批次** | `9035228` | 13 文件（serverIO/uploads/transfers/filters 组 10）；词数 3410/段落 160；锚点 5 处；B13 组进度口径勘误（46/101 非 55/101） |
| **B15 翻译批次** | `91686ca` | 13 文件（byteBody 组 4/sessions/sse/websocket 组 3/http2/http3）；词数 3457/段落 168；锚点 2 处 |
| **B16 翻译批次** | `10c360d` | 24 文件（serverConfiguration 组 21 等）；词数 3265/段落 242；锚点 8 处（9 条豁免消解）；**回溯补注入 [[events]]**（B03 报告与实际不符的遗留缺陷）；httpServer 组 96/101 |
| **B17 翻译批次** | `d83478f` | 15 文件（httpServer 收尾 5 + httpClient 开头 10）；词数 2893/段落 167；锚点 5 处；restore 拦截译丢段（clientBasics）；**httpServer 章 101/101 全章译出（第六个全章）**；进度过半 |
| **B18 翻译批次** | `44b2cdf` | 8 文件（clientConfiguration/proxyClient/clientAnnotation 组 4）；词数 3303/段落 209；锚点 2 处；**reviewer 段落对齐第三次拦截真缺陷**（跨文件段错位）；上游 `////` 注释块纪律确立 |
| **B19 翻译批次** | 本次提交 | 14 文件（httpClient 注解余下 9 + certificates + contextPropagation 组 3 + cloud 章页）；词数 3471/段落 199；锚点 3 处 + 源内显式锚 certificates 保留；restore 第 4 次拦截译丢段；⑦ ×6 与 ③ ×1 修正；**httpClient 章 26/26 全章译出（第七个全章）** |

## 状态快照（2026-11-21，B19 收尾）

- 分支 main；基线 v5.2.25（`0b46d27afdfa`，快照日期 2026-11-20）；全部批次冻结窗口遵守（未跑 --apply）
- manifest：388 条目 = 156 missing + 2 skipped + **230 current**（进度 59.3%）
- 看板：B01–B19 = current，其余 13 批 pending
- anchor-registry：121 条（不变）；validate 全量跑：PASSED（230 文件，⑤ 豁免警告 18 条，M3 清零）
- 页头溯源投影：页名=toc 英文原题、URL=`https://docs.micronaut.io/5.2.x/core/#core-<basename>`、基线锁定日期 2026-11-19、translated_at=2026-11-21
- reports/progress.md 已重新生成（**七个全章**：introduction 2/2、quickStart 9/9、IoC 55/55、config 15/15、aop 10/10、httpServer 101/101、httpClient 26/26；contextPropagation 2/2；cloud 1/17）
- **会话累计**：本会话完成 B07–B19 十三批共 133 文件，进度 73→230（+157 文件，18.8%→59.3%）

## 实测结论（累计，下一会话必读）

1. **锚点注入规则（B02 精化）**：basename 约定锚点 = 官方站 `core-<basename>` = 片段首内容之前的块锚；页内标题锚按 PLAN §5.6 原位注入于标题行之前（B11 首实践）；源内已有显式锚（ANCLINE 占位符）逐字节保留。B07–B19 共 47 处注入 + 2 处源内锚保留。
2. **词数口径**：以批次执行时 inventory.py 口径实测为准（B07 2540/2484、B08 3400/3336、B09 2852/2835、B10 3022/3002、B11 3270/3240、B12 3363/3336、B13 3122/3076、B14 3410/3402、B15 3457/3416、B16 3265/3193、B17 2893/2870、B18 3303/3282、B19 3471/3424，格式 总词/非代码），M1 报告值仅作切分参考。
3. **批间前向引用消解**：先行文件对未译目标的 xref 记为 ⑤ 豁免，目标落盘后自动消解；每次批次报告必须核对豁免增减明细（最新 22→18）。
4. **门禁拦截真缺陷记录**：restore 译丢段 4 次（B10 锚点、B12 锚点、B17 callout、B19 snippet 占位符）+ validate ⑤ 锚点缺失 2 次（B10/B12）+ reviewer 段落对齐 3 次（B10 retry、B18 跨文件段错位等）+ 回溯补注入 1 次（B16 补 B03 的 [[events]]）——四道门禁（restore/validate ⑤/reviewer/validate 全量）层层兜底有效。
5. **reviewer 模板**：/tmp/b19_reviewer.py 为当前模板（临时不入库；复用 `vt.check_terms` 与 validate ③ 同源；含 NEED_ANCHOR 与 SOURCE_EXPLICIT_ANCHOR 检查）。**临时脚本一律用 Write 工具创建并先 py_compile 再运行**。
6. **validate ⑦ 邻接规则（累计 9 次踩坑）**：占位符/行内码/加粗标记后紧跟全角开括号必拒——占位符后接 `（` 一律预留空格必须作为翻译期硬习惯；宏 `[]` 后接全角开括号不在机检范围。
7. **③ 必译术语误触三类修法**：宏路径命中→补首现括注；指令行未 strip 命中小写 API 名→正文普通词物化；正文物化术语（如 classpath→类路径、Netty）需以正确译法过门禁，不绕过机检。
8. **上游 `////` 注释块**：按纪律逐字节保留（含块内占位符）；停用词启发会误报漏译（B18 3 条已文档化）；不要全局剥块（源/译分段会不同步）。
9. **大批次工作法（B12–B19 验证）**：先全量 protect（核对占位符总数）→ 逐文件写译文 → 批量 restore → 批量 assemble → 逐文件 validate → reviewer → mark-current。
10. **读 progress.md 必须核对列位**（B13 曾误读 missing 列为 current）。「报告声称的锚点注入」须与 zh 实际核对（B16 教训）。相邻章节接续语段落须核对归属文件（B18 教训）。

## 待办（下一会话）

1. **M2 继续**：B20 起（21 文件：cloud/cloudConfiguration 组 9 + serviceDiscovery 组 6 + clientSideLoadBalancing + distributedTracing + serverlessFunctions 组 4，双指标达标），看板改 in-progress 后按 §5.1 SOP + 固化校验链执行；启动提示词见 `docs/新会话启动提示词.md`（已更新至 B20 起）。注意：B20 落盘 cloudConfiguration/serviceDiscovery/serverlessFunctions 后预计消解 7 条豁免（bootstrap→distributedConfiguration、environments→cloudConfiguration、propertySource→distributedConfigurationVault、clientAnnotation→serviceDiscovery ×2、clientConfiguration→serviceDiscovery{Manual} ×2、eagerInit→serverlessFunctions）；distributedConfigurationConsul 落盘消解 clientAnnotation 第 3 条。
2. 术语滚动：B05–B19 括注待复核（构造型 stereotype、可保留 retainable、别名 alias、属性源 property source、mixin、规范构造器 canonical constructor、类型使用注解 type-use annotation、可空性注解、banner、kebab case、驼峰式 camel-case、提供者 provider、默认环境 default environment、求值表达式 evaluated expressions、小驼峰式 lower camel case、通知 advice、切面 aspect、环绕通知/引入通知、存根值 stubbed value、校验通知 validation advice、缓存拦截器 CacheInterceptor、weigher 权重计算器、断路器 Circuit Breaker、规约 specification、展开操作符 exploded operator、编解码器 codec、事件循环 Event Loop、数据类 Data Classes、校验组 validation groups、局部/全局错误处理器、异常处理器 exception handler、背压 backpressure、流式上传/完成上传、部件 part、管道断裂 broken pipe、主操作 primary operation、拆分/认领 split/claim、服务器发送事件 SSE、原生传输 native transports、事件循环载体 event loop carrier、跨源资源共享 CORS、证书提供者、密钥库 key store、ACME、服务器端视图渲染、访问日志记录器、主机名验证、中间人攻击、连接池 connection pool、应用层协议协商 ALPN、声明式客户端 declarative client、绑定器 binder、传播上下文 Propagated Context）；**context propagation 已随 B19 全章译出，括注「传播上下文」待复核转正**
3. M3+：断链豁免清零（当前 18 条）、抽检（含锚点注入报告与实际一致性专项）、sync drill、tag v1.0

## 调试经验与坑位（累计）

1. 长输出损坏处置：立即读回文件 → 修损坏行 → pytest 全绿 → 再提交（M1 经验）
2. gh api commits?path= 须用全仓路径 `src/main/docs/<rel>`
3. 网络直连 github.com 失败 → git/curl 走 `http://192.168.33.1:10808`；gh api 直连可用；11MB 级大页 curl 直连会超时截断，必须代理 + 后台跑
4. validate ⑤ 段落对照机检：zh 侧剔除页头溯源段（引用行+注释行合并为一段，恒 +1 偏差）
5. PreToolUse hook 拒绝 Bash 直写文件（heredoc/append/sed -i）→ 一律 Write/Edit 提交（含 /tmp 临时脚本）
6. zh 译文页头 `> ` 引用行与 `<!-- -->` 注释行不参与 ⑦/③ 校验，溯源字段以 ⑥/manifest 对账为准
7. translator 必须使用受保护文本中的真实占位符哈希——占位符以 `-protected.txt` 为准逐个复制
8. restore 输出 JSON 无 ok 字段（成功时含 `restored` 键）
9. validate_translation.py `--file` 为单参数，多文件逐个跑；不同 cwd 下注意路径

## 硬性纪律清单（继承）

1. `docs/翻译计划.md` 为唯一权威规范；改架构走 decision_log（DR-004 起递增）
2. 所有脚本 memgate 包裹；`source/` 只读；`manifest.yml` 禁人工直改（--mark-current 除外）
3. 门禁硬性化，禁止 `|| true`
4. 每批次 squash commit + 批次报告；决策类提交末行 `Decision: DR-编号`
5. agent 并发上限 = 串行 1；上下文过半立即交接
