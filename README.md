# Micronaut 官方文档中文翻译（micronaut-zh-docs）

Micronaut Framework 官方主指南（[docs.micronaut.io/5.2.x](https://docs.micronaut.io/5.2.x/)，源码 `micronaut-projects/micronaut-core` 仓库 `src/main/docs/`）的社区非官方中文翻译：agent 分批翻译、git 管理、上游 blob-sha 账本驱动增量同步与增量翻译。

> **非官方声明**：本项目非 Micronaut 官方项目，与 Micronaut 团队（Object Computing / micronaut-projects）无隶属关系；译文可能有滞后，如有冲突以官方英文文档为准。译文问题欢迎提 issue。

## 翻译基线锚定

- upstream: micronaut-core@v5.2.25（5.2.x 分支），锁定于 2026-11-19；**初译完成于 2026-11-21（tag `v1.0`）**
- 远程仓库：[jxsword/micronaut-zh-docs](https://github.com/jxsword/micronaut-zh-docs)（main 直推，push 触发 validate CI 与 Pages 部署）
- 上游变更由每周 sync 检测（`--check` 对照 5.2.x 分支 HEAD）；v1.0 后 `--apply` 门控解除，进入持续增量模式：检测 → issue → 段落级增量复译（只重译变更段，保留已译段）

## 在线阅读

- **GitHub Pages 在线阅读**：<https://jxsword.github.io/micronaut-zh-docs/>（单页合集，左侧编号导航页内跳转，交互对齐官方文档站；push 到 main 自动部署）
- 本地预览：`npm ci --prefix scripts/preview && node scripts/preview/render.mjs` 后用任意静态服务器打开 `build/site/`（如 `python3 -m http.server 8321 --directory build/site`）
- 渲染形态（DR-005）：与官方站同构的单页合集——h1 章 / h2 页（toc 树全路径编号）、`core-<basename>` 页锚与官方锚互通、左侧页面树导航 + scrollspy；构建期注入的代码示例与配置属性表按官方站对照提示处理

## 在线对照结构

- 每个译文文件页头附溯源引用块，含官方站对应页链接：`https://docs.micronaut.io/5.2.x/core/#core-<页面 basename>`；引用块后的 HTML 注释记录上游文件/提交/blob 哈希与翻译日期（机读，`--mark-current` 校验对象）
- 上游主指南在构建期从 micronaut-core 各模块注入真实代码（`source::`/`source[]` 宏）并生成配置属性参考表，纯 .adoc 快照无法单独重建完整官方站点：译文页中代码段与属性表以官方站对应章节为准，相关页已附「官方站锚点提示」
- 导航目录 `guide/toc.yml` 与 `guide/toc-python.yml`（Python 文档变体）的 386 条页面标题已译（页面路径与文件名不译），键路径与上游逐一对齐，由 `scripts/check_toc.py` 结构校验
- 上游官网仅渲染主指南部分章节（httpServer/httpClient/certificates 三章未在官方站渲染），译文侧仍完整翻译

## 署名（TASL 四要素）

| 要素 | 内容 |
|---|---|
| Title | Micronaut Framework Documentation 中文翻译 |
| Author | Object Computing, Inc. and Micronaut contributors |
| Source | https://github.com/micronaut-projects/micronaut-core（`src/main/docs/`）｜ https://docs.micronaut.io/5.2.x/ |
| License | [Apache-2.0](LICENSE_TRANSLATION.md)（原文许可；译文以同许可发布） |

## 工程结构

| 路径 | 说明 |
|---|---|
| `source/` | 英文原文快照（只读，仅 sync 写入；含 `guide/` 全量 .adoc、`guide/toc*.yml` 导航、`resources/` 图片） |
| `zh/` | 中文译文（与 source/ 同名 1:1 镜像；纯 include 壳文件以最小镜像 + 锚点形式存在） |
| `manifest.yml` | 上游账本（唯一状态源，只允许脚本读写；blob sha + 四态状态机） |
| `scripts/` | 同步/分段/保护/校验/锚点/进度管线（见各脚本 docstring） |
| `config/` | 术语表（glossary.yml，含禁用译名黑名单）、风格指南、锚点登记表 |
| `reports/` | 同步报告、批次切分清单、进度报表（自动生成区） |
| `docs/` | 翻译计划（唯一权威规范）、decision_log、任务看板、交接文档 |
| `tests/` | pytest：同步五类 diff、分段器、保护器往返、校验器、锚点检查 |

## 进度与治理

- 批次看板：[docs/translation-board.md](docs/translation-board.md)
- 进度报表：[reports/progress.md](reports/progress.md)（脚本自动生成）
- 权威规范：[docs/翻译计划.md](docs/翻译计划.md)（v1.1，一切流程以它为准）

## 许可证

- 本仓库自身（脚本、配置、文档）：[MIT](LICENSE)（micronaut-zh-docs Contributors）
- 上游原文许可与署名：见 [LICENSE_TRANSLATION.md](LICENSE_TRANSLATION.md)
