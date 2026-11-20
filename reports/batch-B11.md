# 批次报告 B11

> 完成日期：2026-11-21 ｜ 执行：M2 第十一批次（串行 1，单会话编排方亲跑）

## 范围与规模

| 指标 | 值 |
|---|---|
| 文件数 | 7（AOP 收尾 2：scheduling + springAop + httpServer 章页与前 4 节：runningServer/runningSpecificPort/routing/binding） |
| 总词数（当前 protect 后口径，实测） | 3270（M1 inventory 报告值 3352，口径见 reports/batch-B02.md） |
| 非代码词（当前口径，实测） | 3240（M1 inventory 报告值 3350） |
| 段落数 | 206（manifest paragraphs 合计：39+13+11+46+83+6+8） |
| 上游基线 | v5.2.25（tag，2026-11-17 发布；快照 `0b46d27afdfa`） |
| 最终状态 | 7 文件全部 current（manifest 388 条目中 101/388，进度 26.0%） |

双指标达标：非代码词 3240 ≤ 3500 且总词 3270 ≤ 5500。

## 流程执行（PLAN §5.1 SOP + 固化校验链）

1. protect：7 文件（占位符合计 223：28+8+12+12+5+98+60）；
2. 翻译：占位符逐个从 `-protected.txt`/映射表复制；`dependency:`/`dependency::` 宏 4 处与
   上游 `//TODO:` 注释逐字节保留；routing 2 张表格（URI 模板匹配/HTTP 路由注解）与
   binding 2 张表格（参数绑定注解/可绑定类型）仅译单元格文本；
   `[.lang-…]`+`--` 开放块、`{blank}` 列表项（ATTRREF 占位符）结构保持；
   页内 xref `<<_uri_path_variables,URI 路径变量>>` 按 PLAN §5.6 在「== URI 路径变量」标题处
   原位注入 `[[_uri_path_variables]]`；
   `<<cors, CORS>>`/`<<moduleScripts,模块脚本>>`/`<<hibernateSupport,Hibernate 支持>>`
   目标逐字节保留、label 译出；
3. restore：7/7 哈希完整性全过（0 残留，restored 数与输入数核对一致）；
4. 溯源投影：`assemble_zh.py` 注入（translated_at=2026-11-21）；
5. reviewer 五项：段落对译 7/7 PASS（routing 62/62 段、binding 36/36 段等）；
   脚本新增页内标题锚位置检查（INNER_HEADING_ANCHOR）；
6. validate：6/7 首轮全绿 + httpServer ③ 必译术语缺失（netty→Netty：`dependency:…-netty[]`
   指令行未被 strip 使 src 侧命中小写 netty，而 zh 侧 "Netty" 在链接 label 内被 RE_URL 连带剥除）——
   正文改写为普通词提及 Netty 后通过；全量 101 文件 PASSED；
   ⑤ 豁免警告 24 条（23 → 24：creatingClient→httpServer、creatingServer→runningSpecificPort
   消解 −2；routing→cors、routing→moduleScripts、springAop→hibernateSupport 新增 +3）；
7. `--mark-current` 7/7 核销（hash+commit 双字段对账通过）；pytest 95 绿。

## 锚点注入（PLAN §5.6，B02 精化规则 + §5.6 原位注入）

- `guide/httpServer.adoc` → `[[httpServer]]`（被 creatingClient 引用，已译——落盘后豁免消解，批间闭环）
- `guide/httpServer/runningSpecificPort.adoc` → `[[runningSpecificPort]]`（被 creatingServer 引用，
  已译——落盘后豁免消解，批间闭环）
- `guide/httpServer/routing.adoc` → `[[routing]]`（被 clientParameters 引用，未译豁免承接）
- `guide/httpServer/binding.adoc` → `[[binding]]`（被 httpServerArch/localErrorHandling 引用，均未译豁免承接）
- `guide/httpServer/routing.adoc` 页内标题锚 `[[_uri_path_variables]]` 注入于「URI 路径变量」标题前
  （页内 xref 引用，registry 未登记——PLAN §5.6 原位注入首次实践）
- scheduling.adoc、springAop.adoc、runningServer.adoc 未被登记引用，无注入。

## 术语滚动

- 本批无新增 glossary 条目；新首现括注（按首现处理，频次待后续复核）：规约（specification，
  runningServer Spock 语境）、展开操作符（exploded operator，binding）；
- 既有术语命中：Netty（httpServer 正文物化命中 glossary 拼写规则）、拦截器、响应式、
  编译期（compile-time）、bean/工厂/内省（@Introspected 语境「内省」）、依赖注入（springAop）；
- banned 黑名单 0 命中（validate ③ 全量扫描）。

## 里程碑

**AOP 章（guide/aop，10 文件）全部 current——AOP 全章译出**（含章页 aop.adoc，B09 起步 3 → 8 → 10）。
httpServer 章起步：15 文件中 current 5（章页 + runningServer/runningSpecificPort/routing/binding）。
已全章译出：introduction、quickStart、IoC（55）、config（15）、AOP（10）。
整库进度 101/388（26.0%）。

## 遗留与后续

- 24 条 ⑤ 豁免警告登记于 validate 输出，M3 全量断链清零时一并处理；
- 本批次未触发 sync --apply（冻结窗口遵守）；`source/` 无写入；
- routing.adoc（83 段、98 占位符、2 张表、4 组开放块）为 httpServer 章最长文件，
  对译检查通过后确认无返工；页内标题锚机制自本批起进入常规流程。
