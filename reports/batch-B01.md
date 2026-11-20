# 批次报告 B01

> 完成日期：2026-11-20 ｜ 执行：M2 首批次（串行 1，单会话编排方亲跑）

## 范围与规模

| 指标 | 值 |
|---|---|
| 文件数 | 19（Introduction 3 + Quick Start 10 + IoC 前 6 节） |
| 总词数（protect 后口径） | 3355（与 inventory 实测完全一致） |
| 段落数 | 190（manifest paragraphs 合计） |
| 上游基线 | v5.2.25（tag，2026-11-17 发布；快照 `0b46d27afdfa`） |
| 最终状态 | 19 文件全部 current（manifest 388 条目中 19/388，进度 4.9%） |

## 流程执行（PLAN §5.1 SOP）

1. protect：19 文件全部生成受保护文本 + 映射表（`workdir/protect/`，gitignored）；
2. 翻译：占位符逐字节保留，`<<anchor,` 目标保留、label 译出；
3. restore：19 文件哈希完整性校验全过（无残留/无丢失）；
4. 溯源投影：`scripts/assemble_zh.py`（本批次新增）从 manifest 读
   upstream_commit/blob_sha 注入页头引用块 + HTML 注释四字段，杜绝手抄哈希；
   页名取 toc.yml 英文原题，官方站 URL 锚点取 `core-<basename>`（实测，见下）；
5. reviewer 五项：段落对照 19/19 一致且 0 漏译（逐段 zip + 停用词检测）；
   术语/banned、代码块/指令逐字节、xref 锚点、溯源四字段均由 validate 机检通过；
6. validate 七项全绿（28 条 ⑤ 豁免警告 = 未译目标文件，M3 清零跟踪）；
7. `--mark-current` 19/19 核销。

## 锚点注入（PLAN §5.6）

被引用标题按 anchor-registry 原位注入：

- `guide/introduction/upgrading.adoc` → `[[upgrading]]`（被 whatsNew.adoc 引用）
- `guide/quickStart/buildCLI.adoc` → `[[buildCLI]]`（文件无标题行，按块锚注入文件首；被 guide/cli.adoc 引用）
- `guide/quickStart/ideSetup.adoc` → `[[ideSetup]]`（同上块锚；被 guide/languageSupport/java/ide.adoc 与 quickStart.adoc 引用）

## 官方站锚点实测（核实日期 2026-11-20）

- `https://docs.micronaut.io/5.2.x/guide/index.html` 302 → `/5.2.x/core/`（保留 hash）；
- 单页 HTML（11.4MB，curl 代理实测）标题 id 形如 `core-<basename>`（`core-introduction`、`core-quickStart`、`core-upgrading`、`core-creatingServer`…），子标题 auto-id 为 `core-_xxx_yyy`（idprefix/idseparator 均为 `_`）；
- 因此 zh 页头「官方对应 URL」统一为 `https://docs.micronaut.io/5.2.x/core/#core-<basename>`。

## 上游怪癖（记录，不阻断）

`guide/httpServer.adoc`、`guide/httpClient.adoc`、`guide/certificates.adoc` 三章在上游源码与 toc.yml 中存在，但官方站 `/5.2.x/core/` 未渲染（站内无 `core-httpServer` 等锚点与导航项）。创建于 `creatingClient.adoc` 的 `<<httpServer,...>>`/`<<httpClient,...>>` 裸锚点在官方站本身为死链；译文按「目标不译」纪律原样保留，validate ⑤ 因目标文件在源中存在而正常通过。后续批次遇到这三章时，页头 URL 锚点将按 toc 键惯例生成并在批次报告注明站内不可达。

## M1 缺陷修复（本批次实测发现，均已补回归测试）

1. **check_anchors.py**：URL 过滤 `startswith(("http", "mailto"))` 把以 `http` 开头的裸锚点（`httpServer`/`httpClient`/`http3Server`/`httpServerFilter`/`https`）误当 URL 跳过 → 收紧为协议头匹配；anchor-registry 由 116 → 121 条（重新生成，自动产出物）。
2. **validate_translation.py ⑤**：裸锚点 `<<anchor,Label>>` 被当文件路径必然误报 → 与 check_anchors 同规则（含 `/ .` 判页级文件引用）经登记表全域解析；未登记裸锚点降为豁免警告（M3 跟踪）。
3. **validate_translation.py ⑤**：已译目标的锚点检查含 `anchor in reg_ids` 放行，而登记表恰是被引锚点集合 → 放行恒真、注入机检形同虚设 → 移除，改为必须存在 `[[id]]` / `[#id]` 字面注入。
4. **validate_translation.py ⑦ 禁繁体表**：混入简繁共用字（行/息/主/境/景/常，源自「執行緒/訊息/主題/環境/佈景/常駐」误拆）→ 简体正文大面积误报（42 错误中 41 个为该误报）→ 仅保留繁体独有字。
5. **segment_adoc.py**：`snippet::` 构建期代码注入宏未纳入指令行 → 补入 `RE_DIRECTIVE`，其行现受 validate ② 逐字节门禁保护（B01 含 8 行 snippet）。

测试 86 → 94 全绿（新增 6 项回归 + snippet 用例，合并为 8 处断言扩展）。

## 术语新增

无新术语（B01 全部命中既有 glossary；「限定符（qualifier）」「饿汉式初始化（eager initialization）」「上下文传播」等首现括注按风格指南处理，暂不入表，待后续批次复核频次后决定是否转正）。

## 轻量决策（不立 DR，记录于此）

- 页头引用块 `<页名>` 取 toc.yml **英文原题**（指向官方英文页面，避免与未来 toc.yml 中文标题批次产生两套译名）。
- 无标题行的 include 片段（buildCLI/ideSetup）的被引锚点以**块锚**形式注入文件首。
- 新增 `scripts/assemble_zh.py`：§5.4 溯源投影装配的机械化实现（非架构变更，仅为消除逐文件手抄哈希的差错面）。

## 遗留与后续

- 28 条 ⑤ 豁免警告登记于 validate 输出，M3 全量断链清零时一并处理；
- `zh/resources/` 图片镜像已按 §3 目录约定补齐（`source/resources/img` 13 张 → `zh/resources/img` 字节复制，`cmp` 抽验一致）；B01 三个 `image::` 宏引用的图片（intellij-annotation-processors.png、installing-tools-for-micronaut-vs-code.gif、netbeans-plugins-java-web-ee.png）均可达；本批次未触发 sync --apply。
