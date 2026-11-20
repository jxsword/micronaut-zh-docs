# 批次报告 B32

> 完成日期：2026-11-21 ｜ 执行：M2 第三十二批次——**M2 收官批次（串行 1，单会话编排方亲跑；与 B21–B31 同会话接续）**

## 范围与规模

| 指标 | 值 |
|---|---|
| 文件数 | 2（appendix/breaks + languageSupport/python/overloads） |
| 总词数（protect 后口径，实测） | 3181（M1 inventory 报告值 3183，口径基数差异以实测为准） |
| 非代码词（当前口径，实测） | 3177（M1 报告值 3180） |
| 段落数 | 181（inventory segments 口径，与既往批次 commit 口径一致） |
| 上游基线 | v5.2.25（tag，2026-11-17 发布；快照 `0b46d27afdfa`） |
| 最终状态 | 2 文件全部 current（manifest 388 条目 = **384 current + 2 skipped（appendix/i18n 纯 include 壳文件）+ 2 missing（toc.yml ×2）**；386 个 .adoc 全部处置完成） |

双指标达标：非代码词 3177 ≤ 3500 且总词 3181 ≤ 5500。占位符合计 156
（**breaks 129 个为全库单文件之最**，487 行/2908 词/166 段/145 译段）；源文件无显式锚（ANCLINE 0 处）。

## 流程执行（PLAN §5.1 SOP + 固化校验链）

1. protect：2 文件（156 占位符）；
2. 翻译：overloads（重载实现/可变参数/重载选择三节）、breaks（**全库最大文件**：
   5.2→5.0→4.0 三大版本破坏性变更清单——反射分发异常传播/HTTP 客户端授权头/头部值限制/
   配置资源快速失败/Jackson 3/Groovy 5/JSpecify/Bean 上下文/线程选择/Jackson 内省模块移除/
   模块化拆分/ConvertService/CORS/Retryable/Kotlin suspend 路由等 40+ 小节）；
   `<<duplicateConfigurationResources,…>>`、`<<serializationUsingJacksonDatabind,…>>` ×3、
   `<<graal,Graal>>`、`<<contextPropagation,传播上下文>>` 目标逐字节保留、label 译出；
3. restore：2/2 首轮全过；assemble 落 zh/ 2 文件（translated_at=2026-11-21）；
4. validate：逐个 `--file` breaks 首轮 ④ ×2（模块名标题「Micronaut Discovery Core」「Micronaut Retry」
   补译名括注「（服务发现核心模块）」「（重试模块）」——B25 ④ 先例）+ ⑦ ×4 修复后 2/2 全绿；
5. 锚点注入 1 处：`[[breaks]]` 为**标题锚**（title='A reflectively dispatched executable method
   propagates the method's exception'），注入「=== 反射分发的可执行方法会传播方法自身的异常」
   标题行之前；落盘后 grep 核对在位；
6. reviewer 五项：/tmp/b32_reviewer.py **2/2 PASS**（breaks 145 译段全对齐）；
7. `--mark-current` 2/2 核销；**全量 384 文件 PASSED**；pytest 95 绿。

## 里程碑：M2 全库 .adoc 处置完成

- **386 个 .adoc 全部处置完成：384 个译出 current + 2 个 skipped（appendix.adoc / i18n.adoc 纯 include 壳文件，无需翻译）**；
- **十七个全章**：introduction、quickStart、IoC、config、aop、httpServer、httpClient、cloud、
  serverlessFunctions、messaging、commandLineApps、configurations、logging、
  languageSupport/python、languageSupport/kotlin、management、cli；
- **⑤ 豁免 6→3 条**：breaks ×3 随落盘消解；**剩余 3 条均为 M3 项**——
  i18n.adoc（skipped 壳文件，M3 专项）+ 裸锚点 ×2（clientBasics `_client_specific_configuration`、
  routing `_uri_path_variables`，M3 跟踪）；
- **唯一遗留：guide/toc.yml 与 guide/toc-python.yml**（manifest status=missing，各 paragraphs=1）——
  PLAN §1.2 的 M1 实测项实测含 76 条英文导航标题，但 M1 批次切分未将其排入任何批次。
  **处置建议（待 M3 规划确认）**：M3 专项创建 zh/guide/toc.yml 镜像并翻译 title 值
  （标题译文可对照 zh/ 各文件页头引用块的英文原题与各章标题译名），并补充轻量结构校验；
  不影响本批 386 个 .adoc 的完成声明。

## 术语滚动

- 本批无新增 glossary 条目；
- 首现括注：热替换（hotswap，AOP 语境）、保留策略（retention policy）、
  受检异常（checked exceptions）复现、线路级（wire-level）复现；
- banned 黑名单 0 命中。

## 执行教训

- breaks 129 占位符翻译中零花括号缺陷（B20 回读习惯持续生效）；
- ④ 标题未译在新批次仍会出现（本批 ×2：模块名标题），④ 检查在每个含英文标题的新文件上都会触发。

## M3 待办（承接 handoff）

1. toc.yml/toc-python.yml 翻译专项（见上）；
2. 全量 sweep（漏译检测）+ 抽检 ≥10%（含锚点注入报告与实际一致性专项）；
3. sync 全链路演练（drill 八步）+ tag v1.0（初译期基线锁定解除开关）；
4. 断链豁免 3 条收尾：i18n.adoc 专项 + 裸锚点 ×2 处置；
5. 术语滚动复核清单见 handoff（B05–B32 累计括注）。
