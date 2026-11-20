# 批次报告 B17

> 完成日期：2026-11-21 ｜ 执行：M2 第十七批次（串行 1，单会话编排方亲跑）

## 范围与规模

| 指标 | 值 |
|---|---|
| 文件数 | 15（httpServer 收尾 5：accessLogger/secondaryServers/views/openapi/graphql + httpClient 章开头 10） |
| 总词数（当前 protect 后口径，实测） | 2893（M1 inventory 报告值 3008，口径见 reports/batch-B02.md） |
| 非代码词（当前口径，实测） | 2870（M1 inventory 报告值 3004） |
| 段落数 | 167（manifest paragraphs 合计） |
| 上游基线 | v5.2.25（tag，2026-11-17 发布；快照 `0b46d27afdfa`） |
| 最终状态 | 15 文件全部 current（manifest 388 条目中 208/388，进度 53.6%） |

双指标达标：非代码词 2870 ≤ 3500 且总词 2893 ≤ 5500。

## 流程执行（PLAN §5.1 SOP + 固化校验链）

1. protect：15 文件（占位符合计 137）；
2. 翻译：占位符逐个从 `-protected.txt`/映射表复制；accessLogger 访问日志标记列表
   （ATTRREF 占位符 `%{…}i` 形态）与 httpd 格式说明逐条译出；
   clientPostRequests 的 HttpRequest 工厂方法表 7 行仅译说明列；
   `<<replaces,bean 替换>>`（B03 已译）、`<<serviceDiscovery,服务发现>>`、
   `<<proxyClient,代理请求>>`/`<<proxy,HTTP 代理>>`、`<<_client_specific_configuration,客户端特定配置>>`
   目标逐字节保留 label 译出；
3. restore：首轮 clientBasics 门禁拦截（**译丢 1 段 callout**：`Argument.of`/`Map` 占位符缺失）——
   restore 译丢段门禁按设计拦截，补齐后 15/15 哈希完整性全过（0 残留，restored 数与输入数核对一致）；
4. 溯源投影：`assemble_zh.py` 注入（translated_at=2026-11-21）；
5. reviewer 五项：段落对译 15/15 PASS（clientBasics 44/44 段为组长）；
6. validate：逐个 `--file` 首轮 14/15 全绿 + clientPostRequests ⑦ 邻接 ×1（占位符后漏空格）修正后
   15/15 全绿；全量 208 文件 PASSED；⑤ 豁免警告 21 条（24 → 21：formData→httpClient、
   creatingClient→httpClient ×2、creatingClient→lowLevelHttpClient、introduction→nettyHttpClient、
   introduction→jdkHttpClient 共 −6 消解；jdkHttpClient→proxyClient、jdkHttpClient→proxy、
   clientBasics→serviceDiscovery 新增 +3）；
7. `--mark-current` 15/15 核销（hash+commit 双字段对账通过）；pytest 95 绿。

## 锚点注入（PLAN §5.6，B02 精化规则）

- `guide/httpClient.adoc` → `[[httpClient]]`（被 formData/creatingClient ×2/secondaryServers 引用，
  已译——落盘后 3 条豁免消解 + secondaryServers 批内闭环）
- `guide/httpClient/httpClientImplementations/nettyHttpClient.adoc` → `[[nettyHttpClient]]`
  （被 introduction/同批 jdkHttpClient 引用——introduction 批间消解 + 批内闭环）
- `guide/httpClient/httpClientImplementations/jdkHttpClient.adoc` → `[[jdkHttpClient]]`
  （被 introduction 引用，已译——批间消解）
- `guide/httpClient/lowLevelHttpClient.adoc` → `[[lowLevelHttpClient]]`（被 creatingClient 引用，
  已译——批间消解）
- `guide/httpClient/lowLevelHttpClient/clientStreaming.adoc` → `[[clientStreaming]]`
  （被 clientAnnotationStreaming 引用，未译豁免承接）
- 其余 10 文件未被登记引用，无注入。

## 术语滚动

- 本批无新增 glossary 条目；新首现括注（按首现处理，频次待后续复核）：服务器端视图渲染、
  访问日志记录器（access logger）、主机名验证（hostname verification）、
  中间人攻击（Man-in-the-Middle）、工厂 bean（承 B10 factories 语境）；
- 既有术语命中：拦截器（未出现）、bean（小写保留）、依赖注入（不出现）、工厂（Factory Bean）、
  内省未出现；banned 黑名单 0 命中（validate ③ 全量扫描）。

## 里程碑

**httpServer 章（guide/httpServer，101 文件）全部 current——httpServer 全章译出**
（第六个全章：introduction、quickStart、IoC、config、AOP、httpServer）。
httpClient 章起步 9/26。**整库进度 208/388（53.6%）——过半。**

## 遗留与后续

- 21 条 ⑤ 豁免警告登记于 validate 输出，M3 全量断链清零时一并处理；
- 本批次未触发 sync --apply（冻结窗口遵守）；`source/` 无写入；
- restore 译丢段门禁再次证明价值：clientBasics 漏 callout 被拦（第 3 次：B10 锚点/B12 锚点/本批译丢段）；
- clientBasics.adoc（63 段、44 可译段）为 httpClient 章最长文件，对译检查通过后确认无返工。
