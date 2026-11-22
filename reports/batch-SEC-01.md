# 批次报告：SEC-01（security 首批 42 文件 + toc.yml）

- 模块：security（micronaut-projects/micronaut-security，ref 5.2.x，默认分支 5.5.x，基线 `cc524538f059`，快照 2026-11-23 锁定）
- 批次范围：SEC-01 = 42 文件（introduction / releaseHistory / whatsNew / breaks / security-installation / securityFilter 组 18 文件 / exceptionHandlers / endpoints 组 10 文件 / securityConfiguration 组 5 文件 / authenticationProviders 组 4 文件 / authenticationStrategies 的 basicAuth+session+jwt）+ toc.yml 导航标题，**非代码词 3432 / 总词 3454**（inventory 实测）
- 段数：账本 145 条目合计 857 段，本批 43 条目（42 adoc + toc.yml）
- 流程：七步全流程；per-file commit --collect-commits 145 条全采（0 失败）→ validate --manifest 全绿 → --mark-current 43 条核销（97 条 SEC-02/03/04 保持 missing）
- validate 结果：43 文件全绿；豁免警告 2 条：
  - `endpoints.adoc`：⑤ 裸锚点 loginController 未登记——上游即悬空引用（官方站亦无该 id，跨站指向 core LoginController 节），按 DR-006 §9 保持原样跟踪
  - `loginHandler.adoc`：⑤ 目标未译 modules/security/guide/oauth.adoc#oauth——oauth 在 SEC-03，待该批注入 [[oauth]] 后消解
- 快照口径调整（随本批生效，坑位 25）：
  - security resources/img/security_diagramms.sketch（3.3MB，Sketch 设计源文件）触发 2MB 单文件硬上限。按 SOP §4「快照仅 .adoc + toc + resources 图片入库」口径，read_upstream 改为白名单外扩展名不入库并告警；guide/ 0 引用该文件，core 资源目录实测全为白名单类型，无回归
  - 入库图片 33 个 5.9MB（不含 sketch）；单模块 5.9MB，多模块累加距 300MB 仍远，**git-lfs 维持不启用**
- 实译发现与处置：
  - **裸 `<<target>>` xref 首次在模块出现（11 个页级目标）**：译文按 core 惯例译显示文本、保留目标，并在目标页片段首内容之前原位注入 [[basename]] 显式锚 8 处（login/authenticationProviders/redirection/securityFilter/loginHandler/logout/logoutHandler/secured）；render 后 href ↔ id 闭环实测通过
  - validate ⑤ 登记表路径双前缀缺陷修复：登记表 file 字段为 source/ 相对路径（模块条目自带 modules/<site>/ 前缀），原实现再拼 doc_prefix 致模块裸锚 15 处全误报「目标文件不存在」——registry 命中路径不再叠加前缀；pytest 123 绿
  - ④ whatsNew 标题「What's New in Micronaut Security 3」→「Micronaut Security 3 的新特性」
  - 上游英文病句（builtInHandlers 4 个认证模式页「X a bean of type Y is enabled」重复 API 名）按语义等价译出「设置 X 后，会启用 Y——一个 Z 类型的 bean」，两处 API 名均保留
  - ⑦ 邻接规则零违规（初稿即避开 `标记+全角开括号` 模式）
- 术语写回（glossary modules: 分节，module: security）：Authentication Provider→认证提供者、Authentication Fetcher→认证获取器、Token Reader→令牌读取器、Token Validator→令牌校验器、Login Handler→登录处理器、Logout Handler→登出处理器、Security Rule→安全规则、Claims（不译）、Intercept URL Map（不译+括注）
- toc 键错位实测：securityFilter/securityRule 与 authenticationStrategies/ldap 两键的 toc 嵌套层级与文件实际路径不一致（文件在 guide 根层），inventory 已如实标注；check_toc 只比键树不受影响，文件均已被批次覆盖

*批次收尾：squash commit（本文件 + zh/modules/security/** 整目录 + manifests/security.yml + glossary + validate ⑤ 修复）*
