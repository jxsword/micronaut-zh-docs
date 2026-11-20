# 批次报告 B29

> 完成日期：2026-11-21 ｜ 执行：M2 第二十九批次（串行 1，单会话编排方亲跑；与 B21–B28 同会话接续）

## 范围与规模

| 指标 | 值 |
|---|---|
| 文件数 | 14（cli 组 7 + i18n 组 2 + resources + appendix/architecture 组 4） |
| 总词数（protect 后口径，实测） | 3252（M1 inventory 报告值 3257，口径基数差异以实测为准） |
| 非代码词（当前口径，实测） | 3217（M1 报告值 3226） |
| 段落数 | 191（inventory segments 口径，与既往批次 commit 口径一致） |
| 上游基线 | v5.2.25（tag，2026-11-17 发布；快照 `0b46d27afdfa`） |
| 最终状态 | 14 文件全部 current（manifest 388 条目中 375/388，进度 97.0%，剔 skipped 口径） |

双指标达标：非代码词 3217 ≤ 3500 且总词 3252 ≤ 5500。占位符合计 141
（最多 commands 39）；annotationArch 664 非代码词/16 段为批次最重；源文件无显式锚（ANCLINE 0 处）。

## 流程执行（PLAN §5.1 SOP + 固化校验链）

1. protect：14 文件（141 占位符）；
2. 翻译：commands（CLI 命令大全 7 组表格）、reloading 组 5（自动重启/JRebel/Gradle/IDE 重载）、
   proxy、i18n 组 2（资源包/LocalizedMessageSource）、resources（资源加载器）、
   architecture 组 4（编译器/注解元数据/内省架构附录）；
   `<<gradleReload,Gradle 重载>>`、`<<ideReload,IDE 重载>>`、`<<localeResolution,…>>`、
   `<<introspection,Bean 内省>>`、`<<compilerArch,Micronaut 编译器>>` 目标逐字节保留、label 译出；
3. restore：14/14 首轮全过；assemble 落 zh/ 14 文件（translated_at=2026-11-21）；
4. validate：逐个 `--file` 9/14 首轮全绿，jrebel ⑦ ×3、gradleReload ⑦ ×1、
   compilerArch ⑦ ×4 + ③ visitor、annotationArch ⑦ ×1 + ③ visitor、introspectionArch ⑦ ×1 + ③ visitor
   （URL/XREF 宏直贴汉字 + TypeElementVisitor 宏路径触发 visitor 术语，补「（类型元素访问者）」括注）
   修复后 14/14 全绿；
5. 锚点注入 5 处（注入前核对 title 字段）：`[[compilerArch]]`/`[[annotationArch]]`/`[[proxy]]`/
   `[[gradleReload]]`（basename 锚；proxy 消解既有豁免 jdkHttpClient→proxy；compilerArch 被
   aopArch/containerArch/iocArch（B30）豁免承接）、`[[ideReload]]`（标题锚「=== IntelliJ」之前，
   批内闭环）；**annotationArch 首轮漏注入 basename 锚，锚点 grep 核对环节发现后补齐**（B16 教训复用）；
   落盘后 grep 核对 5/5 在位且位置正确；
6. reviewer 五项：/tmp/b29_reviewer.py 13/14 PASS——唯一 FAIL 为 annotationArch
   paragraph-3 的 xref 目标**顺序**差异（`<<compilerArch` 与 Element API link 在中文语序中对调，
   目标多重集一致、validate ⑤ 全绿）——按 B21 多重集口径判定为合法语序重排，非缺陷；
7. `--mark-current` 14/14 核销；全量 375 文件 PASSED；pytest 95 绿。

## 术语滚动

- 本批无新增 glossary 条目；visitor/装饰器/存根/构造型等 B21–B26 术语复用命中；
- 首现括注：持续构建（continuous builds）、类型元素访问者（TypeElementVisitor 括注 ×3）、
  语言中立 abstraction（compilerArch 保留原词）、资源包（resource bundle）；
- banned 黑名单 0 命中。

## 里程碑与进度

- 整库进度 375/388（97.0%，剔 2 skipped）；**cli 章 10/10 全章译出（第十七个全章）**；
- i18n 组 2/2；appendix 章 4/12（architecture 组 4/6，iocArch 等在 B30）；
- **⑤ 豁免 7→6 条（−1 消解 proxy +0 新增）**：剩余 i18n（M3 专项）+ breaks ×3（B32）+ 裸锚点 ×2（M3）
  ——B30 落盘后预计 0 新增（iocArch 等引用的 compilerArch/annotationArch/introspection 锚点均已在位）。

## 遗留与后续

- **B30（4 文件：appendix/architecture 的 iocArch/aopArch/containerArch/httpServerArch）预计锚点 0 处**
  （registry 实测：其引用的 compilerArch/annotationArch/introspection 等锚点均已随 B29/B03 注入在位，
  落盘即闭环）；B31（faq/usingsnapshots/problems 3 文件，problems→languageSupport 随 B21 锚点闭环）；
  B32（breaks + overloads 2 文件，breaks 落盘消解最后 3 条 breaks 豁免）——三批合计 9 文件后全库初译完成；
- reviewer xref 顺序检查对中文语序重排存在误报（目标多重集一致即合法），口径已文档化；
- 本批次未触发 sync --apply（冻结窗口遵守）；`source/` 无写入。
