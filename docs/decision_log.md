# 决策记录（micronaut-zh-docs）

> 编号规则：取当前最大编号 + 1；被推翻时不改旧条目，新增条目并把旧条目改为 `[状态: 已替代 → DR-新编号]`。

## DR-001 2026-11-19 翻译范围：主指南一期、guides 二期分期立项  [状态: 生效]
- 背景: 官方无中文文档；docs.micronaut.io 主指南（386 adoc/约11万词，Apache-2.0）与 guides.micronaut.io（196 篇/约15.6万词，CC-BY-4.0）合计约26万词，许可证不同。
- 选项与权衡: A 两者并行（一步到位，但上下文/工期压力最大，弃用）; B 主指南+guides 分期（风险分期释放、许可证分开署名）✓; C 仅主指南（不覆盖 guides 站，弃用）
- 结论: 选 B——一期翻译主指南并锁定基线 tag v5.2.25（2026-11-17 发布，与在线 /5.2.x/core/ 一致）；guides 为二期，开工前另立决策。
- 理由: 分期使每个里程碑可验收；guides 每篇含 6 语言代码工程，同步复杂度高不宜同期启动。
- 影响: docs/翻译计划.md 第 1、8 节；二期开工时需新决策。
- 记录时间 / 会话: 2026-11-19 / micronaut-zh-docs 计划制定会话

## DR-002 2026-11-19 翻译载体：.adoc 原文直译  [状态: 生效]
- 背景: 上游文档为 Asciidoctor 格式，家族既有管线全是 markdown/rst/wiki，需决定翻译载体。
- 选项与权衡: A .adoc 原文直译（与上游逐字节 1:1，blob-sha 增量账本从 benchmark/spdlog 原样移植，保留官方构建兼容性）✓; B po4a gettext PO（msgmerge 增量最成熟，但 po4a 的 asciidoc backend 未验证、agent 操作 .po 体验差，弃用）; C 转 Markdown 再译（家族 mkdocs 管线现成，但有损转换丢 xref/属性/条件块语义，永远无法回灌官方构建管线，弃用）
- 结论: 选 A——`source/` 快照 + `zh/` 同名 1:1 镜像；agent 以占位符保护 asciidoc 指令后翻译。
- 理由: 增量机制是本工程硬需求，家族已验证的段落迁移工具链价值最大；.adoc 语法风险用保护+校验器闭环。
- 影响: docs/翻译计划.md 第 3–5 节；需新写 segment_adoc.py / protect_untranslatable.py（asciidoc 版）。
- 记录时间 / 会话: 2026-11-19 / micronaut-zh-docs 计划制定会话

## DR-003 2026-11-19 站点形态：暂不建站，M3 后再评估  [状态: 已替代 → DR-004]
- 背景: 官方站存在构建期特性（source:: 宏注入代码、配置属性表生成），只快照 .adoc 无法单独重建完整官方站点；家族 gtest 有「纯镜像不建站」先例。
- 选项与权衡: A 暂不建站、仓库内阅读（依赖最轻，专注翻译质量）✓; B asciidoctorj 轻渲染（出站快，但构建期特性只能降级为占位提示，弃用—M3 后可重评）; C 官方 Gradle 管线 overlay 构建（输出与官方站一致，但 JDK+Gradle+全仓构建重、本机内存风险高，弃用—M3 后可重评）
- 结论: 选 A——初译期纯译文仓库；译文页保留官方站锚点对照提示；M3 收尾时按 B→C 顺序重新评估建站。
- 理由: 翻译质量优先于阅读形态；建站工具链投入应发生在内容基本齐全之后。
- 影响: docs/翻译计划.md 第 2.3、5.2、8 节；CI 不含 deploy workflow。
- 记录时间 / 会话: 2026-11-19 / micronaut-zh-docs 计划制定会话

