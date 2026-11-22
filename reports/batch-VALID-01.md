# 批次报告：VALID-01（validation 全模块 11 文件）

- 模块：validation（micronaut-projects/micronaut-validation，ref 5.2.x（默认分支即 5.2.x），基线 `079f75dc6ba8`，快照 2026-11-23 锁定）
- 批次范围：VALID-01 = 11 文件（introduction / releaseHistory / quickStart / methodsValidation / dataClassesValidation / configurationValidation / additionalConstraints / builtInConstraints / compileTimeValidation / breaks / repository + toc.yml 导航标题），**非代码词 1463 / 总词 1479**（inventory 实测）
- 段数：106（账本 paragraphs 合计）
- 流程：同七步；per-file commit --collect-commits 采集 12 条 → validate --manifest 全绿 → --mark-current 逐文件核销
- validate 结果：12 文件全绿 0 警告
- 实译发现与处置：
  - ③ 必译术语：constraint → 约束（module 作用域术语，breaks.adoc 的 api: 宏路径含小写 constraints 触发扫描，译文补「约束校验器」括注）；classpath→类路径、data classes→数据类、meta-annotation→元注解、decorator→装饰器、reactive→响应式等通用术语随 ③ 通过
  - ④ 标题「Micronaut Validation 5.0.0」→「…的破坏性变更」；xref 目标 core guide（Micronaut User Guide）保持官方站绝对链接原样（DR-006 §9 已知差异）
  - 邻接规则零违规（初稿即避开行内码+全角括号模式）
- 术语写回（glossary modules: 分节）：constraint→约束（aliases constraints）
- 上游同构性实测：validation 无 0 字节壳、无图片；toc 结构与 core 同构，inventory/validate/render 全链路零改动复用 ✓

*批次收尾：squash commit（本文件 + zh/modules/validation/** + manifests/validation.yml + glossary）*
