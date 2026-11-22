# 交接文档（handoff-latest）

> 更新：2026-11-23 ｜ 会话：M4.0 多模块基建 + micrometer/validation 试点（DR-006 落地）｜ 下一会话任务：**M4.1 P0 安全与观测——security 起步（2–3 会话）**（启动提示词见 `docs/新会话启动提示词.md`）

## 已完成清单（M4.0 会话，全部随收尾提交入库）

| 工作单元 | 说明 |
|---|---|
| 基建套件（4de82c6） | sync_upstream.py `--doc-root/--manifest` 参数化（manifests/<site>.yml ↔ modules/<site>/ 前缀一一对应，账本顶层 ref+locked_at，克隆缓存按仓库 slug 分目录）；validate `--manifest` + ⑤ 模块文档树前缀 + ③ 扫描集=通用+当前模块术语；assemble_zh 模块账本/toc/官方 URL（core 引用块格式 385 文件逐字节不变实测）；inventory `--manifest`+批次前缀（modules.json batch_prefix）；progress 多账本聚合按模块分组；render.mjs 聚合（modules.json 驱动逐模块单页 + landing.html 官方 18 组导航复刻 + 各页顶部模块切换条）；新增 check_all.sh；CI validate/sync workflows 模块化；pytest 100→123 绿 |
| 试点快照（6e33c11） | micrometer（30 文件，基线 c4d064ee3af4）+ validation（12 文件，基线 079f75dc6ba8），ref 5.2.x + locked_at 2026-11-23；无 0 字节壳、无图片；inventory 切批 MICRO-01(27 文件 3239 词)/MICRO-02(2 文件 327 词)/VALID-01(11 文件 1463 词) |
| MICRO-01（9fac35a） | 27 文件七步全流程；⑦ 行内码紧跟全角括号 41 处改写；② 门禁拦下 metricsAndReporters 误并内容（导读页实为标题+一段）；toc.yml 导航标题随批译出 |
| MICRO-02（bdc535c） | observation/repository；④ 标题保留 API 名加括注；模块 30 条目全 current |
| VALID-01（c9601ae） | 11 文件全模块；③ constraint→约束 module 作用域术语生效；④ 版本标题「…的破坏性变更」；模块 12 条目全 current |
| 渲染上线 | 聚合站 core+micrometer+validation+landing 0 失败；core 剔除模块条后与 DR-005 版逐字节一致、809 个 core- 锚点零差集；本地 http://127.0.0.1:8321 冒烟 4 页 200 |
| 图片体量实测（LFS 决策） | 试点两模块 0 图；gh api 抽样：security 8.9MB/34 图、oracle-cloud 4.5MB/28 图、aws 0.9MB/4 图、openapi/data ≤0.1MB（jackson-xml/sql/kotlin 等仓库 slug 或分支 404 未计入）——**外推 71 模块 <300MB，暂不启用 git-lfs**；security 快照落地时（P0）复测 |
| 看板模块维度 | translation-board.md 增「模块批次总览」节（MICRO-01/02、VALID-01 + LFS 结论 + M4.1 待办） |

## 状态快照（2026-11-23，M4.0 收尾）

- 分支 main，5 个新提交（4de82c6 基建 → 6e33c11 快照 → 9fac35a/bdc535c/c9601ae 三批次）；远程 https://github.com/jxsword/micronaut-zh-docs（push 走 SSH——坑位 14）
- core：388 条目 = 387 current + 1 skipped + 0 missing；validate 387 文件全绿；pytest 123 绿
- micrometer：30/30 current；validation：12/12 current；两模块 validate 全绿 0 警告
- 聚合站（DR-006）：index.html（core）+ micrometer.html + validation.html + landing.html；本地预览 http://127.0.0.1:8321（`cd build/site && setsid memgate 2048 python3 -m http.server 8321 & disown`）；在线 https://jxsword.github.io/micronaut-zh-docs/（deploy-pages.yml 自动部署）
- glossary：45 通用术语 + 6 banned + **modules.terms 3 条**（reporter→上报器、Observation 不译 [micrometer]；constraint→约束 [validation]）
- config/modules.json：官方导航 18 组实抓（2026-11-23），72 可译条目（core+71）+ gradle 外链；repo 字段仅 core/micrometer/validation 已填，其余开工时核实补填
- check_all.sh：core + 已快照模块逐模块 `--check`（退出码聚合：0 无变更/1 有变更/2 环境错误），产出 reports/check-all-<date>.md + check-all-latest.jsonl（CI 逐模块开 issue 用）

