# 批次报告 B09

> 完成日期：2026-11-21 ｜ 执行：M2 第九批次（串行 1，单会话编排方亲跑）

## 范围与规模

| 指标 | 值 |
|---|---|
| 文件数 | 8（config 收尾 4：jmx/eachBean/bootstrap/immutableConfig + AOP 开头 4：aop/aroundAdvice/introductionAdvice/adapterAdvice） |
| 总词数（当前 protect 后口径，实测） | 2852（M1 inventory 报告值 2915，口径见 reports/batch-B02.md） |
| 非代码词（当前口径，实测） | 2835（M1 inventory 报告值 2915） |
| 段落数 | 125（manifest paragraphs 合计：2+7+11+40+6+29+19+11） |
| 上游基线 | v5.2.25（tag，2026-11-17 发布；快照 `0b46d27afdfa`） |
| 最终状态 | 8 文件全部 current（manifest 388 条目中 89/388，进度 22.9%） |

双指标达标：非代码词 2835 ≤ 3500 且总词 2852 ≤ 5500。

## 流程执行（PLAN §5.1 SOP + 固化校验链）

1. protect：8 文件（占位符合计 99：14+29+8+1+1+29+12+5）；
2. 翻译：占位符逐个从 `-protected.txt`/映射表复制；`dependency::micronaut-context[]` 与
   adapterAdvice 代码块内 `include::` ×2 逐字节保留；`<<refreshable,…>>` ×3、
   `<<configurationPropertiesAccessorsStyle,更改访问器风格>>`、`<<propertySource,属性源>>`、
   `<<factories,bean 工厂>>` 目标逐字节保留、label 译出（批间已译目标全部可达）；
   approved 术语 eager initialization→饿汉式初始化 在 aroundAdvice 命中按 glossary 处理；
   advice 按 B06 reflection 先例译「通知（advice）」（首现括注），Around/Introduction Advice 译
   环绕通知/引入通知；
3. restore：8/8 哈希完整性全过（0 残留，restored 数与输入数核对一致）；
4. 溯源投影：`assemble_zh.py` 注入（translated_at=2026-11-21）；
5. reviewer 五项：段落对译 8/8 PASS（immutableConfig 33/33 段、aroundAdvice 23/23 段等）。
   首轮术语检查 9 条全部为 reviewer 脚本误报（裸正则：别名 DI 子串命中「distributed」、
   宏路径 `api:aop.` 命中 AOP）——脚本改为直接复用 validate ③ 同源 check_terms（含 banned）
   后 8/8 PASS，后续批次沿用；
6. validate：8 文件 `--file` 全绿；全量 89 文件 PASSED；
   ⑤ 豁免警告 25 条（27 → 25：whatsNew→aop、annotationMetadata→aop、factories→aop
   因本批落盘消解 −3；bootstrap→distributedConfiguration 新增 +1）；
7. `--mark-current` 8/8 核销（hash+commit 双字段对账通过）；pytest 95 绿。

## 锚点注入（PLAN §5.6，B02 精化规则）

- `guide/aop.adoc` → `[[aop]]`（被 aopArch、whatsNew、annotationMetadata、factories、
  incrementalannotationgradle、openandaop 引用；前 3 个已译——本批落盘后 3 条豁免消解，
  批间 whatsNew/annotationMetadata/factories 引用闭环）
- `guide/aop/aroundAdvice.adoc` → `[[aroundAdvice]]`（被 aopArch 引用，未译豁免承接）
- `guide/aop/introductionAdvice.adoc` → `[[introductionAdvice]]`（被 clientAnnotation 引用，未译豁免承接）
- `guide/config/bootstrap.adoc` → `[[bootstrap]]`（被 cloud 章 5 文件引用，均未译豁免承接）
- `guide/config/jmx.adoc` → `[[jmx]]`（被 providedEndpoints 引用，未译豁免承接）
- eachBean.adoc、adapterAdvice.adoc、immutableConfig.adoc 未被登记引用（immutableConfig 仅作引用方），
  无注入。

## 术语滚动

- 本批无新增 glossary 条目；新首现括注（按首现处理，频次待后续复核）：
  通知（advice）、切面（aspect）、环绕通知（Around Advice）、引入通知（Introduction Advice）、
  存根值（stubbed value）、冻结（frozen）；
- 既有术语命中：饿汉式初始化（eagerly initialize 别名，aroundAdvice）、编译期（compile-time）、
  bean/工厂/配置属性/依赖注入（指令行外未出现）、拦截器（未出现）；
- banned 黑名单 0 命中（validate ③ 全量扫描）。

## 里程碑

**config 章（guide/config，15 文件）全部 current——config 全章译出**（B06 起 3 → 7 → 11 → 15）。
AOP 章（guide/aop，10 文件）3/10 起步（aroundAdvice/introductionAdvice/adapterAdvice）+ 章页 aop.adoc。
整库进度 89/388（22.9%）。IoC 章 55/55 保持全 current。

## 遗留与后续

- 25 条 ⑤ 豁免警告登记于 validate 输出，M3 全量断链清零时一并处理；
- 本批次未触发 sync --apply（冻结窗口遵守）；`source/` 无写入；
- immutableConfig.adoc（40 段、6 个 ==/== 级标题、WARNING 块）为本批最长文件，对译检查通过后确认无返工；
- reviewer 脚本自 B09 起术语检查与 validate ③ 同源（复用 check_terms），临时脚本位于 /tmp/b09_reviewer.py（不入库）。
