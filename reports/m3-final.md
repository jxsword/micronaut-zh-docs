# M3 全量收尾报告（2026-11-21）

> 依据：docs/翻译计划.md §8（M3 验收标准：演练八步全通；断链豁免清零；v1.0 打标）
> 前置状态：B32 完成——386 个 .adoc 全部处置（384 current + 2 skipped），388 manifest 条目中仅 2 个 toc.yml missing

## 结论一览

| 验收项 | 结果 |
|---|---|
| toc.yml / toc-python.yml 翻译专项 | ✅ 完成并核销（missing → current） |
| 全量 sweep 漏译检测 | ✅ 4048 段，真漏译 0 |
| 锚点注入一致性专项 | ✅ registry 123/123 实锚在位 |
| 抽检 ≥10% | ✅ 39/39 PASS（10.2%）+ 人工精读 4 文件 |
| sync 全链路 drill 八步 | ✅ 全通（门控拒绝 + 解除双向验证） |
| 断链豁免清零 | ✅ ⑤ 豁免 3 → 0 |
| README 在线结构 | ✅ 已补「在线对照结构」节 |
| tag v1.0 | ✅ 已打标，--apply 门控解除验证通过 |
| validate 全量 | ✅ 387 文件 PASSED，0 警告 0 失败 |
| pytest | ✅ 100 绿（95 → 100，+5 check_toc 测试） |

## 1. toc.yml / toc-python.yml 翻译专项

- 实测口径修正：handoff 记录的「76 条」为 M1 仅数 `title:` 行的口径；实测 toc.yml 385 条标题（76 条 title 行 + 309 条标量叶子），toc-python.yml 301 条（含 toc.yml 未收录的 `languageSupport.python.overloads` 页），两文件同键标题值一致。
- 译文来源：385 条标题由编排方直接翻译（源片段 .adoc 无 H1，页题只存在于 toc——这是上游构建特性），译名对齐 zh 语料既有用法（如 bean 小写保留、CLI 语境 feature 不译、locale→语言区域、Health 端点风格、Gradle/IDE 重载）与 xref label 惯用；API 名/产品名/HTTP 头名不译。
- 生成方式：行级变换（键/缩进/注释逐字节保留，仅替换标题值），页头加 YAML 注释版溯源投影（`# >` 引用行 + `<!-- upstream_file/commit/hash/translated_at -->`，满足 `--mark-current` 的 RE_PROVENANCE 且保持 YAML 合法）。
- 新增 `scripts/check_toc.py` 结构校验器（键树逐键对齐、标题已译或白名单、注释行保留、溯源三字段对账 manifest）+ `tests/test_check_toc.py` 5 项测试；白名单 31 条（IntelliJ IDEA、@Blocking、Cross-Origin-*-Policy、Micronaut for Java/Kotlin/…、Micronaut CLI、bean 等）。
- manifest 核销：`--mark-current guide/toc.yml` / `guide/toc-python.yml` 均 ok。
- overloads 页说明：`guide/languageSupport/python/overloads.adoc` 是上游 toc.yml 遗漏的页面（仅 toc-python.yml 收录），其 .adoc 已在 B32 译出，无缺口。

## 2. 全量 sweep（漏译检测）

- 口径对齐 spdlog `check_alignment.py`：段级译文与源文逐字节相同且英文停用词 ≥3 → 漏译；停用词 1–2 或实词 ≥3 → 告警人工复核。适配 .adoc：两侧 segment_adoc 分段，仅比对 TRANSLATABLE 段（代码块/指令行天然排除），zh 侧剥离溯源块，difflib 对齐。
- 结果：387 文件 / 4048 源段 → **errors 3，warns 93，真漏译 0**。
- errors 3 条全部位于 `clientParameters.adoc` 上游 `////` 注释块内（asciidoctorj issue 注记）——B18 已确立「注释块逐字节保留」纪律，属已知误报。
- warns 93 条逐条人工分诊：全部为合法不译内容——`dependency:`/`snippet::` 宏行（约 45 条）、文件路径 block title（8 条）、CLI 命令名标题（5 条，B29 既有裁决）、行内码/宏/link 列表段（约 30 条）、上游 `//TODO` 注释行（1 条）。

## 3. 锚点注入一致性专项

- 对 `config/anchor-registry.yml` 全部 123 条（121 + 本次新增 2）逐一 grep 对应 zh 文件：**123/123 实锚在位**（`[[<id>` 或 `[#<id>]`），同 id 多条目冲突 0。

## 4. 抽检 ≥10%

- 分层抽样（固定种子 20261121）：32 批每批 1 件 + 大批次加权（B12/B21 各 +2、B26/B28 各 +1）+ 固定 2 件特重文件（breaks 145 段、jacksonConfigurationBeans）→ **39 文件（10.2%）**。
- 五项机检（段数/型别一致、逐字节漏译、代码块逐字节、术语 ③ 同源、xref 多重集、溯源对账）+ 源内显式锚保留检查：**39/39 PASS**。
- 人工精读 4 文件逐段对照全部合格：`quickStart/ideSetup/ideaSetup.adoc`（B01）、`httpServer/producesAnnotation.adoc`（callout 对应）、`ioc/injection/methodInjection.adoc`（WARNING/块标题/构造器注入术语）、`languageSupport/python/pythonThreading.adoc`（GIL/上下文池/虚拟线程括注纪律）。

## 5. sync 全链路 drill（八步）