## DR-004 2026-11-21 站点形态：轻渲染多页静态站 + GitHub Pages 托管  [状态: 已替代 → DR-005]
- 背景: M3 收尾后用户提出本地/在线预览需求（DR-003 预留的重新评估点；用户明确指令建仓部署）；GitHub 对 .adoc 的 safe-mode 原生渲染无导航、定制宏残留、相对链接断裂，不满足阅读需求。
- 选项与权衡: A GitHub 原生 .adoc 渲染（零成本但宏原文/无导航/断链，仅评审视角，弃用）; B asciidoctor.js 适配层轻渲染多页静态站 + GitHub Pages ✓; C 官方 Gradle 管线全仓构建（忠实度最高，但需完整 micronaut-core 仓库与构建期代码注入，重且内存风险高，弃用）
- 结论: 选 B——scripts/preview/render.mjs 适配层（溯源块正规化 / javadoc 宏族去宏化 / 构建期注入段 TIP 官方站提示 / 裸锚经 anchor-registry 跨页改写 / xref 多页相对化 / imagesdir 深度注入），本地 http.server 与 GitHub Actions deploy-pages 共用同一脚本；本地 http://127.0.0.1:8321，在线 https://jxsword.github.io/micronaut-zh-docs/。
- 理由: 正文/结构/链接/图片全渲染（386 页 0 失败），构建期注入内容按 DR-003 既定口径降级为官方站对照提示，忠实度定位不变；轻依赖（asciidoctor.js + js-yaml）双端一致。
- 影响: scripts/preview/、.github/workflows/deploy-pages.yml、README 在线对照结构节；DR-003 状态改为已替代。
- 记录时间 / 会话: 2026-11-21 / M3 收尾后续会话（用户指令建仓部署）

## DR-005 2026-11-21 站点交互形态：单页合集复刻官方导航（替代 DR-004 多页形态）  [状态: 生效]
- 背景: 用户实测多页站后指出官方文档为单页（左侧导航页内跳转），多页站查看其他页面需返回索引页，操作不便；经抓取官方 11.4MB 单页核实其机制（toc 顺序拼接、页标题由构建插件插入、全局 core- 前缀锚、内容零偏移）。
- 选项与权衡: A asciidoctor 单 master 文档渲染（numbered/toc 原生，但 article/book 语义均无法表达「多个 h1 章带正文」，实测 99→30 条 level-0/part 错误，弃用）; B 多页站 + JS hash 路由侧栏（体验接近但 JS 依赖/维护面大/锚点与官方不互通，弃用）; C 逐片段 convert（standalone:false）+ HTML 拼接，伪层级 + postprocess 全局升位 ✓
- 结论: 选 C——按 toc.yml 顺序逐片段渲染拼接为单页 index.html；章 ==、页 ===（升位后 h1/h2）、片段内容 +1 偏移（内部 == → h3）；每片段插 [[core-<basename>]] 页锚与官方互通；页面树侧栏（toc.yml 展开编号 + scrollspy）注入；渲染后标题全局升位（h2→h1…）对齐官方层级。
- 理由: 与官方交互一致（单页 + 页内跳转 + 编号导航）；片段级渲染属性隔离、拼接后内部引用天然页内可达；实测 385 片段 0 失败、1.4MB、0.4s。已知差异：内容标题比官方深一级（官方零偏移系 Astro 构建拼接，asciidoctor 无法复现；导航与锚点不受影响）。
- 影响: scripts/preview/render.mjs 重写；README 在线阅读节；本地 http.server 预览入口不变。
- 记录时间 / 会话: 2026-11-21 / 同会话（用户确认 A1）

## DR-006 2026-11-21 全模块翻译：同仓库聚合架构 + P0→P5 分层计划  [状态: 生效]
- 背景: 用户决定翻译官方站 /5.2.x/ 聚合站下 core 之外的 ~71 个模块文档（分散于 micronaut-projects 各独立仓库 src/main/docs/，抽样均 Apache-2.0；估算 ~2600 页 / 30–40 万词 / ~250–300 批）；需决策仓库架构与优先级。
- 选项与权衡: A 每模块独立仓库（隔离彻底但基建 ×71 重复、术语 71 份副本漂移、71 个站点无法聚合导航，弃用）; B 混合（大模块独立仓+小模块聚合，两套模式并存、边界随词数漂移，弃用）; C 同仓库聚合（source/modules/<site>/ + 每模块独立 manifest，core 零迁移）✓
- 结论: 选 C——单仓聚合：术语/校验链/渲染/CI/看板全套复用，术语跨模块统一，单 Pages 站聚合导航对齐官方形态；优先级 P0 安全观测 → P1 数据消息 → P2 API → P3 云 → P4 语言测试 → P5 长尾，层间 tag v1.1–v1.6；批次编号 <模块>-<序号>（SEC-01…）；glossary 增 modules: 分节 + validate ③ 模块化扫描集；脚本参数化收敛为 sync/inventory/progress 三个。
- 理由: security 实测模块与 core 完全同构（guide/toc.yml + 壳文件），manifest 全路径字段使多数脚本零改动；锚前缀 <site>-<basename> 与官方各模块站互通（实测官方锚形态）。
- 影响: docs/翻译计划-模块扩展.md（独立计划）；PLAN v1.1 §1.3 加指针；scripts/preview/render.mjs 聚合；M4.0 基建 + micrometer/validation 试点先行。
- 记录时间 / 会话: 2026-11-21 / 同会话（三轮复审 15 项修正后定稿）
