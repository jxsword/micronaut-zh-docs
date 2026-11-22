# 批次报告：TRACING-01（tracing 全模块单批 24 文件+toc.yml）

- 模块：tracing（micronaut-projects/micronaut-tracing，**ref 8.4.x（默认分支）**，基线 `d38f08c067a9`，快照 2026-11-23 锁定；modules.json 本会话补填 repo/batch_prefix=TRACING）
  - 分支判定：micronaut-tracing 无 5.2.x 分支（自有版本线 6.x/7.x/8.x），按 SOP §4「缺失用默认分支」取 8.4.x；**8.3.x 与 8.4.x 的 docs 树经 blob sha 逐一比对完全一致**（最新 docs 提交同为 a798d48d，官方 /5.2.x/tracing/ 页徽标 v8.3.0），ref=8.4.x 与官方 5.2.x 内容无漂移
- 批次范围：TRACING-01 = 24 文件 + toc.yml（根层 8：breaks/introduction/jaeger/opentelemetry/releaseHistory/repository/tracingGuides/zipkin + opentelemetry/ 16），**非代码词 2878 / 总词 2929 / 段数 219**（inventory 实测）
- 流程：七步全流程（protect → 翻译 → restore → assemble → validate → mark-current；collect-commits 25/25 成功当日补采）；restore 24/24 首轮全过零拦截
- validate 结果：**25 文件全绿**；--mark-current 25/25 核销，模块 25/25 = 100%
- 门禁拦截与修复（首轮 3 错误全部真缺陷）：
  - logback ③ classpath→类路径（通用术语，B19 先例口径）
  - logback ③ instrumentation→插桩——触发源为 dependency: 宏 groupId="io.opentelemetry.instrumentation" 属性文本（dependency 行不被保护、落入 ③ 扫描集）；按语义补正：末段「MDC 集成」改述为「MDC 插桩集成」（mdc.adoc 原文即称 Logback MDC instrumentation，语义等价）
  - mdc ④ 标题「Logback MDC」未译——按实测结论 6 补中文括注「（映射诊断上下文）」；toc.yml 导航标题维持官方口径「Logback MDC」
- 锚点：批内裸 xref 1 处——ucp→`<<jdbc,JDBC>>`（批内闭环），按实测结论 8/13 口径在 jdbc.adoc 译文首行注入 `[[jdbc]]`；registry 为 core 扫描域无 tracing 条目，ucp ⑤ 走「裸锚点未登记，豁免（M3 跟踪）」警告分支（SEC-02 wwwAuthenticate 同型），渲染闭环由 [[jdbc]] 注入保证并经冒烟实测兜底
- 术语：glossary modules 新增 **tracing 6 条**（先写回再继续）：distributed tracing→分布式追踪、span→跨度（对齐 OpenTelemetry 中文社区口径；@WithSpan/SpanAttribute 类名语境不译）、exporter→导出器、propagator→传播器、instrumentation→插桩（OpenTelemetry Instrumentation 等产品/依赖名不译）、sampler→采样器；modules.terms 现 **24 条**（micrometer 2、validation 1、security 15、tracing 6——handoff 原记载「20 条/security 17」系过时口径，本会话实核修正，详见交接）
- 保留不译口径（与 core 一致）：api:/pkg:/ann: 宏逐字节保留；dependency: 宏行逐字节保留（annotations.adoc 的 dependency 行内嵌 ATTRREF 占位符原样还原）；include::（mdc.adoc 的 logback-mdc.xml，白名单外未入库）占位符原样保留；NOTE:/TIP: 提示词前缀保留英文（core 先例）；snippet::/codeblock/attribute 占位符原样
- 上游病句/笔误按语义等价处理：opentelemetry.adoc「The Default values that are defined inside the Micronaut which values might be different…」断裂句重写为「Micronaut 中定义的默认值如下（其中一些可能与 … 模块中的默认值不同）」；http.adoc「depedency」、grpc.adoc「GRPC→gRPC」、zipkin.adoc「ZipKin→Zipkin」笔误按正确形式译出
- 块标题（.Title）全部随文译出（使用 CLI/配置多个 Zipkin 服务器/过滤 HTTP 请求跨度等）；zipkin.adoc 两个同名块标题「.Configuring Multiple Zipkin Servers」系上游复制粘贴遗留，忠实保留同名译法
- 本批后模块状态：**tracing 25 条目全部 current = 100%（P0 层第 6 个完成模块）**

*批次收尾：squash commit（本文件 + zh/modules/tracing/ 整目录 + manifests/tracing.yml + glossary.yml + progress.md）*