## 实测结论（M4.0 新增，继承 M3 结论 1–8 与 B01–B32 全部结论）

1. **dest 前缀约定**：`--manifest manifests/<site>.yml` ⇔ `source/modules/<site>/` ⇔ `zh/modules/<site>/` ⇔ 账本 file 字段 `modules/<site>/…` ⇔ 页 `<site>.html` ⇔ 锚 `<site>-<basename>`——全部由 manifest 文件名 stem 一一推导，无第二处配置。
2. **模块结构同构性**：micrometer/validation 与 core 完全同构（guide/toc.yml + 嵌套 dict + title 键），segment/protect/validate/assemble/inventory 零改动复用成立；但**源文件可能是纯导读页**（metricsAndReporters.adoc 仅标题+一段，21 个 reporter 各为独立页）——切批后先 cat 源文件确认边界，勿按文件名推测内容。
3. **模块图片可为零**：试点两模块无 resources/；渲染 imagesdir=modules/<site>/img/ 仅在存在图片时可见（copyImages 摊平 resources/img → site modules/<site>/img/）。
4. **per-file commit 采集**：模块账本也走 `--collect-commits`（gh api 42 条全成功，串行+缓存按 remote slug 命名）；assemble 在 per-file commit 缺失时回退账本 baseline（与 mark-current 期望一致，两级兜底）。
5. **⑦ 邻接规则高频违规模式**：reporter 表格「默认值：`X`（1 分钟）」模式——统一改写「…，即 1 分钟」；「`X`（或某个…」枚举括注——重排列举顺序让（ 跟随 CJK 词。模块批次初稿先用 grep `}}（` 自查可省一轮 validate。
6. **④ 标题未译规则的 API 名处理**：≥2 英文词的标题（Micrometer Observation）保留 API 名 + 中文括注「（观测）」通过；单英文词标题（Configuration）可直接译中文。
7. **check_all 退出码聚合**：脚本内部逐模块采集退出码不掩码，最终取最严重值（2>1>0）——`set -e` 不能用，采集模式与「禁止 || true」纪律兼容。

## 待办（下一会话：M4.1 P0 安全与观测）

1. **security 模块（2–3 会话，24 章 60+ 页最大头部模块）**：开工先 `gh api repos/micronaut-projects/micronaut-security --jq .default_branch` + 分支清单核实 5.2.x；`sync_upstream.py --repo https://github.com/micronaut-projects/micronaut-security --doc-root src/main/docs --manifest manifests/security.yml --ref 5.2.x --init`；inventory 切批 SEC-01…（batch_prefix 在 config/modules.json 补填 `{"security": {"batch_prefix": "SEC", "repo": "micronaut-projects/micronaut-security"}}`，repo 为 null 的模块开工时一律先核实补填）；按 §5.1 七步逐批推进。
2. **validation 剩余/micrometer 后续增量**：周 check_all 检出变更走 PLAN §5.1 修订批次（core 增量优先）。
3. **hibernate-validator + tracing + session**：同 security 流程；tracing 跨组引用（Analytics/Cloud）按首组去重口径。
4. **图片体量复测**：security 快照落地后 du -sh source/modules/security/resources，若单模块接近 9MB 且多模块累加逼近 300MB 再议 LFS（.gitattributes）。
5. **core 持续增量例行**：周 `bash scripts/check_all.sh`（扩后含模块）；有变更开 issue `[upstream-sync][<site>] <sha>` 并按 §5.1 增量复译。
6. 层间收尾 tag v1.1（P0 全部 100% 后）。
7. 5.3.x 基线切换、guides 二期、Maven/Platform 外链、configuration-reference（官方导航分组外新增，DR-006 计划外）：届时单独决策（DR-007 起）。

## 调试经验与坑位（M4.0 增补 19–22，继承 1–18）

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
