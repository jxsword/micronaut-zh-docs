# 批次报告：SEC-02（security 第二批 40 文件）

- 模块：security（micronaut-projects/micronaut-security，ref 5.2.x，基线 `cc524538f059`，快照 2026-11-23 锁定）
- 批次范围：SEC-02 = 40 文件（jwt reader 组 2 / jwtParser+jwtValidation+jwks 组 6 / jwtGenerator 组 4 / jwtEncryption 组 3 / claims+render+jwtGuides 4 / ldap configuration+extending 2 / x509 / custom / rejection 组 2 / csrf 组 14 / htmlSanitizer / tokenPropagation），**非代码词 3452 / 总词 3539**（inventory 实测）
- 流程：七步全流程（protect → 翻译 → restore → assemble → validate → mark-current；per-file commit SEC-01 已全采，幂等未重跑）
- validate 结果：83 文件全绿（SEC-01 43 + 本批 40）；豁免警告 6 条，均为预期中间态或既有跟踪：
  - `jwks.adoc` ×2：目标未译 openid-authorization-code / keys（均在 SEC-03，待该批注入 [[openid-authorization-code]]、[[keys]] 后消解）
  - `loginHandler.adoc`：目标未译 oauth.adoc（SEC-03 遗留，同上）
  - `endpoints.adoc`：loginController 悬空引用（上游即无该 id，SEC-01 已建立 M3 跟踪）
  - `wwwAuthenticate.adoc` ×2：basicAuth / protectedResourceMetadata 未登记豁免——根因是上游 xref 笔误（`<<basicAuth, basic auth>` 缺右 `>`，不平衡括号致 check_anchors 扫描未捕获），渲染层闭环由显式锚注入保证，protectedResourceMetadata 待 SEC-04 注入
- 门禁拦截与修复（全部真缺陷）：
  - restore 首轮拦 2 处译丢段：jwtValidation 丢 `qualified` 链接占位符、doubleSubmitCookiePattern 丢 Cookie prefix 防护链接占位符——补齐后全过（40/40）
  - validate 首轮 4 项错误：jwks/staticJwks ③ classpath 未译「类路径」×2；doubleSubmitCookiePattern/httpHeaderCsrfTokenResolver ⑤ 引用 csrfConfiguration 但目标译文缺 [[csrfConfiguration]] 锚（批内闭环，注入后消解）——修复后全绿
- **回溯补注入 4 处（B16 [[events]] / B30 [[config]] 先例）**：SEC-01 的 11 个页级目标中 4 个此前未注入的锚被本批引用触发——[[basicAuth]]（basicAuth.adoc）、[[session]]（session.adoc）、[[micronautSecurityAuthenticationCookie]]、[[micronautSecurityAuthenticationIdToken]]（builtInHandlers 两模式页），均在 zh 片段首内容之前原位注入；SEC-01 报告的「8 处注入」实际对应 11 目标中已引用的子集，本批补齐后被引用目标全部闭环
- csrfConfiguration 锚点注入走**译文首行**路径（-translated.txt 首行 [[csrfConfiguration]] → restore → assemble 后落位于片段首内容之前），与 SEC-01 直接 Edit zh 片段的路径等价且对 re-assemble 幂等
- 术语写回（glossary modules: 分节，module: security，现 13 条）：sanitizer→净化器、token propagation→令牌传播
- 上游病句/笔误按语义等价口径处理：
  - jwtValidation「The easiest way is to create … is to have」重复谓语；custom「users access your application are authenticated」缺关系从句；httpHeaderCsrfTokenResolver「ships a X an implementation」重复冠词；signedDoubleSubmitCookiePattern「Sign the CSRF Token with to prevent」缺宾语（补译为对 CSRF Token 签名防覆盖）；doubleSubmitCookiePattern「can extend security protections」缺主语；jwks 标题「JKWS」拼写（应为 JWKS，原样保留）
  - wwwAuthenticate 的两处不平衡 `<<target, text>` xref 原样保留结构（不擅自补全括号），仅译显示文本
- 特殊结构实测：httpHeaderCsrfTokenResolver 的 URL 含括号锚 `#anti-forgery-support-(csrf)`——protect 把 URL 截断至括号前，译文中原样保留 `(csrf)` 字面，restore 后与占位符拼回完整 URL
- ⑦ 邻接规则：初稿 grep `}}（` 自查拦 1 处（x509「{{…}}（取决于…）」改写为逗号分句），validate 层面零违规
- 图片：本批无新增图片引用（image 宏 0 处）

*批次收尾：squash commit（本文件 + zh/modules/security/ 整目录 + manifests/security.yml + glossary + progress.md）*
