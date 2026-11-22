# 批次报告：SEC-04（security 第四批/收口批 28 文件）

- 模块：security（micronaut-projects/micronaut-security，ref 5.2.x，基线 `cc524538f059`，快照 2026-11-23 锁定）
- 批次范围：SEC-04 = 28 文件（oauth flows/clientcredentials 尾部 3 + password + oauth-endpoints 组 5 + custom-client/proxyToAuthServer/oauthGuides + ojdbcExtensions 组 8 + aot 组 4 + repository/ldap/securityRule 根层 3），**非代码词 2833 / 总词 2842**（inventory 实测）
- 流程：七步全流程（protect → 翻译 → restore → assemble → validate → mark-current；per-file commit SEC-01 已全采，幂等未重跑）
- validate 结果：**140 文件全绿（SEC-01 43 + SEC-02 40 + SEC-03 29 + 本批 28）**；security 模块 **145 条目全部处置完成 = 140 current + 5 skipped，进度 100%**
- 豁免警告 3 条（与 SEC-03 后一致，均为既有跟踪）：
  - `endpoints.adoc`：loginController 悬空引用（上游即无该 id，M3 跟踪）
  - `wwwAuthenticate.adoc` ×2：basicAuth / protectedResourceMetadata 未登记豁免——上游不平衡 xref 笔误，registry 扫描盲区（实测结论 12 口径）：警告分支保留，渲染闭环由显式锚注入保证（[[basicAuth]] SEC-02 + [[protectedResourceMetadata]] 本批），由全量渲染冒烟实测兜底
- **锚点注入**：
  - 本批目标页 `[[protectedResourceMetadata]]`（protectedResourceMetadata.adoc 译文首行，实测结论 13 路径）——wwwAuthenticate 两处不平衡 `<<protectedResourceMetadata, …>` 引用的目标自此存在
  - **回溯补注入 5 处（B16/B30/SEC-02 先例第 3 次）**：批内引用触发、既有页缺锚——[[runAs]]（privilegeEscalation 引用）、[[jwks]]（aotJwks 引用）、[[ipPattern]]/[[interceptUrlMap]]/[[builtInEndpointsAccess]]（securityRule 引用）；开工前逐一核实后统一在 zh 片段首内容之前注入；[[login]]/[[logout]]/[[oauth]]/[[secured]] 核实已在位无需补
- 批内裸 `<<target>>` xref 5 处（实测结论 8 口径）：password→login、privilegeEscalation→runAs、aotOpenidConfiguration→oauth、aotJwks→jwks、endsession→logout、securityRule→ipPattern/secured/interceptUrlMap/builtInEndpointsAccess（表格内 4 处）
- 门禁拦截与修复（全部真缺陷）：
  - validate ③ bean 口径 ×3 文件 ×4 处（endsession ×2/protectedResourceMetadata ×1/user-info ×1）——与 SEC-03 同款新译大写 Bean，统一改小写后全绿
- 术语：ojdbcExtensions 组「End User Security Context / DATA ROLE / Database Access Token」等按既定裁决**不收录 glossary**——均为 Oracle 产品域专有配置概念，句内首现加中文括注即可；本批 glossary 零改动（modules.security 维持 17 条）
- 上游病句/笔误按语义等价口径处理：
  - oauthGuides/clientCredentialGuides「learn more abut」→「了解更多……的内容」
  - securityRule 表头「UNKNOWN confition」拼写（应为 condition）译为「UNKNOWN 条件」
  - aot.adoc 引语块「…at runtime]」游离右方括号——语义等价重写，不保留游离符号
  - endUserSecurityContextConfiguration「separate by commas」语序修正
- 特殊结构实测：
  - repository.adoc 的 URL+ATTRREF 复合占位符（`{{URL}}{{ATTRREF}}[{{URL}}{{ATTRREF}}]`，显示文本与目标同构）——双重集占位符原样保留，restore/validate ①通过
  - user-info.adoc 嵌套占位符 `{{URL}}[{{CODE}} endpoint]`——URL 显示文本内含行内码占位符，整体保留仅译「端点」
  - proxyToAuthServer 表格 4 个单格数据行（上游表头 2 列、数据行 1 列）——结构原样保留，asciidoctor 渲染层自行补齐空格
- 图片：本批无新增图片引用（password.adoc 的 2 个 image 指令为 include 引用的 SVG，快照已在库）
- 本批后遗留豁免跟踪（security 模块终态）：endpoints→loginController（上游悬空，M3 跟踪）+ wwwAuthenticate ×2（上游不平衡 xref，registry 盲区，渲染闭环已由锚注入保证）

*批次收尾：squash commit（本文件 + zh/modules/security/ 整目录 + manifests/security.yml + progress.md）*

## 全量渲染冒烟（三批统一，本批后执行）

- 产物：security.html 144/144 片段全渲染（含 5 个 skipped 壳的标题级页头），failureCount 0；产物时间戳实测更新（坑位 19）
- **本会话注入的 10 锚全部 href↔id 闭环**（oauth/openid-authorization-code/openid-configuration/keys/protectedResourceMetadata/runAs/jwks/ipPattern/interceptUrlMap/builtInEndpointsAccess）
- 悬空 href 终态 1 条：loginController（上游悬空，官方站亦无该 id，M3 跟踪维持）
- **冒烟发现并修复 render.mjs 两处内容缺口**（基建修复单独提交，冒烟纪律实跑）：
  1. 无页 toc 分组键（reader/flows/oauth-endpoints/securityRule/ldap）官方站生成 `<h2 id="security-<键>">`，本站此前不生成 → 5 条导航死链；修复：分组键（dict 节点）缺页时输出标题级页头，导航闭环
  2. 根层 securityRule.adoc/ldap.adoc 未入 toc → 不在片段清单 → **已译内容静默缺失**（官方站渲染在同名分组标题下）；修复：未入 toc 片段按 basename 挂载到同名分组键
  3. 「部分译文」横幅改以 missingPage（真实未译叶页）为条件——security 100% 后横幅不再误显（此前 139/144 系把 5 个 skipped 壳计入分母）
- 回归对照：core/micrometer/validation/landing 四页修复前后逐字节一致（备份 /tmp/render-smoke-before）；security 修复前后 missingPage 5→0、rendered 139→144
- 已知噪音（预存在，非本批回归）：重复自动 id（多模块同名 CJK 标题，core 8 处/micrometer 1 处，无 href 指向）；asciidoctor「no callout found」警告（M4.0 起即有）
