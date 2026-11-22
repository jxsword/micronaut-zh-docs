# 批次报告：HV-01（hibernate-validator 全模块单批 4 文件+toc.yml）

- 模块：hibernate-validator（micronaut-projects/micronaut-hibernate-validator，ref 5.2.x，基线 `0ae7293d6bc9`，快照 2026-11-23 锁定；modules.json 本会话补填 repo=micronaut-projects/micronaut-hibernate-validator、batch_prefix=HV）
- 批次范围：HV-01 = 4 文件 + toc.yml（introduction/setup/repository/releaseHistory），**非代码词 76 / 总词 76 / 段数 9**（inventory 实测）
- 流程：七步全流程（protect → 翻译 → restore → assemble → validate → mark-current；collect-commits 5/5 成功当日补采）
- validate 结果：**5 文件全绿（含 toc.yml），零豁免警告**；--mark-current 5/5 核销，模块 5/5 = 100%
- 结构实测：
  - setup.adoc 全文件即 `dependency:` 宏指令行（占位符 0）——译文=原文逐字节保留（validate ② 指令行口径）
  - repository/releaseHistory 为 SEC-04 同款 URL+ATTRREF 复合占位符（`{{URL}}{{ATTRREF}}[{{URL}}{{ATTRREF}}]`）——显示文本与目标同构，多重集占位符原样保留，restore/①通过
  - introduction 的 URL 显示文本「Bean Validation」保留英文规范名不译——与 core 既译口径一致（zh/guide/ioc/beanValidation.adoc 页题、validationGroups.adoc 等多处先例；非 HV 专属专名，不收录 glossary）
- 锚点：批内 0 处 xref、registry 无本模块引用，锚点注入 0 处
- 术语：glossary 零改动（modules 分节维持 20 条；Hibernate Validator 为产品名整体不译）
- 本批后模块状态：**hibernate-validator 5 条目全部 current = 100%（P0 层第 5 个完成模块）**

*批次收尾：squash commit（本文件 + zh/modules/hibernate-validator/ 整目录 + manifests/hibernate-validator.yml + progress.md）*
