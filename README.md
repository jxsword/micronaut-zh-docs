# Micronaut 官方文档中文翻译（micronaut-zh-docs）

Micronaut Framework 官方主指南（[docs.micronaut.io/5.2.x](https://docs.micronaut.io/5.2.x/)，源码 `micronaut-projects/micronaut-core` 仓库 `src/main/docs/`）的社区非官方中文翻译：agent 分批翻译、git 管理、上游 blob-sha 账本驱动增量同步与增量翻译。

> **非官方声明**：本项目非 Micronaut 官方项目，与 Micronaut 团队（Object Computing / micronaut-projects）无隶属关系；译文可能有滞后，如有冲突以官方英文文档为准。译文问题欢迎提 issue。

## 翻译基线锚定

- upstream: micronaut-core@v5.2.25（5.2.x 分支），锁定于 2026-11-19
- 上游变更由每周 sync 检测（--check 对照 5.2.x 分支 HEAD）；初译期（v1.0 tag 前）仅开 issue 记录，`--apply` 门控禁用，避免批次目标漂移

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
| `source/` | 英文原文快照（只读，仅 sync 写入；含 `guide/`、`resources/` 图片、`toc.yml`） |
| `zh/` | 中文译文（与 source/ 同名 1:1 镜像，未译文件不存在于 zh/） |
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
