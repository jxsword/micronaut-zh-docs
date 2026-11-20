# 批次报告 B18

> 完成日期：2026-11-21 ｜ 执行：M2 第十八批次（串行 1，单会话编排方亲跑）

## 范围与规模

| 指标 | 值 |
|---|---|
| 文件数 | 8（httpClient：clientConfiguration/lowLevelClientError/bindErrors/proxyClient/clientAnnotation 组 4） |
| 总词数（当前 protect 后口径，实测） | 3303（M1 inventory 报告值 3379，口径见 reports/batch-B02.md） |
| 非代码词（当前口径，实测） | 3282（M1 inventory 报告值 3379） |
| 段落数 | 209（manifest paragraphs 合计） |
| 上游基线 | v5.2.25（tag，2026-11-17 发布；快照 `0b46d27afdfa`） |
| 最终状态 | 8 文件全部 current（manifest 388 条目中 216/388，进度 55.7%） |

双指标达标：非代码词 3282 ≤ 3500 且总词 3303 ≤ 5500。

## 流程执行（PLAN §5.1 SOP + 固化校验链）

1. protect：8 文件（占位符合计 192）；
2. 翻译：占位符逐个从 `-protected.txt`/映射表复制；clientParameters 的上游 `////` 注释块
   （含上游内部吐槽与 JIRA 链接）按纪律逐字节保留（含块内 ADMON 占位符）；
   clientParameters 3 张表（参数绑定注解/查询值格式化/基于类型的绑定）仅译文字单元格；
   `<<introductionAdvice,引入通知>>`（B09 已译）、`<<routing,路径变量>>`（B11 已译）、
   `<<filters,HTTP 服务器过滤器>>`（B14 已译）、`<<configurationProperties,配置属性>>`（B08 已译）、
   `<<serviceDiscoveryManual,服务发现>>`/`<<serviceDiscovery,服务发现>>` 目标逐字节保留 label 译出；
3. restore：8/8 哈希完整性全过（0 残留，restored 数与输入数核对一致）；
4. 溯源投影：`assemble_zh.py` 注入（translated_at=2026-11-21）；
5. reviewer 五项：段落对译首轮 5/8——proxyClient 多出 1 段、clientAnnotation 缺 1 段
   （「既然您已经了解了低层 HTTP 客户端…」一段误置于 proxyClient 尾部，实为 clientAnnotation 首段），
   互相归位后两文件 5/5 与 23/23 全对齐；clientParameters 45/45 对齐但停用词启发命中 3 条
   ——全部位于上游 `////` 注释块内（按纪律逐字节保留、validate ①-⑦ 全绿确认无真实漏译），
   文档化为已知启发式误报（reviewer 尝试全局剥注释块会导致源/译邻接结构不同步，已回退）；
6. validate：逐个 `--file` 首轮 7/8 全绿 + proxyClient ⑦ 邻接 ×1（占位符后漏空格）修正后 8/8 全绿；
   全量 216 文件 PASSED；⑤ 豁免警告 22 条（21 → 22：jdkHttpClient→proxyClient/proxy、
   apiVersioning→clientAnnotation、creatingClient→clientAnnotation 共 −4 消解；
   clientAnnotation→serviceDiscovery ×2、clientConfiguration→serviceDiscovery{Manual} ×2 新增 +5；
   净 +1 含次数口径差）；
7. `--mark-current` 8/8 核销（hash+commit 双字段对账通过）；pytest 95 绿。

## 锚点注入（PLAN §5.6，B02 精化规则）

- `guide/httpClient/clientAnnotation.adoc` → `[[clientAnnotation]]`（被 apiVersioning/creatingClient
  引用，已译——落盘后 2 条豁免消解，批间闭环；distributedConfigurationConsul 未译豁免承接）
- `guide/httpClient/proxyClient.adoc` → `[[proxyClient]]`（被 jdkHttpClient 引用，已译——
  落盘后豁免消解，批间闭环）
- 其余 6 文件未被登记引用，无注入。

## 术语滚动

- 本批无新增 glossary 条目；新首现括注（按首现处理，频次待后续复核）：引入通知复现、
  连接池（connection pool）、应用层协议协商（ALPN）、声明式客户端（declarative client）、
  绑定器（binder）、套接字激活未涉及；
- 既有术语命中：拦截器（CRUD 拦截器复现）、bean（小写保留）、配置属性（<<configurationProperties,…>>）、
  内省（@Introspected 语境）、校验（jakarta.validation）；banned 黑名单 0 命中（validate ③ 全量扫描）。

## 里程碑

httpClient 组（guide/httpClient/，26 文件）current 17/26（65%）。
整库进度 216/388（55.7%）。已全章译出：introduction、quickStart、IoC（55）、config（15）、
AOP（10）、httpServer（101）六个章。

## 遗留与后续

- 22 条 ⑤ 豁免警告登记于 validate 输出，M3 全量断链清零时一并处理；
- 本批次未触发 sync --apply（冻结窗口遵守）；`source/` 无写入；
- **reviewer 段落对齐第三次拦截真缺陷**：proxyClient/clientAnnotation 相邻段落误置（跨文件段错位），
  由「段数不一致 + 型别错位」信号定位；对含相邻章节接续语的文件（"Now that you have…"）
  写译文时须核对段落归属；
- **上游 `////` 注释块启发式误报为已知项**：块内英文按纪律逐字节保留，reviewer 停用词启发会命中；
  全局剥块会导致源/译邻接分段不同步（已实测回退），后续批次以人工核对 + validate 全绿为准。