1. 前置盘点：git 清洁、manifest 388 条目状态复核 ✅
2. `--check` 全量：对照上游 5.2.x HEAD（`cca2a1ce83cd`，2026-11-21）→ 388 文件全部 NONE，0 变更，退出码 0 ✅
3. `--check --file guide/aop.adoc` 单文件增量判定 ✅
4. `--apply --dry-run` 预演：mode=apply、dry_run=true、未写盘 ✅
5. 门控验证（打 tag 前）：`--apply` 被拒——「初译期 --apply 门控禁用（PLAN §4.4）」错误信息正确 ✅
6. `--collect-commits`：already=388、collected=0、failed_deferred=0（缓存生效）✅
7. `--mark-current guide/i18n.adoc` 幂等复跑：状态保持 current、无额外 diff ✅
8. `--check` 复跑幂等（exit 0）+ 构建产物出树确认（`.upstream/` gitignored，仓库树无污染）✅

- 打标后补验：`--apply` 门控解除，0 变更下执行为 no-op（见 §7）。

## 6. 断链豁免 3 条收尾（⑤ 豁免 3 → 0）

| 豁免项 | 处置 |
|---|---|
| i18n.adoc（skipped 壳文件，errorFormatting 的 `<<i18n,本地化>>` 目标未译） | 创建 `zh/guide/i18n.adoc` 最小壳镜像（溯源投影块 + basename 锚 `[[i18n]]`；源文件 0 字节无可译正文），`--mark-current` 核销；manifest 现为 387 current + 1 skipped（appendix.adoc，无引用不处理） |
| 裸锚点 `_client_specific_configuration`（clientBasics → 目标为 clientConfiguration 的标题自动锚） | zh `clientConfiguration.adoc` 回溯补注入 `[[_client_specific_configuration]]`（`=== 客户端特定配置` 标题行之前，title 锚规则） |
| 裸锚点 `_uri_path_variables`（routing 自引） | B11 已注入 `[[_uri_path_variables]]`，无需再动 |

- 根因与根治：两条裸锚点在源扫描中不可解析（AsciiDoc 标题自动锚无显式定义）。`check_anchors.py` 增强**标题自动锚解析**为第三解析优先级（① 显式锚 → ② include 文件 basename 约定 → ③ 标题 auto-id：idprefix/idseparator 均为 `_`，Micronaut 构建实测口径，如 "URI Path Variables" → `_uri_path_variables`）。registry 重生成：anchors 121 → 123、unresolved 2 → 0，既有 121 条目零变化。
- 注：check_anchors 解析增强属实现层缺陷修复（对齐 PLAN §5.6「扫描全量 xref 目标锚点」本意），沿用 B01 缺陷修复先例，按轻量决策处理，未开 DR。

## 7. README 在线结构 + tag v1.0

- README 新增「在线对照结构」节（官方站 `#core-<basename>` 对照规则、构建期注入边界与官方站锚点提示、toc 导航已译与 check_toc 校验、官方站未渲染三章的说明）；基线锚定节更新 v1.0 状态；勘误工程结构表 toc 路径。
- **tag `v1.0`**：指向 M3 收尾提交（annotated）。tag 后 `--apply` 门控自动解除（`v1.0^{commit}` 可解析），已实测：0 变更下 `--apply` 为安全 no-op。此后进入持续增量模式（周检测 → issue → 段落级增量复译）。

## 8. 术语滚动复核（handoff 待办 3）

- 57 组候选术语全库一致性扫描（源文出现文件数 × zh 译名命中 × 异译候选）。
- 裁定要点：
  - **14 条转正**（写入 glossary，含 context 溯源）：advice→通知、property source→属性源、event loop→事件循环、service discovery→服务发现、declarative client→声明式客户端、health indicator→健康指示器、distributed tracing→分布式追踪、circuit breaker→断路器、validation group→校验组、exception handler→异常处理器、error handler→错误处理器、camel-case→驼峰式、nullability annotations→可空性注解、data classes→数据类。
  - **真缺陷 3 处修复**（advice 旧译/未译残留，均为 B01/B02 早期批次）：whatsNew xref label「重试建议」→「重试通知」；factories `<<aop, AOP advice>>` label → `<<aop, AOP 通知>>`；constructorInjection 正文「AOP advice」→「AOP 通知（advice）」。
  - **误报澄清**：规范/规约（Bean Validation 规范 vs PEP 协议规约，语境分工）、方面（普通行文）、编解码（编解码器子串）、绑定类（可绑定类型子串）、托管区（子串）、高水位（high-water mark 正确译法）、中间人攻击（已译，带括注分隔致扫描未命中）、native image（glossary 已有 GraalVM native image 条目，不重复转正以免 ③ 误触完整词组）。
  - **不转正**（回流风险大/低频括注已足）：provider（API 名误触面大）、codec、aspect、connection pool、kebab case、aware、naive、arity、write-through 等低频条目。
- 转正后全量 validate ③ 回流校验：387 文件 **0 失败**。

## 9. 遗留与移交

- 上下文进度报表/看板/交接文档已同步更新；下一会话进入「持续增量」阶段（PLAN §8）：周一 cron（远程托管后生效）→ `--check` 检出变更 → 开 issue → 48h 内按 5.1 SOP 增量复译。
- appendix.adoc（0 字节壳，无 xref 引用）维持 skipped，非债务。
- sweep/抽检脚本为 /tmp 临时件（m3_sweep.py、m3_sample.py、m3_termscan.py），口径已文档化于本报告，不入库。
