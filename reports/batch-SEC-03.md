# 批次报告：SEC-03（security 第三批 29 文件）

- 模块：security（micronaut-projects/micronaut-security，ref 5.2.x，基线 `cc524538f059`，快照 2026-11-23 锁定）
- 批次范围：SEC-03 = 29 文件（tokenendpoints 组 3 / retrievingAuthenticatedUser 组 4 / dataAuditing 组 3 / securityEvents / oauth 组 18：oauth 根 + installation + openid + flows/authorization-code 全树 + clientcredentials），**非代码词 3456 / 总词 3503**（inventory 实测）
- 流程：七步全流程（protect → 翻译 → restore → assemble → validate → mark-current；per-file commit SEC-01 已全采，幂等未重跑）
- validate 结果：**112 文件全绿（SEC-01 43 + SEC-02 40 + 本批 29）**；豁免警告 3 条，均为既有跟踪：
  - `endpoints.adoc`：loginController 悬空引用（上游即无该 id，SEC-01 建立 M3 跟踪）
  - `wwwAuthenticate.adoc` ×2：basicAuth / protectedResourceMetadata 未登记豁免——上游不平衡 xref 笔误（实测结论 12），basicAuth 锚已在位渲染闭环由冒烟兜底；protectedResourceMetadata 待 SEC-04 注入
- **开工即注入 3 锚 + 批内 1 锚（全部走译文首行路径，实测结论 13）**：
  - `[[oauth]]`（oauth.adoc）→ 消解 SEC-01 loginHandler 豁免
  - `[[openid-authorization-code]]`（openid-authorization-code.adoc）→ 消解 SEC-02 jwks 豁免之一
  - `[[keys]]`（keys.adoc）→ 消解 SEC-02 jwks 豁免之二
  - `[[openid-configuration]]`（openid-configuration.adoc）→ 批内闭环（pkce.adoc 引用）
  - SEC-02 收尾时列出的 3 条豁免全部随落盘消解；registry 中 SEC-02/01 页对 SEC-03 目标的引用全部闭环（oauth 被 loginHandler + aotOpenidConfiguration 引用，后者在 SEC-04）
- 批内裸 `<<target>>` xref 3 处（实测结论 8 口径：译显示文本+保留目标）：
  - oauth.adoc `<<loginHandler, 登录处理器>>` → SEC-01 已注入 [[loginHandler]]（开工前核实在位，zh 第 4 行）
  - openid-user-details.adoc `<<loginHandler, 登录处理器>>` + `<<logoutHandler, 登出处理器>>` → SEC-01 已注入
  - pkce.adoc `<<openid-configuration, 发现（Discovery）>>` → 批内注入闭环
- 门禁拦截与修复（全部真缺陷）：
  - validate 首轮 ⑦ 邻接 ×1（oauth2-configuration 占位符紧跟全角括号 ×2 同句）——初稿 grep 自查漏检此句，改写逗号分句后通过
  - validate 二轮 ③ bean ×13 文件 ×18 处——新译写大写「Bean」，glossary 口径为小写 bean 保留（上游惯例，SEC-01 先例「类型的 bean」）；落盘后统一修正（代码块内 beanContext 等不受影响）
- 术语写回（glossary modules: 分节，module: security，现 17 条）：refresh token→刷新令牌、access token→访问令牌（SEC-02 render.adoc 首译本批实录）、Client Credentials Grant→客户端凭证许可、nonce→nonce（不译）。**state/issuer 试用后撤回**：词形过于通用，③ 必译检查对既有 7 文件系统性误报（B22 滚动回流教训复现），在 context 中留注不收录理由
- 上游病句/笔误按语义等价口径处理：
  - nonce.adoc 两处游离反引号+括号（`(api:…CookieNoncePersistence[]`) and another one…`）：前者整段被 protect 收作不可译占位符原样还原（译句以中文括注衔接），后者在散文中按语义重写（去游离符号）
  - refresh.adoc「As you can see, is a form request」缺主语——补译主语
  - authorization-code.adoc 全篇长句重构（上游单句 60+ 词）
- 表格批次：securityEvents（事件表 7 行）、nonce/state（自定义接口职责表各 4 行）——CELLSEP/TABLEDELIM 占位符原样保留，仅译单元格文本
- 图片：本批无新增图片引用（image 宏 0 处）
- 周检：本会话开工例行 check_all 四快照模块全 0 变更（core cca2a1ce / security cc524538 / micrometer c4d064ee / validation 079f75dc），无需开 issue

*批次收尾：squash commit（本文件 + zh/modules/security/ 整目录 + manifests/security.yml + glossary + progress.md）*
