# 批次报告 B31

> 完成日期：2026-11-21 ｜ 执行：M2 第三十一批次（串行 1，单会话编排方亲跑；与 B21–B30 同会话接续）
> 提交说明：B31 与 B32 因 manifest.yml 为单一账本文件，合并为一次 squash commit（各自报告独立保留）。

## 范围与规模

| 指标 | 值 |
|---|---|
| 文件数 | 3（appendix：faq/usingsnapshots/problems） |
| 总词数（protect 后口径，实测） | 960（与 M1 inventory 报告值 960 一致） |
| 非代码词（当前口径，实测） | 955（与 M1 inventory 报告值 955 一致） |
| 段落数 | 44（inventory segments 口径，与既往批次 commit 口径一致） |
| 上游基线 | v5.2.25（tag，2026-11-17 发布；快照 `0b46d27afdfa`） |
| 最终状态 | 3 文件全部 current |

双指标达标：非代码词 955 ≤ 3500 且总词 960 ≤ 5500。占位符合计 31；源文件无显式锚。

## 流程执行（PLAN §5.1 SOP + 固化校验链）

1. protect：3 文件（31 占位符）；
2. 翻译：faq（八问：字节码/Spring/Scala/微服务之外/优势/Consul 与 Eureka/Groovy Singleton 混淆/启动慢）、
   usingsnapshots（SNAPSHOT 版本用法）、problems（三常见问题）；
   `<<serverlessFunctions,Serverless 计算>>`、`<<languageSupport,语言支持>>` 目标逐字节保留、label 译出；
   **锚点注入 0 处**（registry 实测：两处引用的锚点均已随 B20/B21 注入在位，落盘即闭环）；
3. restore：3/3 首轮全过；assemble 落 zh/ 3 文件（translated_at=2026-11-21）；
4. validate：逐个 `--file` faq 首轮 ⑦ ×1（占位符后紧跟全角开括号）修复后 3/3 全绿；
5. reviewer 五项：/tmp/b31_reviewer.py **3/3 PASS**（faq 26 段）；
6. `--mark-current` 3/3 核销；全量 382 文件 PASSED；pytest 95 绿。

## 里程碑与进度

- 整库进度 382/388；appendix 章 11/12（仅剩 breaks@B32）；
- ⑤ 豁免维持 6 条（0 新增 0 消解）；
- banned 黑名单 0 命中；术语零新增（既有复用命中）。

## 遗留与后续

- B32（breaks/overloads）为 M2 收官批次，见 reports/batch-B32.md；
- 本批次未触发 sync --apply（冻结窗口遵守）；`source/` 无写入。
